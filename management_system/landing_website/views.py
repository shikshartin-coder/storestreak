from django.shortcuts import render,redirect
from . import mobile_verfication as number_verification
from . import config_user
from . import address 
from django.http import JsonResponse
from .data_interface import OneTimePasswordInterface, UserInterface
from landing_website.mobile_verfication import mobile_verification, otp_submission
from django.contrib.auth import update_session_auth_hash
from Business.data_interface import Product_type_interface, Business_interface
from .search import search_pattern
from django.core import serializers
from landing_website import helper
from django.contrib.auth.decorators import login_required


def not_found_view(request,exception=True):
    return render(request,'./landing_website/404.html',{})

def error_view(request,exception=True):
    return render(request,'./landing_website/500.html',{})


# Create your views here.

def homepage(request):
    if(request.method == "POST"):
        name = request.POST.get('name')
    return render(request,'./landing_website/homepage.html',{})


def forgot_password(request):
    context = {
        'page':'forgot_password'
    }
    if request.method == 'POST':
        btn = request.POST.get('btn')
        mobile_number = request.POST.get('mobile_number')
        if btn == "mobile_number_submit" or btn == "otp_resend":
            returned_dict = mobile_verification(request)
            if returned_dict['otp_id']:
                context = {
                    'page':'forgot_password',
                    'mobile_number':mobile_number,
                    "otp_id":returned_dict['otp_id'],
                }
                return render(request,'./landing_website/otp_verification.html',context)
            else:
                user_type = config_user.get_user_type(mobile_number)
                context = {
                    'page':'forgot_password',
                    'error': returned_dict['error'],
                    'user_type': user_type
                }
                return render(request, './landing_website/mobile_verification.html', context)

        elif btn == 'otp_submit':
            error = otp_submission(request)
            if error:
                context = {
                    'error':"Invalid OTP",
                    'page':'forgot_password',
                }
                return render(request,'./landing_website/mobile_verification.html' ,context) 
            else:
                context = {
                    'mobile_number' : mobile_number,
                }
                return render(request, './landing_website/reset_password.html',context)

        else:
            password_mode = request.POST.get('password_mode')
            password = request.POST.get('password')

            if password_mode == "validation":
                error = config_user.is_validated(password)
                return JsonResponse({'error':error})

            if password_mode == "change_password":
                username = mobile_number
                user = config_user.change_password(username, password)
                user_type = config_user.get_user_type(username)
                return render(request, './landing_website/reset_password_success.html', {'user_type':user_type})
            
    return render(request, './landing_website/mobile_verification.html',context)

def change_password(request, message = None):
    user = request.user
    username = user.username
    user_type = config_user.get_user_type(username)
    if user_type == None:
        return not_found_view(request)
    path_to_user_base = "./"+user_type+"/base.html"
    print(path_to_user_base)
    context = {
        'url_path':'change-password',
        'path_to_user_base':path_to_user_base,
        'message':message,
    }
    if request.method == 'POST':
        password_mode = request.POST.get('password_mode')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('password')

        if password_mode == 'validation':
            error = config_user.is_validated(new_password)
            return JsonResponse({'error':error})

        if password_mode == 'change_password':
            is_old_password_valid = user.check_password(old_password)
            if is_old_password_valid:
                user = config_user.change_password(username, new_password)
                update_session_auth_hash(request, user)
                message_var = 'Password Change Success'
            else:
                message_var = 'Old Password Incorrect'
            print(message_var)
            return redirect(change_password, message = message_var)
    if message == None:
        return redirect(change_password, message='change')
    return render(request,'./landing_website/change_password.html',context)


def add_address_view(request, id):
    return address.add_address(request, id)


@login_required(login_url=config_user.login_url)
def address_list_view(request):
    return address.address_list(request)

def contact(request):
    return render(request,'./landing_website/contact.html',{})

def about(request):
    return render(request,'./landing_website/about.html',{})

def search(request):
    search_query = request.GET['search_query']
    product_type_all_list = Product_type_interface().get_all_product_type()
    product_type_list_processed = helper.process_product_type_list_for_dict(product_type_all_list)
    business_list = Business_interface().get_business()
    business_list_processed = helper.process_business_list_for_dict(business_list)
    product_type_list_processed.extend(business_list_processed)
    product_type_search_list = search_pattern(search_query, product_type_list_processed)
    return JsonResponse({'search_list': product_type_search_list})
