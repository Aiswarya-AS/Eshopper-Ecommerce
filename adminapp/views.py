from ast import Sub
from django.shortcuts import render,redirect
from django.contrib import messages
from accounts.models import CustomUser
from category.models import Category, Subcategory,Product
from django.utils.text import slugify
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from orders.models import Order,OrderItem
# Create your views here.

@login_required(login_url='adminlogin')
def admin_home(request):
    if request.user.is_superuser==True:
        return render(request,'adminapp/dashboard.html')


@login_required(login_url='adminlogin')
def show_users(request):
    users=CustomUser.objects.all()
    return render(request,'adminapp/users.html',{
        'users':users
    })


@login_required(login_url='adminlogin')
def category(request):
    cat=Category.objects.all()
    context={
        'categories':cat
    }
    return render(request,'adminapp/category.html',context)



@login_required(login_url='adminlogin')
def subcategory(request):
    sub_category=Subcategory.objects.all()
    context={
        'sub_category':sub_category
    }
    return render(request,'adminapp/subcategory.html',context)

@login_required(login_url='adminlogin')
def products(request):
    products=Product.objects.all()

    return render(request,'adminapp/products.html',{
        'products':products
    })


@login_required(login_url='adminlogin')
def add_category(request):
    if request.method=="POST":
        if request.POST['catname']:
            name=request.POST['catname']
            if Category.objects.filter(cat_name=name).exists():
                messages.error(request,'Category Already Exists!')
                return redirect('category')
            cat=Category()
            cat.cat_name=name
            cat.slug=slugify(name)
            cat.save()
            messages.error(request,'New Category Added')
            return redirect('category')

    return render(request,'adminapp/add-category.html')

def delete_category(request,id):
    de=Category.objects.filter(id=id).delete()
    return redirect('category')

@login_required(login_url='adminlogin')
def edit_category(request,id):
    cat=Category.objects.get(pk=id)
    if request.method=='POST':
        name=request.POST.get('catname')
        cat.cat_name=name
        cat.slug=slugify(name)
        cat.save()
        messages.error(request,"Updated")
        return redirect('category')
    return render(request,'adminapp/edit-category.html',{
        'cat'
    })



@login_required(login_url='adminlogin')
def add_subcategory(request):
    category=Category.objects.all()
    if request.method=='POST':
        cate=request.POST.get('selectcat')
        print(cate)
        sub_name=request.POST.get('subcatname')
        print(sub_name)
        if Subcategory.objects.filter(sub_name=sub_name).exists():
            messages.error(request,'Already Exists')
            return redirect('subcategory')
        else:
            obj=Subcategory()
            obj.sub_name=sub_name
            obj.slug=slugify(sub_name)
            
            obj.parent_cat_id=cate
            obj.save()
            messages.error(request,'SubCategory Created')
            return redirect('subcategory')
    return render(request,'adminapp/add-subcategory.html',{
        'categories':category
    })


def delete_subcategory(request,id):
    Subcategory.objects.filter(id=id).delete()
    return redirect('subcategory')


@login_required(login_url='adminlogin')
def edit_subcategory(request,id):
    category=Category.objects.all()
    sub=Subcategory.objects.get(id=id)
    if request.method=='POST':
        cate=request.POST.get('selectcat')
        sub_name=request.POST.get('subcatname')
        if Subcategory.objects.filter(sub_name=sub_name).exists():
            messages.error(request,'Already Exists')
            return redirect('subcategory')
        else:
            
            sub.sub_name=sub_name
            sub.slug=slugify(sub_name)
            
            sub.parent_cat_id=cate
            sub.save()
            messages.error(request,'SubCategory Created')
            return redirect('subcategory')

    
    return render(request,'adminapp/edit-subcategory.html',{
        'categories':category,'sub':sub
    })


@login_required(login_url='adminlogin')

def add_product(request):
    if request.method=="POST":
        productname=request.POST.get('productname')
        if Product.objects.filter(product_name=productname).exists():
            messages.error(request,'Product Name Already Exists')
            return redirect('products')
        product=Product()
        product.product_name=productname
        product.slug=slugify(productname)
        product.price=request.POST.get('price')
        product.stock=request.POST.get('stock')
        product.product_desc=request.POST.get('productdesc')
        product.subcategory_id=request.POST.get('selectsubcategory')
        
        product.category_id=request.POST.get('selectcategory')

        if 'productimage1' in request.FILES:
            product.img1=request.FILES['productimage1']
        if 'productimage2' in request.FILES:
            product.img2=request.FILES['productimage2']
        if 'productimage3' in request.FILES:
            product.img3=request.FILES['productimage3']
        if 'productimage4' in request.FILES:
            product.img4=request.FILES['productimage4']

        if int(product.stock) < 0:
            product.is_available=False
        else:
            product.is_available=True
        product.save()
        messages.success(request,"New Product Added!")
        return redirect('products')

    return redirect('addingproduct')





def delete_product(request,id):
    Product.objects.get(id=id).delete()
    return redirect('products')


def admin_login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['pass']
        user=authenticate(email=email,password=password)
    
        if user is not None:
            login(request,user)
            print(request.user.is_admin)
            print('??????????????????????????/')
            if request.user.is_admin==True:
                return redirect('admin-home')
            else:
                print("thiwwww")
                messages.error(request,'Invalid credatials')
                return redirect('adminlogin')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('adminlogin')
    return render(request,'adminapp/login.html')

def admin_logout(request):
    logout(request)
    return redirect('adminlogin')


def adding_product(request):
    categories=Category.objects.all()
    subcategories=Subcategory.objects.all()
    context={
        'categories':categories,
        'subcategories':subcategories
    }
    return render(request,'adminapp/add-product.html',context)



def load_subcategory(request,catid):
    subcategory=Subcategory.objects.filter(parent_cat_id=catid)
    print(subcategory)
    context={
        'subcategory':subcategory
    }
    return render(request,'adminapp/dropdown.html',context)

def block_user(request,id):
    user=CustomUser.objects.get(id=id)
    if user.blocked:
        user.blocked=False
        user.save()
        
    else:
        user.blocked=True
        user.save()
    return redirect('users')




def orders(request):
    orders=Order.objects.all()
    order_items=OrderItem.objects.all()
    context={
        'orders':orders,
        'order_items':order_items
    }
    return render(request,'adminapp/orders.html',context)

def order_items(request):
    order_items=OrderItem.objects.all()
    context={
        
        'order_items':order_items
    }
    return render(request,'adminapp/orderitems.html',context)

def order_delete(request):
    pass

def order_item_delete(request):
    pass