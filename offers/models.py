from django.db import models
from category.models import Category,Subcategory,Product
# Create your models here.
class CategoryOffer(models.Model):
    category_name=models.OneToOneField(Category,on_delete=models.CASCADE)
    discount=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_valid=models.BooleanField(default=True)

class SubcategoryOffer(models.Model):
    subcategory_name=models.OneToOneField(Subcategory,on_delete=models.CASCADE)
    discount=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_valid=models.BooleanField(default=True)

class ProductOffer(models.Model):
    product_name=models.OneToOneField(Product,on_delete=models.CASCADE)
    discount=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_valid=models.BooleanField(default=True)

class Coupon(models.Model):
    code=models.CharField(max_length=200)
    discount=models.IntegerField()
    valid_from=models.DateField()
    valid_to=models.DateTimeField()
    min_amount=models.IntegerField(default=0)
    is_valid=models.BooleanField(default=True)
