from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib import messages
from accounts.models import CustomUser
from category.models import Category, Subcategory,Product
from django.utils.text import slugify
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from orders.models import Order,OrderItem
from django.db.models import Sum
import datetime
from django.db.models import Count,Q
import csv
from django.template.loader import render_to_string

from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.views.generic import View
from django.template.loader import get_template
import xlwt

from offers.forms import CategoryOfferForm,SubcategoryOfferForm,ProductOfferForm,CouponForm
from offers.models import CategoryOffer,SubcategoryOffer,ProductOffer,Coupon
# Create your views here.

@login_required(login_url='adminlogin')
def admin_home(request):
    if request.user.is_superuser==True:
        total_users=CustomUser.objects.filter(is_active=True).count()
        total_products=Product.objects.filter(is_available=True).count()
        total_orders=OrderItem.objects.filter(status='Delivered').count()
        total_revenue=Order.objects.aggregate(Sum('total_price'))
        

        current_year=timezone.now().year
        order_detail=OrderItem.objects.filter(created_at__lt=datetime.date(current_year,12,31),status="Delivered")
        monthly_order_count=[]
        month=timezone.now().month
        for i in range(1,month+2):
            monthly_order = order_detail.filter(created_at__month=i).count()
            monthly_order_count.append(monthly_order)
        

        today=datetime.datetime.now()
        dates=OrderItem.objects.filter(created_at__month=today.month).values('created_at__date').annotate(order_items=Count('id')).order_by('created_at__date')
        returns=OrderItem.objects.filter(created_at__month=today.month).values('created_at__date').annotate(returns=Count('id',filter=Q(status='Cancelled'))).order_by('created_at__date')
        sales=OrderItem.objects.filter(created_at__month=today.month).values('created_at__date').annotate(sales=Count('id',filter=Q(status='Delivered'))).order_by('created_at__date')
        
        most_moving_product_count=[]
        most_moving_product=[]
        
        products=Product.objects.all()
        for i in products:
            most_moving_product.append(i)
            most_moving_product_count.append(
                OrderItem.objects.filter(
                    product=i,status='Delivered'
                ).count()
            )
        
        placed_count=OrderItem.objects.filter(status="Order Placed").count()
        shipped_count=OrderItem.objects.filter(status="Shipped").count()
        delivered_count=OrderItem.objects.filter(status="Delivered").count()
        return_count=OrderItem.objects.filter(status="Refund Initiated").count()
        cancelled_count=OrderItem.objects.filter(status="Cancelled").count()


        print(placed_count,"placed Count")
        print(shipped_count,"shipped Count")
        print(delivered_count,"delivered Count")
        print(return_count,"return Count")
        print(cancelled_count,"cancelled Count")

        
        return render(request,'adminapp/dashboard.html',{
            
            'total_orders':total_orders,
            'total_products':total_products,
            'total_users':total_users,
            'total_revenue':total_revenue,
            "monthly_order_count": monthly_order_count,
            'today':today,
            'sales':sales,
            'returns':returns,
            'dates':dates,
            'most_moving_product':most_moving_product,
            'most_moving_product_count':most_moving_product_count,
            'status_count':[
                placed_count,
                shipped_count,
                delivered_count,
                return_count,
                cancelled_count,
            ]

        })


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
        'cat':cat
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


