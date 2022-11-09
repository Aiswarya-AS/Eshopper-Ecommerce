from django.db import models
from accounts.models import CustomUser
from category.models import Product
from userprofile.models import Address
# Create your models here.


class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    total_price=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=150,null=False)
    payment_id=models.CharField(max_length=250,null=True)

    status=models.CharField(max_length=150,default='Placed')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at_at=models.DateTimeField(auto_now=True)
    


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.FloatField(null=False)
    quantity=models.IntegerField(null=False)
    status=models.CharField(max_length=150,default='Order Placed')
    
    
