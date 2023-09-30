from store.models import Cart, Order, OrderItem, Product, Profile
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
import random
from django.contrib import messages
# from django.contrib.auth.models import User

@login_required(login_url='login_required')
def index(request):
  rawcart = Cart.objects.filter(user=request.user)
  for item in rawcart:
    if item.product_qty > item.product.quantity :
      Cart.objects.delete(id=item.id)

  cartitems = Cart.objects.filter(user=request.user)
  total_price = 0
  for item in cartitems:
    total_price = total_price + item.product.selling_price * item.product_qty

  userprofile = Profile.objects.filter(user=request.user).first()
  context = {'cartitems':cartitems, "total_price": total_price, "userprofile": userprofile}
  return render(request, 'store/checkout.html', context)


@login_required(login_url="loginpage")
def placeorder(request):
    if request.method == 'POST':
        currentuser = request.user
        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()

        try:
            userprofile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            userprofile = Profile(
                user=request.user,
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                country=request.POST.get('country'),
                pincode=request.POST.get('pincode')
            )
            userprofile.save()

        neworder = Order(
            user=request.user,
            fname=request.POST.get('fname'),
            lname=request.POST.get('lname'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            country=request.POST.get('country'),
            pincode=request.POST.get('pincode'),
            payment_mode=request.POST.get('payment_mode'),
            payment_id=request.POST.get('payment_id')
        )

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price += item.product.selling_price * item.product_qty

        neworder.total_price = cart_total_price
        trackno = 'segzy' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = 'segzy' + str(random.randint(1111111, 9999999))
        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )

            # To decrease the product from available stock
            orderproduct = Product.objects.get(id=item.product_id)
            orderproduct.quantity -= item.product_qty
            orderproduct.save()

        # To clear user Cart
        Cart.objects.filter(user=request.user).delete()

        messages.success(request, "Your order has been placed successfully")

        # Check payment mode
        payMode = request.POST.get('payment_mode')
        if payMode in ["paid by paystack", "paid by PayPal"]:
            return JsonResponse({'status': "Your order has been placed successfully"})

        return redirect('/')

    # If the request is not POST, return a bad request response
    return HttpResponseBadRequest("Bad Request")

# @login_required(login_url="loginpage")
# def placeorder(request):
#   if request.method == 'POST':
#     currentuser = User.objects.filter(id=request.user.id).first()
#     if not currentuser.first_name :
#       currentuser.first_name = request.POST.get('fname')
#       currentuser.last_name = request.POST.get('lname')
#       currentuser.save()
#     if not Profile.objects.filter(user=request.user):
#       userprofile = Profile()
#       userprofile.user = request.user
#       userprofile.phone = request.POST.get('phone')
#       userprofile.address = request.POST.get('address')
#       userprofile.city = request.POST.get('city')
#       userprofile.state = request.POST.get('state')
#       userprofile.country = request.POST.get('country')
#       userprofile.pincode = request.POST.get('pincode')
#       userprofile.save()
    
#     neworder = Order()
#     neworder.user = request.user
#     neworder.fname = request.POST.get('fname')
#     neworder.lname = request.POST.get('lname')
#     neworder.email = request.POST.get('email')
#     neworder.phone = request.POST.get('phone')
#     neworder.address = request.POST.get('address')
#     neworder.city = request.POST.get('city')
#     neworder.state = request.POST.get('state')
#     neworder.country = request.POST.get('country')
#     neworder.pincode = request.POST.get('pincode')

#     neworder.payment_mode = request.POST.get('payment_mode')
#     neworder.payment_id = request.POST.get('payment_id')
    

#     cart = Cart.objects.filter(user=request.user)
#     cart_total_price = 0
#     for item in cart:
#       cart_total_price = cart_total_price +item.product.selling_price * item.product_qty

#     neworder.total_price = cart_total_price
#     trackno = 'segzy'+str(random.randint(1111111, 9999999))
#     while Order.objects.filter(tracking_no=trackno) is None:
#       trackno = 'segzy'+str(random.randint(1111111, 9999999))

#     neworder.tracking_no = trackno
#     neworder.save()

#     neworderitems = Cart.objects.filter(user=request.user)
#     for item in neworderitems:
#      OrderItem.objects.create(
#         order=neworder,
#         product=item.product,
#         price=item.product.selling_price,
#         quantity=item.product_qty
#       )

#     # To decreate the product from available stock
#     orderproduct = Product.objects.filter(id=item.product_id).first()
#     orderproduct.quantity = orderproduct.quantity - item.product_qty
#     orderproduct.save()
#   # To clear user Cart
#     Cart.objects.filter(user=request.user).delete()
  
#     messages.success(request, "Your order has been placed successfully")
#   # check mode
#     payMode = request.POST.get('payment_mode')
#     if(payMode ==  "paid by paystack" or payMode ==  "paid by PayPal"):
#       return JsonResponse({'status': "Your order has been placed successfully"})
#   return redirect('/')

@login_required(login_url="loginpage")
def verify(request):
    try:
        # Filter orders by user and get one order if it exists
        order = Order.objects.filter(user=request.user).first()
        
        if order:
            tracking_no = order.tracking_no
        else:
            tracking_no = None
    except Order.DoesNotExist:
        tracking_no = None

    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price += item.product.selling_price * item.product_qty

    return JsonResponse({
        'total_price': total_price,
        'tracking_no': tracking_no,
    })

def orders(request):
  return HttpResponse("My orders page")