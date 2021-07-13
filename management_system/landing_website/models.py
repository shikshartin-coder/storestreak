from django.db import models

# Create your models here.


class OneTimePassword(models.Model):
    mobile = models.CharField(blank=False,null=True,max_length=100)
    otp = models.CharField(blank=False,null=True,max_length=100)
    status = models.IntegerField(null=True)
    last_change_date_time = models.DateTimeField(auto_now_add=True,null=True)


class Address(models.Model):
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

