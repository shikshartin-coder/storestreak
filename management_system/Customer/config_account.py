from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,update_session_auth_hash
from .data_interface import Customer_Interface
from django.contrib.auth.hashers import make_password
from landing_website import config_user

login_url = '/customer-login'
logout_url = "/customer-login"
CUSTOMER = "customer"


def create_customer(customer_name,mobile,username,raw_password):
    error = None
    user =  config_user.create_user(username,raw_password)
    if(user != None):
        customer = Customer_Interface().create_customer(new_customer_name= customer_name, new_mobile = mobile, new_user_id = user.id)
        if(customer != None):
            returned_dict = {'user':user,'customer':customer,'error':error}
            return returned_dict
        else:
            error = "customer is not created"
    else:
        error = "user is not created"
    return {'error':error}


