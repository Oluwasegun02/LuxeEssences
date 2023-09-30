# from store.models import Cart, Order, OrderItem, Product, Profile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse, HttpResponse
# from django.contrib import messages
from store.models import Order, OrderItem
# from django.contrib.auth.models import User
@login_required(login_url='login_required')
def index(request):
  orders = Order.objects.filter(user=request.user)
  context = {'orders':orders}
  return render(request, 'store/orders/index.html', context)


def orderview(request, t_no):
  order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
  orderitems = OrderItem.objects.filter(order=order)
  context = {'order':order, 'orderitems':orderitems}
  return render(request, 'store/orders/view.html', context )