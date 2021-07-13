from django.shortcuts import render,redirect, HttpResponseRedirect,HttpResponse
from .data_interface import Customer_Interface,Cart_Interface,Orders_interface
from Business.data_interface import Business_interface,Product_type_interface
from django.http import JsonResponse
from . import orders


def product_cart(request,business_key):
    customer_id =  Customer_Interface().get_customer_id_by_user_id(request.user.id)
    business_id = Business_interface().get_business_obj_by_business_key(business_key).id
    all_cart = Cart_Interface().get_customer_cart(customer_id,business_id)
    active_cart = []

    for cart in all_cart:
        active_cart.append(Product_type_interface().get_product_type_by_id(cart.product_type_id))
    return_obj =  {
        'all_cart': all_cart,
        'product_in_cart':active_cart,
        }

    if(request.method =='POST'):
        btn = request.POST.get('btn')
        if(btn == 'add_cart_catalog'):
            add_to_cart(request)
            return JsonResponse({'added':'1'})
        if btn == 'add_cart_product_page':
            add_to_cart(request)
            business_key = request.POST.get('business_key')
            product_key = request.POST.get('product_key')
            return redirect('product',business_key=business_key,product_key=product_key)
    return return_obj

def cart_place_order(request,payment_obj,payment_mode):
    if(request.method == 'GET'):
        business_key = request.GET.get('business_key')
        address_id = request.GET.get('selected_address')
        customer_id =  Customer_Interface().get_customer_id_by_user_id(request.user.id)
        business_id = Business_interface().get_business_obj_by_business_key(business_key).id
        all_cart = Cart_Interface().get_customer_cart(customer_id,business_id)
        delivery_obj = Business_interface().get_delivery_charge(business_id )
        order = Orders_interface().create_cart_order(all_cart,address_id,customer_id,business_id,delivery_obj,payment_obj,payment_mode)
        empty_cart = Cart_Interface().empty_cart(all_cart)
        return order


def add_to_cart(request):
    if(request.method == 'POST'):
        product_type_id = request.POST.get('product_type_id')
        business_id = request.POST.get('business_id')
        quantity = request.POST.get('quantity')
        customer_id = Customer_Interface().get_customer_id_by_user_id(request.user.id)
        product_obj = Product_type_interface().get_product_type_by_id(product_type_id)
        product_price = product_obj.cost

        cart = Cart_Interface().check_cart_obj(product_type_id,business_id,customer_id)

        if(cart != None):
                quantity = Cart_Interface().get_quantity(cart.id) + int(quantity)
                if(quantity >= 0):
                    total_price = product_obj.cost * quantity

                    cart_obj = Cart_Interface().update_quantity(cart.id,quantity,total_price)
        else:
            if(int(quantity) > 0):
                cart_obj = Cart_Interface().create_cart(product_type_id,business_id,customer_id,quantity,product_price)
        return True

def add_to_cart_authentication_required(username, business_key, product_key):
    business_object = Business_interface().get_business_obj_by_business_key(business_key)
    product_object = Product_type_interface().get_product_type_object_by_product_type_key(product_key)
    quantity = 1
    customer_object_list = Customer_Interface().get_customer_for_mobile(username)
    customer_object = customer_object_list[0]
    product_price = product_object.cost

    cart = Cart_Interface().check_cart_obj(product_type_id=product_object.id, business_id=business_object.id, customer_id=customer_object.id)
    if cart!= None:
        quantity = Cart_Interface().get_quantity(cart.id) + int(quantity)
        total_price = product_object.cost * quantity

        cart_object = Cart_Interface().update_quantity(cart.id, quantity, total_price)

    else:
        cart_object = Cart_Interface().create_cart(product_object.id, business_object.id, customer_object.id, quantity, product_price)
