from django.urls import path
from . import views

from store.controller import authview, cart, wishlist, checkout, profile, order

urlpatterns = [
  path('', views.home, name="home"),
  path('collections', views.collections, name="collections"),
  path('collections/<str:slug>', views.collectionsview, name="collectionsview"),
  path('collections/<str:cate_slug>/<str:prod_slug>', views.productview, name="productview"),

  path('product-list', views.productlist),
  path('searchproduct', views.searchproduct, name="searchproduct"),
  
  path('register/', authview.register, name="register"),
  path('login/', authview.loginpage, name="loginpage"),
  path('logout/', authview.logoutpage, name="logout"),
  
  path('add-to-cart', cart.add_to_cart, name="addtocart"),
  path('cart/', cart.viewcart, name="cart"),
  path('update-cart', cart.update_cart, name="update_cart"),
  path('delete-cart-item', cart.deletecartItem, name="deletecartItem"),

  path('wishlist', wishlist.index, name="wishlist"),
  path('add-to-wishlist', wishlist.addtowishlist, name="addtowishlist" ),
  path('delete-wishlist-item', wishlist.deletewishlistitem, name="deletewishlistitem"),
  
  path('checkout', checkout.index, name="checkout"),
  path('placeorder', checkout.placeorder, name="placeorder"),
  path('verify', checkout.verify, name="verify"),
  
  path('my-orders', order.index, name='myorders'),
  path('view-order/<str:t_no>', order.orderview, name="orderview"),
  
  path('profile/', profile.view_profile, name='view_profile'),
  path('delete-profile-image', profile.delete_profile_image, name='delete-profile-image'),
  path('update-profile-image/', profile.update_profile_image, name='update-profile-image'),

  
]