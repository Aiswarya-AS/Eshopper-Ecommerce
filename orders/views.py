from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render

# Create your views here.
from userprofile.models import Address
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from carts.models import CartItem
from category.models import Product
from orders.models import Order, OrderItem
from django.contrib import messages
from offers.models import Coupon,ReviewCoupon
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
        address=Address.objects.get(id=request.POST.get('address'))
        neworder.address=address
        print(neworder.address)
        neworder.payment_mode=request.POST.get('payment_mode')
        neworder.payment_id=request.POST.get('payment_id')

        
        cart_items=CartItem.objects.filter(user=request.user)
        cart_total_price=0
        for cart_item in cart_items:
            if cart_item.product.offer_price():
                offer_price=Product.offer_price(cart_item.product)
                cart_total_price+=(offer_price["new_price"]*cart_item.quantity)
            else:
                cart_total_price+=(cart_item.product.price*cart_item.quantity)

            if cart_item.coupon_discount:
                cart_total_price=cart_item.coupon_discount
            else:
                pass
        
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
        

        pay_mode=request.POST.get('payment_mode')
        if(pay_mode=="Razorpay" or pay_mode=="Paypal"):
            return JsonResponse({'status':"Your order has been placed Succesfully"})

    
    return redirect('order_summary')


@login_required(login_url='login-page')
def order_cancel(request,id):
    order_item=OrderItem.objects.get(id=id)
    product=Product.objects.get(id=order_item.product_id)
    product.stock+=order_item.quantity
    product.save()
    order_item.status="Order Cancelled"
    order_item.save()
    
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required(login_url='login-page')
def proceed_to_pay(request):
    cart_item=CartItem.objects.filter(user=request.user)
    total_price=0
    for item in cart_item:
        total_price=total_price+item.product.price*item.quantity
    return JsonResponse({
        'total_price':total_price
    })


def order_status_change(request):
    id=request.POST['id']
    status=request.POST['status']
    order_item=OrderItem.objects.get(id=id)
    order_item.status=status
    order_item.save()
    return JsonResponse({"success":True})

def return_order(request,id):
    order_item=OrderItem.objects.get(id=id)
    order_item.status="Requested For Return"
    order_item.save()
    
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def accept_return(request,id):
    
    order_item=OrderItem.objects.get(id=id)
    
    order_item.status="Refund Initiated"
    product_id=order_item.product_id
    product=Product.objects.get(id=product_id)
    product.stock+=order_item.quantity
    order_item.save()
    product.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])





# for generating pdf invoice

from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.views.generic import View
from django.template.loader import get_template
class generateInvoice(View):
    def get(self,request,id,*args,**kwargs):
        try:
            orders=Order.objects.get(id=id,user=request.user)
            
        except:
            return HttpResponse("505 not found")
        data={
            'order_id':orders.id,
            'date':str(orders.created_at),
            'name':orders.user.first_name,
            'address':orders.address.address,
            'total_price':orders.total_price,
            'transaction_id':orders.payment_id,
            'payment_mode':orders.payment_mode,
            'user_email':orders.user.email,
            'orders':orders
        }
        pdf=render_to_pdf('customerapp/invoice.html',data)
        return HttpResponse(pdf,content_type='application/pdf')

def render_to_pdf(template_src,context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None



