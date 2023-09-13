from django.urls import path
from .import views

urlpatterns = [
  path('',views.home,name="home"),
  path('register',views.register,name="register"),
  path('login',views.loginPage,name="login"),
  path('logout',views.logoutPage,name="logout"),
  path('cart',views.cartPage,name="cart"),
  path('fav',views.favPage,name="fav"),
  path('fav_Viewpage',views.fav_Viewpage,name="fav_Viewpage"),
  path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav"),
  path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
  path('collections',views.collections,name="collections"),
  path('collections/<str:name>',views.collectionsview,name="collections"),
  path('collections/<str:cname>/<str:pname>',views.products_details,name="products_details"),
  path('addToCart',views.addToCart,name="addToCart"),
]