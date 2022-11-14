from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from accounts.models import CustomUser
from carts.models import CartItem
from category.models import Category, Product, Subcategory
from .forms import RegistrationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import random
from twilio.rest import Client
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

from carts.views import _cart_id
from carts.models import Cart,CartItem

from django.views.decorators.cache import never_cache
# Create your views here.
def user_register(request):
    
    form=RegistrationForm()
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            phone=request.POST.get('phone')
            print(phone)
            user=form.save()
            return redirect('login-page')
            # messages.success(request,"Account Created !")
            # return redirect('home')
    return render(request,'customerapp/register.html',{
        'form':form
    })


# def index(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#         return redirect('admin-login')


@never_cache
def home(request):
    # if request.user.is_authenticated:
    #     return redirect(home)
    if request.user.is_superuser:
        return redirect('adminlogin')
    category=Category.objects.all()
    subcategory=Subcategory.objects.all()
    trendy=Product.objects.all()[:4]
    
    return render(request,'customerapp/home.html',{
        'category':category,
        'subcategory':subcategory,
        'trendy':trendy
    })



def user_logout(request):
    logout(request)
    return redirect('login-pass')

def store(request,subcategory_slug=None):
    category=Category.objects.all()
    subcategories=None
    products=None

    if subcategory_slug!=None:
        subcategories=get_object_or_404(Subcategory,slug=subcategory_slug)
        products=Product.objects.filter(subcategory=subcategories,)
        paginator=Paginator(products,2)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
    else:

        products=Product.objects.all()
        paginator=Paginator(products,4)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
    return render(request,'customerapp/store.html',{
        'category':category,
        'products':paged_products
    })

from category.models import Variations
def product_detail(request,subcategory_slug,product_slug):
    category=Category.objects.all()
    
    try:
        single_product=Product.objects.get(subcategory__slug=subcategory_slug,slug=product_slug) 
        variation=Variations.objects.filter(product=single_product.id)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        
        
        
    except Exception as e:
        raise e
    

    return render(request,'customerapp/product-detail.html',{
        'single_product':single_product,
        'category':category,
        'in_cart':in_cart,
        'variation':variation
        
    })


def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            
            products=Product.objects.order_by('-added_date').filter(product_name__icontains=keyword)

    context={
        'products':products
    }
    
    return render(request,'customerapp/store.html',context)





def login_otp(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =='GET':
        phone=request.GET.get('phone')
        print(phone)
        OtpGenerate.send_otp(phone)
        return redirect('otp')
    
def login_page(request):
    if request.user.is_superuser:
        return redirect('adminlogin')
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,'customerapp/login-otp.html')


def otp(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,'customerapp/otp.html')


def verify_otp(request):
    obj=OtpGenerate()
    if request.method=='POST':
        re_otp=request.POST.get('otp')
        ge_otp=obj.Otp
        if re_otp==ge_otp:
            user=CustomUser.objects.get(phone=obj.phone)
            if user.is_superuser==False:
                login(request,user)
                return redirect('home')
        else:
            messages.error(request,"Invalid Otp")
            return redirect('otp')
    else:
        messages.error(request,"Invalid Credentials")
        return redirect('otp')
    



    
class OtpGenerate():
    Otp=None
    phone=None

    def send_otp(phone):
        account_sid='AC9315825af374025a0a2827c4d28ddf85'
        auth_token='01d2740881c46c03f2c129903e0d0682'
        target_number = '+91' + phone
        twilio_number='+12134680849'
        otp=random.randint(1000,9999)
        OtpGenerate.Otp=str(otp)
        OtpGenerate.phone=phone
        msg="your otp is " + str(otp)
        client=Client(account_sid,auth_token)
        message=client.messages.create(
        body=msg,
        from_=twilio_number,
        to=target_number
        )
        print(message.body)
        return True



@never_cache
def login_pass(request):
    if request.user.is_superuser:
        return redirect('adminlogin')
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(email=email,password=password)
        
        
        if user is not None and user.blocked==False:

            if user.is_superuser==False:
                try:
                    
                    cart=Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                    
                    if is_cart_item_exists:
                        cart_item=CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user=user
                            item.save()
                except:
                    pass
                if user.is_superuser==False:
                    login(request,user)
                    return redirect('home')
                else:
                    return redirect('adminlogin')
        else:
            messages.info(request,"Phone Number or Password is Incorrect")
            return redirect(login_pass)
    return render(request,'customerapp/login-pass.html')



def add_to_wishlist(request,id):
    product=get_object_or_404(Product,id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request,"Removed "+product.product_name+" from your wishlist")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request,"Added "+product.product_name+" to your wishlist")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def user_wishlist(request):
    products=Product.objects.filter(users_wishlist=request.user)
    return render(request,'customerapp/wishlist.html',{
        'wishlist':products
    })



def my_profile(request):
    return render(request,'customerapp/my_profile.html')
from category.models import Size
def load_size_user(request):
    print("loaded this function................................................................")
    color=request.GET.get('color_id')

    size=Size.objects.filter(color=color).all()
    return render(request,'customerapp/user-size-dropdown.html',{
        'size':size
    })