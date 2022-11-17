from math import prod
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from carts.models import CartItem
from category.models import Product
from carts.models import Cart
from django.contrib.auth.decorators import login_required
from userprofile.models import Address
from category.models import Category,Subcategory,Variations
from django.http import HttpResponseRedirect
# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart


def add_cart(request,product_id):
    product_variation=[]
    current_user=request.user
    product=Product.objects.get(id=product_id)
    if request.method=="POST":
        c=request.POST.get('color')
        s=request.POST.get('size')

        try:
            variation=Variations.objects.get(product=product,color=c,size=s)
            product_variation.append(variation)
        except:
            pass

    if current_user.is_authenticated:
        try:
            cart_item=CartItem.objects.get(product=product,user=current_user)
            if len(product_variation) >0:
                cart_item.variations.clear()
                for item in product_variation:
                    cart_item.variations.add(item)
            cart_item.quantity+=1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,

            )
            if len(product_variation) >0:
                cart_item.variations.clear()
                for item in product_variation:
                    cart_item.variations.add(item)
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
            if len(product_variation) >0:
                cart_item.variations.clear()
                for item in product_variation:
                    cart_item.variations.add(item)
            cart_item.quantity+=1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,

            )
            if len(product_variation) >0:
                cart_item.variations.clear()
                for item in product_variation:
                    cart_item.variations.add(item)
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
            if cart_item.product.offer_price():
                offer_price=Product.offer_price(cart_item.product)
                total+=(offer_price["new_price"]*cart_item.quantity)
            else:
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

def remove_from_cart(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(product=product,cart=cart)
    
        if cart_item.quantity > 1:
            cart_item.quantity-=1  
            cart_item.save()

        else:
            cart_item.delete()
    except:
        pass
    # return redirect('cart')
    return JsonResponse({
        'quantity':'quantity',
    })

def delete_cart_item(request,product_id):
    
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user)
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
        if cart_item.product.offer_price():
                offer_price=Product.offer_price(cart_item.product)
                total+=(offer_price["new_price"]*cart_item.quantity)
        else:
            total+=(cart_item.product.price*cart_item.quantity)
    
        quantity+=cart_item.quantity
    return render(request,'customerapp/checkout.html',{
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'address':address
    })