def edit_product(request,id):
    product=Product.objects.get(id=id)
    if request.method=='POST':
        productname=request.POST.get('productname')
        if Product.objects.filter(product_name=productname).exists():
            messages.error(request,'Product Name Already Exists')
            return redirect('products')
        
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
    
    return render(request,'adminapp/edit-product.html',{
        'product':product
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
    order_items=OrderItem.objects.order_by("-id").all()
    context={
        
        'order_items':order_items
    }
    return render(request,'adminapp/orderitems.html',context)

def variations(request):
    color=Color.objects.all()
    return render(request,'adminapp/variations.html',{
        'color':color
        })


from category.models import Color,Size,Variations
def add_color(request):
    if request.method=='POST':
        color=request.POST.get('color')
        if Color.objects.filter(color_value=color).exists():
            messages.error(request,"already exists")
            return redirect('variations')
        else:
            c=Color()
            c.color_value=color
            c.save()
            messages.success(request,'added new color')
            return redirect('variations')

def add_size(request):
    if request.method=="POST":
        seccolor=request.POST.get('selectcolor')
        
        size=request.POST.get('size')
        
        if Size.objects.filter(color=seccolor,size_value=size).exists():
            messages.error(request,"already exists")
            return redirect('variations')
        else:
            s=Size()
            s.color_id=seccolor
            s.size_value=size
            s.save()
            messages.success(request,'added new size')
    
    
            return redirect('variations')

def add_variations(request,id):
    product=Product.objects.get(id=id)
    print(product,"??????????????????????????????????")
    colors=Color.objects.all()

    if request.method=="POST":
        c=request.POST.get('selectcolor')
        s=request.POST.get('selectsize')
        vari=Variations()
        if variations.objects.get(product=product,color=c,size=s).exists():
            messages.error(request,'Already Exists')
            return redirect('add_variations')
        vari.product_id=product.id
        vari.color_id=c
        vari.size_id=s
        vari.save()
        messages.success(request,'added')
    return render(request,'adminapp/add_variations.html',{
        
        'colors':colors,
        'product':product
    })


def load_size(request):
    color=request.GET.get('color_id')

    size=Size.objects.filter(color=color).all()
    return render(request,'adminapp/sizedropdown.html',{
        'size':size
    })

def product_report(request):
    products=Product.objects.all()
    

    if request.GET.get('from'):
        product_date_from=datetime.datetime.strptime(request.GET.get('from'),"%Y-%m-%d")
        product_date_to=datetime.datetime.strptime(request.GET.get('to'),"%Y-%m-%d")

        product_date_to+=datetime.timedelta(days=1)
        products=Product.objects.filter(added_date__range=[product_date_from,product_date_to])
        print(products,'..............')
    
    
    
        
    return render(request,'adminapp/product_report.html',{
        'products':products,
        
        
    })

def sales_report(request):
    products=Product.objects.all()
    
    order_items=OrderItem.objects.all().order_by('-created_at')

    if request.GET.get('from'):
        sales_date_from=datetime.datetime.strptime(request.GET.get('from'),"%Y-%m-%d")
        sales_date_to=datetime.datetime.strptime(request.GET.get('to'),"%Y-%m-%d")

        sales_date_to+=datetime.timedelta(days=1)
        order_items=OrderItem.objects.filter(created_at__range=[sales_date_from,sales_date_to])
        products=Product.objects.filter(added_date__range=[sales_date_from,sales_date_to])
    return render(request,'adminapp/sales_report.html',{
        'products':products,
        'order_items':order_items
    })


def product_csv(request):
    response=HttpResponse(content_type='text/csv')
    response[
        "Content-Disposition"
    ] = "attachement; filename=Product_Report.csv"

    writer=csv.writer(response)
    writer.writerow(
        [
            "Product Name",
            "Category Name",
            "Subcategory Name",
            "Price"
            "Stock"
        ]
    )
    products=Product.objects.all().order_by('id')
    for p in products:
        writer.writerow(
            [
                p.product_name,
                p.category.cat_name,
                p.subcategory.sub_name,
                p.price,
                p.stock,
            ]
        )
    return response



class generateProductPdf(View):
    def get(self,request,*args,**kwargs):
        try:
            products=Product.objects.all()
            
        except:
            return HttpResponse("505 not found")
        data={
            'products':products
        }
        pdf=render_to_pdf('adminapp/product_pdf.html',data)
        return HttpResponse(pdf,content_type='application/pdf')

def render_to_pdf(template_src,context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

def product_excel(request):
    response=HttpResponse(content_type='application/ms-excel')
    response[
        "Content-Disposition"
    ] = "attachement; filename=Product_Report.xls"
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Product_Data')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True

    columns=[
            "Product Name",
            "Category Name",
            "Subcategory Name",
            "Price"
            "Stock"
    ]

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style=xlwt.XFStyle()
    rows=Product.objects.all().values_list('product_name','category','subcategory','price','stock')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)

    wb.save(response)
    return response



def sales_csv(request):
    response=HttpResponse(content_type='text/csv')
    response[
        "Content-Disposition"
    ] = "attachement; filename=Sales_Report.csv"

    products=Product.objects.all().order_by('-id')
    writer=csv.writer(response)
    writer.writerow(
        [
            "Product Name",
            "Revenue",
            "Sold Count"
            "Profit",
        ]
    )
    for p in products:
        writer.writerow(
            [
                p.product_name,
                p.stock,
                p.get_revenue()[0]["revenue"],
                p.get_count()[0]["quantity"],
                p.get_profit()

            ]
        )
    return response



def sales_excel(request):
    response=HttpResponse(content_type='application/ms-excel')
    response[
        "Content-Disposition"
    ] = "attachement; filename=Sales_Report.xls"
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Product_Data')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True

    columns=[
            "Order ID"
            "Product Name",
            "Price",
            "Quantity",
            "Status"
    ]

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style=xlwt.XFStyle()
    rows=OrderItem.objects.all().values_list('order','product','price','quantity','status')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)

    wb.save(response)
    return response



class generateSalesPdf(View):
    def get(self,request,*args,**kwargs):
        try:
            products=Product.objects.all()
            
        except:
            return HttpResponse("505 not found")
        data={
            'products':products,
            
        }
        pdf=render_to_pdf('adminapp/sales_pdf.html',data)
        return HttpResponse(pdf,content_type='application/pdf')

def category_offer(request):
    cat_offer=CategoryOffer.objects.all()
    return render(request,'adminapp/category_offer.html',{
        'cat_offer':cat_offer
    })

def subcategory_offer(request):
    sub_offer=SubcategoryOffer.objects.all()
    return render(request,'adminapp/subcategory_offer.html',{
        'sub_offer':sub_offer
    })

def product_offer(request):
    product_offer=ProductOffer.objects.all()
    return render(request,'adminapp/product_offer.html',{
        'product_offer':product_offer
    })


def add_category_offer(request):
    form=CategoryOfferForm()
    if request.method=='POST':
        form=CategoryOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_offer')
    context={
        'form':form
    }
    return render(request,'adminapp/add_category_offer.html',context)

def add_subcategory_offer(request):
    form=SubcategoryOfferForm()
    if request.method=='POST':
        form=SubcategoryOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subcategory_offer')
    context={
        'form':form
    }
    return render(request,'adminapp/add_subcategory_offer.html',context)

def add_product_offer(request):
    form=ProductOfferForm()
    if request.method=='POST':
        form=ProductOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_offer')
    context={
        'form':form
    }
    return render(request,'adminapp/add_product_offer.html',context)




def edit_category_offer(request):
    pass

def edit_subcategory_offer(request):
    pass
def edit_product_offer(request):
    pass

def delete_category_offer(request):
    pass

def delete_subcategory_offer(request):
    pass

def delete_product_offer(request):
    pass

def coupons(request):
    coupons=Coupon.objects.all()
    return render(request,'adminapp/coupons.html',{
        'coupons':coupons
    })


def add_coupons(request):
    form=CouponForm()
    if request.method=='POST':
        form=CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupons')
    else:
        print('error')
    
    return render(request,'adminapp/add_coupons.html',{
        'form':form
    })




def salesReport(request):
    orders=Order.objects.all()
    new_order_list=[]

    for i in orders:
        order_items=OrderItem.objects.filter(order_id=i.id)
        for j in order_items:
            item={
                'id':i.id,
                'ordered_date':i.created_at,
                'user':i.user,
                'price':j.price,
                'method':i.payment_mode,
                'status':j.status,


            }
            new_order_list.append(item)
        
    return render(request,'adminapp/salesReport.html',{
        'order':new_order_list,
    })

def by_date(request):
    if request.GET.get('from'):
        sales_date_from=datetime.datetime.strptime(request.GET.get('from'),"%Y-%m-%d")
        sales_date_to=datetime.datetime.strptime(request.GET.get('to'),"%Y-%m-%d")

        sales_date_to+=datetime.timedelta(days=1)
        orders=Order.objects.filter(created_at__range=[sales_date_from,sales_date_to])

    new_order_list=[]

    for i in orders:
        order_items=OrderItem.objects.filter(order_id=i.id)
        for j in order_items:
            item={
                'id':i.id,
                'ordered_date':i.created_at,
                'user':i.user,
                'price':j.price,
                'method':i.payment_mode,
                'status':j.status,


            }
            new_order_list.append(item)
        
    return render(request,'adminapp/salesReport.html',{
        'order':new_order_list,
    })

class generatesalesReportPdf(View):
    def get(self,request,*args,**kwargs):
        try:
            orders=Order.objects.all()
            new_order_list=[]

            for i in orders:
                order_items=OrderItem.objects.filter(order_id=i.id)
                for j in order_items:
                    item={
                        'id':i.id,
                        'ordered_date':i.created_at,
                        'user':i.user,
                        'price':j.price,
                        'method':i.payment_mode,
                        'status':j.status,


                    }
                    new_order_list.append(item)
                    
        except:
            return HttpResponse("505 not found")
        data={
            'order':new_order_list
        }
        pdf=render_to_pdf('adminapp/salesReport_pdf.html',data)
        return HttpResponse(pdf,content_type='application/pdf')


#coupon django ?




