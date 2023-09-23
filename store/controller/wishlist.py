from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from store.models import Product, Wishlist

@login_required(login_url="loginpage")
def index(request):
  wishlistitems = Wishlist.objects.filter(user=request.user)
  context = {'wishlist': wishlistitems}
  return render(request, 'store/wishlist.html', context)


def addtowishlist(request):
  if request.method == 'POST':
    if request.user.is_authenticated:
      prod_id = int(request.POST.get('product_id'))
      product_check = Product.objects.get(id=prod_id)
      if(product_check):
        if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
          return JsonResponse({'status':"Product Already in Wishlist"})
        else:
          Wishlist.objects.create(user=request.user, product_id=prod_id)
          return JsonResponse({'status': "Product added to wishlist"})
      else:
        return JsonResponse({'status': "No such product found"})

    else:
      return JsonResponse({'status': "Login to continue"})
  return redirect("/")


def deletewishlistitem(request):
  if request.method == 'POST':
    if request.user.is_authenticated:
      prod_id = int(request.POST.get('product_id'))
      
      if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
        wishlistitem = Wishlist.objects.get(product_id=prod_id)
        wishlistitem.delete()
        return JsonResponse({'status':"Product removed from Wishlist"})
      else:
        return JsonResponse({'status': "Product not found in wishlist"})
    else:
      return JsonResponse({'status': "Login to continue"})
  return redirect("/")