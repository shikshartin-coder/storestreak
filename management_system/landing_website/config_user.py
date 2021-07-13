from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,update_session_auth_hash
import re
import random
import string
from Customer.data_interface import Customer_Interface
from landing_website.constants import CUSTOMER, BUSINESS

login_url = '/customer-login'
logout_url = "/customer-login"

def user_account_login(request,username,raw_password):
    user_auth = authenticate(username=username,password=raw_password)
    if(user_auth != None):
        login(request,user_auth)
        error =  None
    else:
        error =  "User id and password not matched"
    return error

def create_user(username,raw_password):
    try:
        user = User.objects.create_user(username,None,raw_password)
        user_auth = authenticate(username=username,password=raw_password)
        user.save()
    except:
        return None
    return user

def change_password(username, password):
	user = User.objects.get(username = username)
	user.set_password(password)
	user.save()
	return user

def is_validated(password):
	error = ""
	if len(password)<5:
		error = error + "5 characters"
	regex = re.compile(r"[A-Za-z]+")
	if regex.search(password)==None:
		if error!="":
			error = error + ", "
		error = error + "alphabets"
	regex = re.compile(r"[0-9]+")
	if regex.search(password)==None:
		if error!="":
			error = error + ", "
		error = error + "numeric"
	regex = re.compile(r"[@_!#$%^&*()<>?/\\|}{~:]+")
	if regex.search(password)==None:
		if error!="":
			error = error + ", "
		error = error + "special characters"
	if error!="":
		error = "Password should have " + error
	return error

def username_is_unique(username):
	error = ""
	user_list = User.objects.filter(username = username)
	if user_list != []:
		error = "Username already exist"
	return error

def get_user_type(username):
    from Business.data_interface import Business_interface
    check_if_customer = Customer_Interface().check_user_is_customer(username)
    check_if_business = Business_interface().check_user_is_business(username)
    if check_if_customer:
        return CUSTOMER
    elif check_if_business:
        return BUSINESS
    else:
        return None


def view_permission(user_id, user_type):
	from Business.data_interface import Business_interface
	if user_type == CUSTOMER:
		customer_object = Customer_Interface().get_customer_by_user_id(user_id)
		if object == None:
			return False
	else:
		business_object = Business_interface().get_business_by_user_id(user_id)
		if object == None:
			return False
	return True

def idfy(string):
	string = string.lower()
	string = re.sub('[^a-zA-Z0-9 \n\.]', ' ', string)
	string = string .replace(" ", "-")
	return string

def random_letter():
	letter = random.choice(string.ascii_letters)
	letter = letter.lower()
	return letter