from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from shop.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json
# from django.http import HttpResponse

def home(request):
    Product_t=Products.objects.filter(trending=1)
    return render(request,'shoptmplt/index.html',{'Product_t':Product_t})

def fav_Viewpage(request):
     if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,'shoptmplt/fav.html',{'fav':fav})
     
     else:
        return redirect("/")
     
def remove_fav(request,fid):
    cartitem=Favourite.objects.get(id=fid)
    cartitem.delete()
    return redirect('/fav_Viewpage')


def cartPage(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'shoptmplt/cart.html',{'cart':cart})

    else:
        return redirect("/")

def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart')


def favPage(request):
    if request.headers.get('X-Request-With')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=(data['pid'])
            product_status=Products.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in add to Favourite'},status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
            return JsonResponse({'status':'Product added to favourite'},status=200)
           
        else:
            return JsonResponse({'status':'Login to add favourite'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)


def addToCart(request):
    if request.headers.get('X-Request-With')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=(data['product_qty'])
            product_id=(data['pid'])
            # print(request.user.id)
            product_status=Products.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in add to card'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to card'},status=200)
                    else:
                        return JsonResponse({'status':'Product Product Stock Not Available'},status=200)

        else:
            return JsonResponse({'status':'Login to add Card'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
   



def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success you can login now..")
            return redirect('/login')
    return render(request,'shoptmplt/register.html',{'form':form})

def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logged Out Successfully')
    return redirect("/")


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
                name=request.POST.get('username')
                pwd=request.POST.get('password')
                user=authenticate(request,username=name,password=pwd)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Successfully')
                    return redirect("/")
                else:
                    messages.error(request,'Invalid User Name or Password')
                    return redirect('/login')
        return render(request,'shoptmplt/login.html')


def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,'shoptmplt/collections.html',{'catagory':catagory})
def collectionsview(request,name):
    if (Catagory.objects.filter(name=name,status=0)):
        Product=Products.objects.filter(Catagory__name=name)
        return render(request,'products/index.html',{'Product':Product,"catagory_name":name})    
    else:
        messages.warning(request,"No such category Found")
        return redirect('collections')


def products_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Products.objects.filter(name=pname,status=0)):
            Product=Products.objects.filter(name=pname,status=0).first()
            return render(request,'products/product_Detail.html',{'Product':Product})
        else:
            messages.error(request,"No such category Found")
            return redirect('collections')
            
        
    else:
        messages.error(request,"No such category Found")
        return redirect('collections')




