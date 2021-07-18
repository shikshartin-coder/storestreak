from . import config_account
from landing_website import config_user
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required, permission_required
from . import catalogue
from . import subscribe as subscribe_file
from . import cart
from . import orders
from .config_account import login_url
from django.http import JsonResponse
from landing_website.mobile_verfication import mobile_verification, otp_submission, create_one_time_password_with_details
from landing_website.constants import BUSINESS, CUSTOMER
from .data_interface import Subscribe_Interface
from Business.data_interface import Business_interface
from .data_interface import Customer_Interface
from landing_website import views as landing_view
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def login_submit_customer(request, page, hidden_val, context):
    username = request.POST.get('mobile_number')
    password = request.POST.get('password')

    user_exist = Customer_Interface().check_user_is_customer(username)

    if user_exist == False:
        context.update({'error': 'Not a Customer'})
        return render(request, './customer/login.html', context)

    error = config_user.user_account_login(request, username, password)
    if(error == None):
        if hidden_val == 'subscribe':
            return redirect(subscribe, business_key=context['business_key'], action=hidden_val)
        elif hidden_val == 'homepage':
            return redirect(homepage)
        elif hidden_val == 'buy_now':
            return redirect(product, business_key=context['business_key'], product_key=context['product_key'])
        elif hidden_val == 'cart' or hidden_val == 'cart_product_page':
            cart.add_to_cart_authentication_required(
                username, business_key=context['business_key'], product_key=context['product_key'], quantity=quantity)
            if hidden_val == 'cart':
                return redirect(catalog, business_key=context['business_key'])
            else:
                return redirect(product, business_key=context['business_key'], product_key=context['product_key'])
    else:
        context.update({'error': error})
        return render(request, './customer/login.html', context)


