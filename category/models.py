from django.utils import timezone
from django.conf import settings
from random import choices
from django.db import models
from django.urls import reverse
from django.apps import apps
from django.db.models.aggregates import Sum
# Create your models here.

class Category(models.Model):
    cat_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=200,unique=True)

class Subcategory(models.Model):
    sub_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    parent_cat=models.ForeignKey(Category,on_delete=models.CASCADE)

    def get_url(self):
        return reverse('products_by_subcategory',args=[self.slug])



class Product(models.Model):
    product_name=models.CharField(max_length=500,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    product_desc=models.TextField()
    price=models.FloatField()
    img1=models.ImageField(upload_to='images/product_images',blank=True)
    img2=models.ImageField(upload_to='images/product_images',blank=True)
    img3=models.ImageField(upload_to='images/product_images',blank=True)
    img4=models.ImageField(upload_to='images/product_images',blank=True)
    added_date=models.DateTimeField(auto_now_add=True)
    stock=models.BigIntegerField()
    is_available=models.BooleanField(default=False)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory=models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    users_wishlist=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='users_wishlist',blank=True)
    
    
    def get_url(self):
        return reverse('product_detail',args=[self.subcategory.slug,self.slug])
        
    def __str__(self):
        return self.product_name

    def get_revenue(self,month=timezone.now().month):
        orderitems=apps.get_model("orders",'OrderItem')
        orders=orderitems.objects.filter(product=self,created_at__month=month,status="Delivered")
        return orders.values("product").annotate(revenue=Sum("price"))
    def get_profit(self,month=timezone.now().month):
        orderitems=apps.get_model("orders",'OrderItem')
        orders=orderitems.objects.filter(product=self,created_at__month=month,status="Delivered")
        calculating_profit=orders.values('product').annotate(profit=Sum('price'))
        profit=calculating_profit[0]['profit']*0.23
        return profit
    def get_count(self,month=timezone.now().month):
        orderitems=apps.get_model("orders",'OrderItem')
        orders=orderitems.objects.filter(product=self,created_at__month=month,status="Delivered")
        return orders.values("product").annotate(quantity=Sum("quantity"))

class Banner(models.Model):
    banner_img1=models.ImageField(upload_to='images/banner_images',blank=True)




class Color(models.Model):
    color_value=models.CharField(max_length=50,null=True)
class Size(models.Model):
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size_value=models.CharField(max_length=50,null=True)

class Variations(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE,null=True)
    color=models.ForeignKey(Color,on_delete=models.CASCADE,null=True)