from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from landing_website import views
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from . import config_account
from .data_interface import Business_interface, Category_interface, Product_interface, Product_type_interface
from django.contrib.auth.decorators import login_required, permission_required
from landing_website import config_user
from . import inventory
from . import business_settings
from . import manage_order
from . import profile
from django.http import JsonResponse
from landing_website.mobile_verfication import mobile_verification, otp_submission
from . import subscriber
from . import report_helper

# Create your views here.


def login_view(request):
    error = None
    context = {
        'error': error,
    }
    if(request.method == "POST"):
        btn = request.POST.get('btn')
        if(btn == 'login_submit'):
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_exist = Business_interface().check_user_is_business(username)
            if user_exist == False:
                return render(request, './business/login.html', {'error': "Not a Business Account"})
            error = config_user.user_account_login(request, username, password)
            if(error == None):
                return redirect(manage_orders)
            else:
                context = {
                    'error': error,
                    'username': username,
                }
    return render(request, './business/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(config_account.logout_url)


def business_signup(request):
    context = {
        'page': 'business'
    }
    if(request.method == "POST"):
        btn = request.POST.get('btn')
        mobile_number = request.POST.get('mobile_number')
        if btn == "mobile_number_submit" or btn == "otp_resend":
            returned_dict = mobile_verification(request)
            if returned_dict['otp_id']:
                context = {
                    'page': 'business',
                    'mobile_number': mobile_number,
                    "otp_id": returned_dict['otp_id'],
                }
                return render(request, './landing_website/otp_verification.html', context)
            else:
                user_type = config_user.get_user_type(mobile_number)
                context = {
                    'page': 'business',
                    'error': returned_dict['error'],
                    'user_type': user_type
                }
                return render(request, './landing_website/mobile_verification.html', context)

        elif btn == 'otp_submit':
            error = otp_submission(request)
            if error:
                context = {
                    'error': "Invalid OTP",
                    'page': 'business',
                }
                return render(request, './landing_website/mobile_verification.html', context)
            else:
                context = {
                    'mobile_number': mobile_number,
                    'category_list': Business_interface().get_category_list()
                }
                return render(request, './business/signup.html', context)
        else:
            password_mode = request.POST.get('password_mode')
            raw_password = request.POST.get('password')

            if(password_mode == "validation"):
                error = config_user.is_validated(raw_password)
                return JsonResponse({'error': error})

            if(password_mode == "signup"):
                name = request.POST.get('personal_name')
                business_name = request.POST.get('business_name')
                category = request.POST.get('business_category')
                mobile = mobile_number
                username = mobile_number
                business_account = config_account.create_business(
                    name, business_name, category, mobile, username, raw_password)

                if(business_account['error'] == None):
                    login(request, business_account['user'])
                    return redirect(manage_orders)
                else:
                    error = 'Something went wrong user not created please.Please signup again'
            context = {
                'mobile_number': mobile_number,
                'error': error,
            }
    # else:
        # return redirect(views.homepage)
    return render(request, './landing_website/mobile_verification.html', context)


@login_required(login_url=config_account.login_url)
def inventory_view(request, part=None):
    page = 'inventory'
    category_list = Category_interface().get_category(request.user.id)

    product_list = Product_interface().get_product(request.user.id)
    product_type_list = Product_type_interface().get_product_type(request)
    all_category = {}
    for category in category_list:
        product_type_obj = []
        products = Product_interface().get_product_by_category_id(category.id)
        for prod in products:
            product_type_obj = product_type_obj + list(Product_type_interface().get_all_product_type_by_product_id(prod.id))
        non_zero_list = True
        if(len(product_type_obj) == 0):
            non_zero_list = False
        if(non_zero_list):
            all_category.update({category: product_type_obj})

    if(request.method == 'POST'):
        btn = request.POST.get('btn')
        product_type_id = request.POST.get('product_type_id')
        if(btn == 'change_stock'):
            stock = request.POST.get('stock')
            Product_type_interface().change_stock(product_type_id, stock)
            return redirect(inventory_view)

        if(btn == 'out_of_stock'):
            Product_type_interface().change_stock(product_type_id, 0)
            return redirect(inventory_view)

        if(btn == 'active'):
            Product_type_interface().change_status(product_type_id, False)
            return redirect(inventory_view)

        if(btn == 'deactive'):
            Product_type_interface().change_status(product_type_id, True)
            return redirect(inventory_view)

    context = {
        'all_category': all_category,
        'product_list': product_list,
        'product_type_list': product_type_list,
        'page': page,
        'search_page': 'inventory',
    }
    if(part == None):
        return render(request, './business/Inventory/business_inventory.html', context)

    if(part == "category"):
        return inventory.category_view(request, page)

    if(part == "add-category"):
        return inventory.add_category(request, page)

    if(part == "add-product"):
        return inventory.add_product(request, page)

    if(part == "grouped"):
        return inventory.product_view(request, page)

    return render(request, './business/Inventory/business_inventory.html', context)


@login_required(login_url=config_account.login_url)
def edit_category(request, category_id):
    return inventory.category_edit(request, category_id)


@login_required(login_url=config_account.login_url)
def inventory_edit(request, product_id):
    page = 'inventory'
    return inventory.edit_product(request, product_id, page)


@login_required(login_url=config_account.login_url)
def edit_product_type(request, product_type_id):
    return inventory.inventory_edit_product_type(request, product_type_id)


@login_required(login_url=config_account.login_url)
def manage_orders(request):
    return manage_order.order_management(request)


@login_required(login_url=config_account.login_url)
def subscribers(request):
    return None

@login_required(login_url=config_account.login_url)
def order_page(request, order_id):
    return manage_order.view_order_page(request, order_id)


@login_required(login_url=config_account.login_url)
def profile_view(request, user_id):
    return profile.Business_profile(request, user_id)

@login_required(login_url=config_account.login_url)
def settings_view(request):
    return business_settings.settings(request)

@login_required(login_url=config_account.login_url)
def payment_settings(request):
    return business_settings.paymentsettings(request)

@login_required(login_url=config_account.login_url)
def delivery_settings(request):
    return business_settings.delivery_settings(request)

@login_required(login_url=config_account.login_url)
def subscribers(request):
    return subscriber.fetch_subscribers(request)

@login_required(login_url=config_account.login_url)
def report(request):
    user_type = config_user.get_user_type(request.user.username)
    if user_type == CUSTOMER or request.method == 'GET':
        return not_found_view(request)

    if request.method == 'POST':
        return report_helper.generate_report(request)

