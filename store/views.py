from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Product
from django.http import JsonResponse

# Create your views here.
def home(request):
  trending_products = Product.objects.filter(trending=1)
  category = Category.objects.filter(status=0)
  context = {
    'trending_products':trending_products,
    'category': category,
  }
  return render(request, "store/index.html", context)


def collections(request):
  category = Category.objects.filter(status=0)
  context = {'category': category}
  return render(request, "store/collections.html", context)


def collectionsview(request, slug):
  if(Category.objects.filter(slug=slug, status=0)):
    products = Product.objects.filter(category__slug=slug)
    category = Category.objects.filter(slug=slug).first()
    content = {'products': products, 'category': category}
    return render(request, "store/products/index.html", content)
  else:
    messages.warning(request, "No such category found for product")
    return redirect('collections')


def productview(request, cate_slug, prod_slug):
  if(Category.objects.filter(slug=cate_slug, status=0)):
    if(Product.objects.filter(slug=prod_slug, status=0)):
      products = Product.objects.filter(slug=prod_slug, status=0).first
      content = {'products': products}
    else:
      messages.error(request, "No Such catagory found")
      return redirect('collections')
  else:
    messages.error(request, "No Such catagory found")
    return redirect('collections')
  return render(request, "store/products/view.html", content)


def productlist(request):
    products = Product.objects.filter(status=0).values_list('name', flat=True)
    productlists = list(products)

    return JsonResponse(productlists, safe=False)

def searchproduct(request):
  if request.method == 'POST':
    searchedterm = request.POST.get('productsearch')
    if searchedterm == "":
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      product = Product.objects.filter(name__contains=searchedterm).first()

      if product:
        return redirect("collections/"+product.category.slug+"/"+product.slug)
      else:
        messages.info(request, "No product matched your search")
        return redirect(request.META.get('HTTP_REFERER'))
        
      
      

  return redirect(request.META.get('HTTP_REFERER'))
    