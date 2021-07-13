from .data_interface import Business_interface
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,update_session_auth_hash
from django.contrib.auth.hashers import make_password
from landing_website import config_user



login_url = '/business-login'
logout_url = "/business-login"
BUSINESS = "business"

def create_business(name,business_name,category,mobile,username,raw_password):
    error = None
    user =  config_user.create_user(username,raw_password)
    if(user != None):
        business_key = Business_interface().create_business_key(business_name)
        business = Business_interface().create_business(business_name,business_key,name,category,mobile,user.id)
        if(business != None):
            returned_dict = {'user':user,'business':business,'error':error}
            return returned_dict
        else:
            error = "business is not created"
    else:
        error = "user is not created"
    return {'error':error}



def mobile_is_unique(mobile):
    error = ""
    mobile_list = Business_interface().get_business_mobile(mobile)
    if mobile_list != []:
        error = "Mobile number already registered"
    return error