import random
from .models import OneTimePassword
from django.core.exceptions import ObjectDoesNotExist
from Customer.data_interface import Customer_Interface
from Business.data_interface import Business_interface
from landing_website.data_interface import UserInterface
from .data_interface import OneTimePasswordInterface
from .constants import MOBILE_EXIST_ERROR, MOBILE_NOT_VALID_ERROR, MOBILE_NOT_EXIST_ERROR
from mobile_otp.views import send_sms

def mobile_verification(request):
    mobile_number = request.POST.get('mobile_number')
    page = request.POST.get('page')
    returned_dict = generate_otp(mobile_number, page)
    return returned_dict

def otp_submission(request):
    otp = request.POST.get('otp')
    mobile_number = request.POST.get('mobile_number')
    otp_id = request.POST.get('otp_id')
    error = OneTimePasswordInterface().verify_otp(otp,mobile_number,otp_id)
    return error

def generate_otp(mobile, page):
    returned_dict = {
        'otp_id': None,
        'error': None
    }
    validation = validate_mobile_number(mobile, returned_dict)

    if validation:
        mobile_exist = check_mobile_present(mobile, returned_dict, page)
        if (not(mobile_exist) and page != 'forgot_password') or (page == 'forgot_password' and mobile_exist):
            create_one_time_password_with_details(mobile, returned_dict)

    return returned_dict

def validate_mobile_number(mobile, returned_dict):
    error = returned_dict['error']
    if(len(mobile)!=10):
        error = MOBILE_NOT_VALID_ERROR
        returned_dict['error'] = error
        return False
    try:
        mobile_int = int(mobile)
    except ValueError:
        error = MOBILE_NOT_VALID_ERROR
    returned_dict['error'] = error

    if error == None:
        return True
    else:
        return False

def check_mobile_present(mobile, returned_dict, page):
    user_list = UserInterface().get_for_username(mobile)
    customer_list = Customer_Interface().get_customer_for_mobile(mobile)
    business_list = Business_interface().get_business_mobile(mobile)

    if len(user_list) > 0 or len(customer_list) > 0 or len(business_list) > 0:
        if page != 'forgot_password':
            returned_dict['error'] = MOBILE_EXIST_ERROR
        return True

    else:
        if page == 'forgot_password':
            returned_dict['error'] = MOBILE_NOT_EXIST_ERROR
        return False


def create_one_time_password_with_details(mobile, returned_dict):
    otp = random.randint(100001,999999)
    OneTimePasswordInterface().disable_all_active_otp_for_mobile(mobile)
    otp_obj = OneTimePasswordInterface().create_one_time_password(mobile = mobile, otp = otp, status = 1)
    if otp_obj == None:
        returned_dict['error'] = "Database Error"
    elif not(returned_dict['error']):
        otp_id = otp_obj.id
        to_be_send = "Your OTP id for verification is "+ str(otp)
        send_sms(to_be_send, mobile)
        returned_dict['otp_id'] = otp_id