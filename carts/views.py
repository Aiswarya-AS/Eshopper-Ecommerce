from math import prod
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from carts.models import CartItem
from category.models import Product
from carts.models import Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from userprofile.models import Address
from category.models import Category,Subcategory
from django.http import HttpResponseRedirect
# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart


def add_cart(request):
    if request.method=='POST':
        product_id=int(request.POST.get('product_id'))
        product_qty=int(request.POST.get('product_quantity'))
        print(product_id,"??????????????????????????????????????????????")
        current_user=request.user
        product=Product.objects.get(id=product_id)

        if current_user.is_authenticated:
            try:
                cart_item=CartItem.objects.get(product=product,user=current_user)
                
                if product.stock > product_qty:
                    cart_item.quantity+=product_qty
                    cart_item.save()
                    messages.success("Added to cart")
                else:
                    return JsonResponse("Product out of stock")
                
            except CartItem.DoesNotExist:
                cart_item=CartItem.objects.create(
                    product=product,
                    quantity=product_qty,
                    user=current_user,

                )
            cart_item.save()
            
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
        else:

            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                cart=Cart.objects.create(
                    cart_id=_cart_id(request)
                )
            cart.save()

            try:
                cart_item=CartItem.objects.get(product=product,cart=cart)
                cart_item.quantity+=product_qty
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item=CartItem.objects.create(
                    product=product,
                    quantity=product_qty,
                    cart=cart,

                )
            cart_item.save()
        
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


def cart(request,total=0,quantity=0,cart_items=None):
    category=Category.objects.all()
    subcategory=Subcategory.objects.all()
    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:

            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)

        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
    except:
        pass
    return render(request,'customerapp/cart.html',{
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'category':category,
        'subcategory':subcategory,
    })


def delete_cart_item(request,product_id):
    
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
            cart_item=CartItem.objects.filter(product=product,user=request.user)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login-page')
def checkout(request,total=0,quantity=0):
    address=Address.objects.filter(user=request.user)
    cart_items=CartItem.objects.filter(user=request.user,is_active=True)
    for cart_item in cart_items:
        total+=(cart_item.product.price*cart_item.quantity)
        quantity+=cart_item.quantity
    return render(request,'customerapp/checkout.html',{
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'address':address
    })

def update_cart(request):
    if request.method=='POST':
        product_id=int(request.POST.get('product_id'))
        if request.user.is_authenticated:
            if (CartItem.objects.filter(user=request.user,product_id=product_id)):
                product_quantity=int(request.POST.get('product_quantity'))
                cart_items=CartItem.objects.get(product_id=product_id,user=request.user)
                cart_items.quantity=product_quantity
                cart_items.save()
                return JsonResponse({'status':"updated successfully"})
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(product_id=product_id,cart=cart)   
            cart_item.save()
            return JsonResponse({'status':"updated successfully"})