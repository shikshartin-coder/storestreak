from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Business(models.Model):
    Business_name = models.CharField(blank=False,null=True,max_length=100)
    business_key = models.CharField(blank=False,null=True,max_length=100)
    name = models.CharField(blank=False,null=True,max_length=100)   
    category = models.CharField(blank=False, null=True, max_length=100)
    dp_image = models.ImageField(upload_to='./static/media', blank=True, null=True)
    cover_image = models.ImageField(upload_to='./static/media', blank=True, null=True)
    mobile = models.CharField(blank=False,null=True,max_length=100)
    payment_choice = models.CharField(blank=False,null=True,max_length=100)
    delivery_charge = models.IntegerField(default=0)
    minimum_delivery_amount = models.IntegerField(default=0)
    delivery_type = models.CharField(default='free',max_length=100)
    user = models.IntegerField(null=True)

class Category(models.Model):
    name = models.CharField(blank=False,null=True,max_length=100)
    image = models.ImageField(upload_to='./static/media', blank=True, null=True)
    status = models.BooleanField(blank=False,null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.IntegerField(null=True)

class Product(models.Model):
    name = models.CharField(blank=False,null=True,max_length=100)
    category_id = models.IntegerField(null=True)
    status = models.BooleanField(blank=False,null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.IntegerField(null=True)

class Product_type(models.Model):
    product_type_key = models.CharField(blank=False,null=True,max_length=100)
    product_id =  models.IntegerField(null=True)
    name = models.CharField(blank=False,null=True,max_length=100)
    image = models.ImageField(upload_to='./static/media', blank=True, null=True)
    content = models.CharField(blank=False,null=True,max_length=1000)
    stock = models.IntegerField(blank=False,null=True)
    cost = models.IntegerField(blank=False)
    mrp = models.IntegerField(blank=False,null=True)
    pack_size = models.CharField(blank=False,null=True,max_length=100)
    unit = models.CharField(blank=False,null=True,max_length=100)
    status = models.BooleanField(blank=False,null=False)
    user = models.IntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
