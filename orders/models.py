from django.db import models
from accounts.models import CustomUser
from category.models import Product
from userprofile.models import Address

from django.urls import reverse
from django.apps import apps
from django.db.models.aggregates import Sum
from django.utils import timezone
# Create your models here.


class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,null=True,on_delete=models.SET_NULL)
    total_price=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=150,null=False)
    payment_id=models.CharField(max_length=250,null=True)
    status=models.CharField(max_length=150,default='Placed')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at_at=models.DateTimeField(auto_now=True)
    


class OrderItem(models.Model):
    order=models.ForeignKey(Order,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    price=models.FloatField(null=False)
    quantity=models.IntegerField(null=False)
    status=models.CharField(max_length=150,default='Order Placed')
    created_at=models.DateTimeField(auto_now_add=True)
    
    