def login_view(request, return_link=None):
    error = None
    context = {
        'error': error,
        'page': 'outside'
    }
    if(request.method == "POST"):
        btn = request.POST.get('btn')
        if(btn == 'login_submit'):
            return login_submit_customer(request, 'outside', 'homepage', context)
    return render(request, './customer/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(config_account.logout_url)


def customer_signup(request):
    context = {
        'page': 'customer'
    }
    error = None
    if(request.method == "POST"):
        btn = request.POST.get('btn')
        mobile_number = request.POST.get('mobile_number')
        if btn == "mobile_number_submit" or btn == "otp_resend":
            returned_dict = mobile_verification(request)
            if returned_dict['otp_id']:
                context = {
                    'page': 'customer',
                    'mobile_number': mobile_number,
                    'otp_id': returned_dict['otp_id'],
                }
                return render(request, './landing_website/otp_verification.html', context)
            else:
                user_type = config_user.get_user_type(mobile_number)
                context = {
                    'page': 'customer',
                    'error': returned_dict['error'],
                    'user_type': user_type
                }
                return render(request, './landing_website/mobile_verification.html', context)
        elif btn == 'otp_submit':
            error = otp_submission(request)
            if error:
                context = {
                    'error': "Invalid OTP",
                    'page': 'customer',
                }
                return render(request, './landing_website/mobile_verification.html', context)
            else:
                context = {
                    'mobile_number': mobile_number,
                }
                return render(request, './customer/customer_signup.html', context)
        else:
            password_mode = request.POST.get('password_mode')
            raw_password = request.POST.get('password')

            if(password_mode == "validation"):
                error = config_user.is_validated(raw_password)
                return JsonResponse({'error': error})

            if(password_mode == "signup"):
                customer_name = request.POST.get('customer_name')
                mobile = mobile_number
                username = mobile_number
                customer_account = config_account.create_customer(
                    customer_name, mobile, username, raw_password)

                if(customer_account['error'] == None):
                    login(request, customer_account['user'])
                    return redirect(homepage)
                else:
                    error = 'Something went wrong user not created please.Please signup again'
            context = {
                'mobile_number': mobile_number,
                'error': error,
            }
    # else:
        # return redirect(views.homepage)
    return render(request, './landing_website/mobile_verification.html', context)


def inside_signup(request):
    if(request.method == "POST"):
        btn = request.POST.get('btn')
        mobile_number = request.POST.get('mobile_number')
        user_type = config_user.get_user_type(mobile_number)
        business_key = request.POST.get('business_key')
        product_key = request.POST.get('product_key')
        hidden_val = request.POST.get('hidden_btn')
        quantity = request.POST.get('quantity', 0)

        context = {
            'error': None,
            'page': 'inside',
            'business_key': business_key,
            'hidden_val':  hidden_val,
            'mobile_number': mobile_number,
            'product_key': product_key,
            'quantity': quantity,
        }

        if user_type == CUSTOMER:
            if btn == 'subscribe':
                context.update({
                    'hidden_val': 'subscribe',
                })
            if btn == 'buy_now':
                context.update({
                    'hidden_val': 'buy_now',
                })
            if btn == 'cart':
                context.update({
                    'hidden_val': 'cart',
                })
            if btn == 'cart_product_page':
                context.update({
                    'hidden_val':'cart_product_page',
                })
            if btn == 'login_submit':
                return login_submit_customer(request, 'inside', hidden_val, context)

            return render(request, './customer/login.html', context)

        elif user_type == None:
            if btn == 'subscribe' or btn == 'otp_resend' or btn == 'mobile_number_submit' or btn == 'buy_now' or btn == 'cart' or btn == 'cart_product_page':
                returned_dict = {
                    'otp_id': None,
                    'error': None,
                }
                create_one_time_password_with_details(
                    mobile_number, returned_dict)
                if returned_dict['otp_id']:
                    context.update({
                        'otp_id': returned_dict['otp_id'],
                    })
                    if btn == 'subscribe':
                        context.update({
                            'hidden_val': 'subscribe',
                        })
                    if btn == 'buy_now':
                        context.update({
                            'hidden_val': 'buy_now',
                        })
                    if btn == 'cart':
                        context.update({
                            'hidden_val': 'cart',
                        })
                    if btn == 'cart_product_page':
                        context.update({
                            'hidden_val':'cart_product_page',
                        })
                    return render(request, './landing_website/otp_verification.html', context)
            elif btn == 'otp_submit':
                error = otp_submission(request)
                if error:
                    context.update({
                        'error': 'OTP Invalid',
                    })
                    return render(request, './landing_website/mobile_verification.html', context)
                else:
                    context.update({
                        'mobile_number': mobile_number
                    })
                return render(request, './customer/customer_signup.html', context)
            else:
                password_mode = request.POST.get('password_mode')
                raw_password = request.POST.get('password')

                if(password_mode == "validation"):
                    error = config_user.is_validated(raw_password)
                    return JsonResponse({'error': error})

                if(password_mode == "signup"):
                    customer_name = request.POST.get('customer_name')
                    mobile = mobile_number
                    username = mobile_number
                    customer_account = config_account.create_customer(
                        customer_name, mobile, username, raw_password)

                    if(customer_account['error'] == None):
                        login(request, customer_account['user'])
                        if hidden_val == 'subscribe':
                            return redirect(subscribe, business_key=business_key, action=hidden_val)
                        elif hidden_val == 'buy_now':
                            return redirect(product, business_key=business_key, product_key=product_key)
                        elif hidden_val == 'cart' or hidden_val == 'cart_product_page':
                            cart.add_to_cart_authentication_required(
                                username, business_key, product_key, quantity = 1)
                            if hidden_val == 'cart':
                                return redirect(catalog, business_key)
                            else:
                                return redirect(product, business_key=business_key, product_key=product_key)
                        else:
                            return redirect(homepage)
                    else:
                        context.update({
                            'error': "Something went wrong. Please Signup again!",
                        })
                        return render(request, './landing_website/mobile_verification.html', context)
        elif user_type == BUSINESS:
                context.update({
                    'error': 'Sorry this number is already registered with business account. We cannot allow customer signup or login with this number.'
                })
                return render(request, './landing_website/mobile_verification.html', context)
    return redirect(homepage)


def homepage(request):
    user_type = config_user.get_user_type(request.user.username)
    if user_type == BUSINESS:
        logout(request)
        return redirect(homepage)
    try:
        subscribe_business_list = subscribe_file.get_all_subscribe_list(
            request.user.id)
    except:
        subscribe_business_list = []

    try:
        unsubscribed_business_list = subscribe_file.get_unsubscribed_list(
            request.user.id)
    except:
        unsubscribed_business_list = subscribe_file.get_all_business()
    context = {
        'subscribe_business_list': subscribe_business_list,
        'all_business': unsubscribed_business_list,

    }
    return render(request, './customer/catalogue/customer_homepage.html', context)


def catalog(request, business_key):
    return catalogue.catalog_access_check(request,business_key)

def product(request, business_key, product_key):
    return catalogue.product_access_check(request,business_key, product_key)


@login_required(login_url=config_account.login_url)
def subscribe(request, business_key, action):
    user_type = config_user.get_user_type(request.user.username)
    if user_type == BUSINESS:
        logout(request)
        return redirect(homepage)
    if user_type == None:
        return redirect(homepage)

    return subscribe_file.subscribe_view(request, business_key, action)


@login_required(login_url=config_account.login_url)
def cart_view(request, business_key):
    user_type = config_user.get_user_type(request.user.username)
    if user_type == BUSINESS:
        logout(request)
        return redirect(homepage)
    if user_type == None:
        return redirect(homepage)
    return cart.product_cart(request, business_key)


@login_required(login_url=config_account.login_url)
def confirm_order(request):
    if(request.method == 'GET'):
        buy_mode = request.GET.get('buy_mode')
        if(buy_mode == 'normal_buy'):
            return orders.confirm_order_view(request)
        if(buy_mode == 'cart_buy'):
            return orders.confirm_order_cart(request)
    return landing_view.not_found_view(request,True)

@login_required(login_url=config_account.login_url)
def payment_view(request):
    return orders.payment(request)

@login_required(login_url=config_account.login_url)
def order_view(request):
    user_type = config_user.get_user_type(request.user.username)
    if user_type == BUSINESS:
        logout(request)
        return redirect(homepage)
    if user_type == None:
        return redirect(homepage)
    return orders.view_orders(request)


@login_required(login_url=config_account.login_url)
def customer_order_page(request, order_id):
    user_type = config_user.get_user_type(request.user.username)
    if user_type == BUSINESS:
        logout(request)
        return redirect(homepage)
    if user_type == None:
        return redirect(homepage)

    return orders.customer_order_page(request, order_id)


@csrf_exempt
def handelpayment(request):
    return orders.handel_payment_request(request)


@login_required(login_url=config_account.login_url)
def success(request,orderid):
    return orders.order_placed_success(request,orderid)



@login_required(login_url=config_account.login_url)
def failure(request,orderid):
    return orders.order_placed_failure(request,orderid)

@login_required(login_url=config_account.login_url)
def customer_settings(request):
    customer_object = Customer_Interface().get_customer_by_user_id(request.user.id)
    context = {
        'privacy_settings':customer_object.privacy_settings,
    }
    if request.method == 'POST':
        privacy_settings = request.POST.get('privacy_settings')
        print(privacy_settings)
        if privacy_settings == 'show':
            Customer_Interface().update_privacy_settings(request.user.id, False)
        if privacy_settings == 'hide':
            Customer_Interface().update_privacy_settings(request.user.id, True)
        return redirect(customer_settings)
    return render(request, './customer/customer_settings.html',context)


@login_required(login_url=config_account.login_url)
def subscribed_businesses(request):
    return subscribe_file.fetch_subscribed_businesses_list(request)
