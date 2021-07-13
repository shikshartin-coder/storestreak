from Business.data_interface import Product_type_interface, Business_interface,Product_interface,Category_interface
from .data_interface import Customer_Interface,Cart_Interface,Subscribe_Interface
from landing_website.data_interface import AddressInterface
from landing_website import views as landing_view
from django.shortcuts import render,redirect, HttpResponseRedirect,HttpResponse
from . import cart
from . import orders
from landing_website import config_user
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from landing_website.constants import BUSINESS, CUSTOMER

def all_catalog_business():
    business = Business_interface().get_business()
    return business

def catalog_access_check(request,business_key):
    business_obj = Business_interface().get_business_obj_by_business_key(business_key)
    if(business_obj == None):
        return landing_view.not_found_view(request,True)
    else:
        user_type = config_user.get_user_type(request.user.username)
        if user_type == BUSINESS:
            logout(request)
            return redirect('catalog', business_key=business_key)
        return catalog_view(request, business_key)

def catalog_view(request,business_key):
    business_user_id = Business_interface().get_user_by_business_key(business_key)
    if(business_user_id == None):
        return landing_view.not_found_view(request,True)
    business_obj = Business_interface().get_business_obj_by_business_key(business_key)
    if(business_obj == None):
        return landing_view.not_found_view(request,True)
    try:
        sub = Subscribe_Interface().check_subscription(Customer_Interface().get_customer_by_user_id(request.user.id).id,business_obj.id)
    except:
        sub = False
    if(request.user.id != None):
        customer_id =  Customer_Interface().get_customer_id_by_user_id(request.user.id)
        all_cart = Cart_Interface().get_customer_cart(customer_id,business_obj.id)
    else:
        all_cart = []

    category_list = Category_interface().get_category(business_obj.user)


    all_category = {}
    for category in category_list:
        product_type_obj = []
        product_type_dict = {}

        products = Product_interface().get_product_by_category_id(category.id)
        for prod in products:
            product_type_obj = product_type_obj + list(Product_type_interface().get_product_type_by_product_id(prod.id))

        non_zero_list = True
        if(len(product_type_obj) == 0):
            non_zero_list = False

        for pro in product_type_obj:
            flag = True
            if pro.stock == 0:
                #print(pro.name)
                product_type_dict.update({pro:'out_stock'})
            else:
                for cart in all_cart:
                    if(cart.product_type_id == pro.id):
                        product_type_dict.update({pro:cart})
                        flag = False
                        break
                if(flag):
                    product_type_dict.update({pro:None})

        if(non_zero_list):
            all_category.update({category:product_type_dict})

    total_amount = 0
    total_items = 0

    for cart in all_cart:
        total_amount = total_amount + cart.total_price
        total_items = total_items + cart.quantity

    cart_count = len(all_cart)

    address_object = AddressInterface().get_address_by_id(business_user_id)

    context = {
        'all_category':all_category,
        'business_key':business_key,
        'business_obj':business_obj,
        'sub':sub,
        'total_amount':total_amount,
        'total_items':total_items,
        'cart_count':cart_count,
        'search_page':'catalog',
        'address_object':address_object,
    }
    return render(request,'./customer/catalogue/catalog.html',context)

def product_access_check(request,business_key, product_key):
    business_user_id = Business_interface().get_user_by_business_key(business_key)
    if(business_user_id == None):
        return landing_view.not_found_view(request,True)
    product_type = Product_type_interface().get_product_type_by_user_id(business_user_id,product_key)
    if(product_type == None):
        return landing_view.not_found_view(request,True)
    user_type = config_user.get_user_type(request.user.username)
    if user_type == BUSINESS:
        logout(request)
        return redirect('product', business_key=business_key, product_key=product_key)
    return product(request, business_key, product_key)

def product(request,business_key,product_key):
    business_user_id = Business_interface().get_user_by_business_key(business_key)
    if(business_user_id == None):
        return landing_view.not_found_view(request,True)
    product_type = Product_type_interface().get_product_type_by_user_id(business_user_id,product_key)
    if(product_type == None):
        return landing_view.not_found_view(request,True)
    category = Category_interface().get_category_by_id(Product_interface().get_category_id_from_product_type_id(product_type.id))
    business_obj = Business_interface().get_business_obj_by_business_key(business_key)
    customer_obj = Customer_Interface().get_customer_by_user_id(request.user.id)
    cart_object = None
    if customer_obj!=None:
        cart_object = Cart_Interface().check_cart_obj(product_type.id, business_obj.id, customer_obj.id)
    cart_quantity = cart_object.quantity if cart_object!=None else 0
    max_qty_val = (product_type.stock-cart_quantity) if (product_type.stock - cart_quantity) < 10 else 10
    selected_qty_val = 1
    if cart_object!=None:
        selected_qty_val = cart_object.quantity if cart_object.quantity <= max_qty_val else max_qty_val
    qty_list = [(x+1) for x in range(max_qty_val)]

    context = {
        'business_key':business_key,
        'product_type':product_type,
        'business_obj':business_obj,
        'category':category,
        'qty_list':qty_list,
        'max_qty_val':max_qty_val,
        'selected_qty_val':selected_qty_val,
    }
    if(request.method == 'POST'):
        btn = request.POST.get('btn')
        if(btn == 'buy'):
            quantity = request.POST.get('quantity')
            try:
                address_list = AddressInterface().fetch_all_addresses_for_user(request.user.id)
                default = address_list[len(address_list)-1].id
            except:
                default = 0
                address_list = []

            context.update({
               'quantity':quantity,
               'address_list':address_list,
               'default':default
            })
            return render(request,'./customer/catalogue/confirm_order.html',context)

        if(btn == 'place_order'):
            order_obj =  orders.place_order(request)
            return redirect('customer_order_page',order_id=order_obj.order_id)

        if btn == 'address_order_id':
            quantity = request.POST.get('quantity_hidden')
            context.update({
                'quantity':quantity,
            })
            return render(request, './customer/add_order_address.html',context)

        if btn == 'new_order_address':
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pincode = request.POST.get('pincode')
            building = request.POST.get('building')
            street = request.POST.get('street')
            landmark = request.POST.get('landmark')
            city = request.POST.get('city')
            state = request.POST.get('state')
            address_type = request.POST.get('address_type')
            quantity = request.POST.get('quantity')
            user_id = request.user.id
            address_object = AddressInterface().create_address(user_id = user_id, name = name, mobile = mobile, pincode = pincode, building = building, street = street, landmark = landmark, city = city, state = state, address_type = address_type)
            if address_object != None:
                default = address_object.id
                address_list = AddressInterface().fetch_all_addresses_for_user(request.user.id)
                context.update({
                'quantity':quantity,
                'address_list':address_list,
                'default':default
                })
            return render(request,'./customer/catalogue/confirm_order.html',context)

    return render(request,'./customer/catalogue/product.html',context)
