from django.shortcuts import HttpResponseRedirect, render

# Create your views here.
from userprofile.models import Address
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from carts.models import CartItem
from category.models import Product
from orders.models import Order, OrderItem
from django.contrib import messages
# Create your views here.

@login_required(login_url='login-page')
def order_summary(request):
    orders=Order.objects.filter(user=request.user).order_by('created_at')[::-1]
    print(orders)
    # order_items=OrderItem.objects.filter(order=orders)
    return render(request,'customerapp/ordersummary.html',{
        # 'order_items':order_items,
        'orders':orders,
    })
def orderview(request,id):
    orders=Order.objects.filter(id=id).filter(user=request.user).first()
    order_items=OrderItem.objects.filter(order=orders)
    context={
        'orders':orders,
        'order_items':order_items
    }
    return render(request,'customerapp/orderview.html',context)


@login_required(login_url='login-page')
def place_order(request):
    if request.method=='POST':
        neworder=Order()
        neworder.user=request.user
        # address_id=request.POST.get('radio-address')
        # print(address_id,'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        neworder.address=Address.objects.get(id=request.POST.get('radio-address'))
        neworder.payment_mode=request.POST.get('payment_mode')

        cart_items=CartItem.objects.filter(user=request.user)
        cart_total_price=0
        for cart_item in cart_items:
            cart_total_price+=(cart_item.product.price*cart_item.quantity)
        

        neworder.total_price=cart_total_price
        neworder.save()


        neworderitems=CartItem.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
                
                
            )
        


            orderproduct=Product.objects.filter(id=item.product_id).first()
            orderproduct.stock-=item.quantity
            orderproduct.save()


        CartItem.objects.filter(user=request.user).delete()
        messages.success(request,'Your order has been placed Succesfully')

    
    return redirect('order_summary')
    

def order_cancel(request,id):
    print('>>>>>>>>>>>>>>>>>>>>>>>')
    order_item=OrderItem.objects.get(id=id)
    product=Product.objects.get(id=order_item.product_id)
    # orders=Order.objects.get(user=request.user,id=order_item.product_id)
    # print(orders,'?????????????????')
    product.stock+=order_item.quantity
    product.save()
    order_item.status="Order Cancelled"
    order_item.save()
    
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

