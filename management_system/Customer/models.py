from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    name = models.CharField(blank=False, null=True, max_length=100)
    address = models.CharField(blank=False, null=True, max_length=500)
    mobile = models.CharField(blank=False, null=True, max_length=100)
    user = models.IntegerField(null=True)
    privacy_settings = models.BooleanField(default=False)

class Subscribe(models.Model):
    customer_id = models.IntegerField(null=True)
    business_id = models.IntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class Cart(models.Model):
    product_type_id = models.IntegerField(null=True)
    business_id = models.IntegerField(null=True)
    customer_id = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)
    total_price = models.IntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class Orders(models.Model):
    order_id = models.IntegerField(null=True)
    business_id = models.IntegerField(null=True)
    customer_id = models.IntegerField(null=True)
    address_id = models.IntegerField(null=True)
    active = models.BooleanField(null=True)
    order_otp =  models.IntegerField(null=True)
    delivery_charge = models.IntegerField(null=True)
    total_order_amount = models.IntegerField(null=True)
    payment = models.BooleanField(default=False)
    payment_mode = models.CharField(null=True, max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class Order_products(models.Model):
    order_id = models.IntegerField(null=True)
    product_type_id = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)
    total_price = models.IntegerField(null=True)

class Orders_status(models.Model):
    order_id = models.IntegerField(null=True)
    status = models.CharField(blank=False, null=True, max_length=100)
    reason = models.CharField(blank=False, null=True, max_length=1000)
    active = models.BooleanField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class Order_Address(models.Model):
    order_id = models.IntegerField(null=True)
    user_id = models.CharField(max_length = 20,null=True)
    name =  models.CharField(blank=False,null=True,max_length=100)
    mobile = models.CharField(max_length = 20,null=True)
    pincode = models.IntegerField(null=True)
    building =  models.CharField(blank=False,null=True,max_length=100)
    street =  models.CharField(blank=False,null=True,max_length=100)
    landmark =  models.CharField(blank=False,null=True,max_length=100)
    city =  models.CharField(blank=False,null=True,max_length=100)
    state = models.CharField(blank=False,null=True,max_length=100)
    address_type = models.CharField(blank=False,null=True,max_length=100)
    default = models.IntegerField(null=True)

class transaction(models.Model):
    order_id = models.IntegerField(null=True)
    txnid = models.CharField(blank=False,null=True,max_length=100)
    txnamount = models.CharField(blank=False,null=True,max_length=100)
    paymentmode = models.CharField(blank=False,null=True,max_length=100)
    currency = models.CharField(blank=False,null=True,max_length=100)
    txndate = models.CharField(blank=False,null=True,max_length=100)
    status = models.CharField(blank=False,null=True,max_length=100)
    respcode = models.CharField(blank=False,null=True,max_length=100)
    respmsg = models.CharField(blank=False,null=True,max_length=1000)
    gatewayname = models.CharField(blank=False,null=True,max_length=100)
    banktxnid = models.CharField(blank=False,null=True,max_length=100)
    bankname = models.CharField(blank=False,null=True,max_length=100)
    checksumhash = models.CharField(blank=False,null=True,max_length=1000)

