from django.shortcuts import render,redirect, HttpResponseRedirect,HttpResponse
from .data_interface import Orders_interface,Customer_Interface, order_status_interface,order_address_interface,Product_orders_interface,transaction_interface, Cart_Interface
from Business.data_interface import Business_interface,Product_type_interface
from landing_website.data_interface import AddressInterface
import random
from landing_website import views as landing_views
from . import cart
from landing_website import constants
from django.views.decorators.csrf import csrf_exempt
from paytm import paytm
import paytmchecksum as PaytmChecksum
import json

def place_order(request,payment_obj,payment_mode):
    if(request.method == 'GET'):
        product_type_id = request.GET.get('product_type_id')
        business_key = request.GET.get('business_key')
        quantity = request.GET.get('quantity')
        address_id = request.GET.get('selected_address')
        business_obj = Business_interface().get_business_obj_by_business_key(business_key)
        delivery_obj = Business_interface().get_delivery_charge(business_obj.id)
        product_obj = Product_type_interface().get_product_type_by_id(product_type_id)
        total_price = product_obj.cost * int(quantity)
        delivery_charge_amount = delivery_obj['delivery_charge']
        total_order_amount =  total_price + delivery_charge_amount
        if(delivery_obj['delivery_type'] == 'custom'):
            if(total_price > delivery_obj['minimum_amount']):
                total_order_amount =  total_price
                delivery_charge_amount = 0

        customer_id = Customer_Interface().get_customer_id_by_user_id(request.user.id)
        order_otp =  Orders_interface().generate_order_otp()
        order = Orders_interface().create_order(product_type_id,business_obj.id,customer_id,quantity,address_id,total_price,order_otp,total_order_amount,delivery_charge_amount,payment_obj,payment_mode)
        return order

def view_orders(request):
    customer_id =  Customer_Interface().get_customer_id_by_user_id(request.user.id)
    order_dict = {}
    orders = Orders_interface().get_customer_orders(customer_id)
    all_business = Business_interface().get_business()
    order_status_list = {}
    for order in reversed(orders):
        order_dict.update({order:len(Product_orders_interface().get_product_order_by_order_id(order.order_id))})
        order_status_list.update({order: order_status_interface().get_active_order_status_by_order_id(order.order_id).status})
    products = Product_type_interface().get_all_product_type()
    context = {
        'order_dict':order_dict,
        'search_page':'orders',
        'order_status_list':order_status_list,
        'all_business':all_business,
    }
    return render(request,'./customer/orders.html',context)


def customer_order_page(request,order_id):
    customer_id =  Customer_Interface().get_customer_id_by_user_id(request.user.id)
    order_obj = Orders_interface().get_order_obj_by_order_id(order_id)
    if(customer_id != order_obj.customer_id):
        return landing_views.not_found_view(request,True)
    business_obj = Business_interface().get_business_obj_by_id(order_obj.business_id)
    product_order_list = Product_orders_interface().get_product_order_by_order_id(order_id)
    address_object =  order_address_interface().get_order_address_by_id(order_obj.order_id)
    print( address_object )
    status_timeline =  order_status_interface().get_order_status_by_order_id(order_id)
    ordered_products = []
    item_sub_total = 0
    for order in product_order_list:
        item_sub_total = item_sub_total + order.total_price
        ordered_products.append(Product_type_interface().get_product_type_by_id(order.product_type_id))

    total_items = len(product_order_list)

    context = {
    'item_sub_total':item_sub_total,
    'business_obj':business_obj,
    'order':order_obj,
    'product_order_list':product_order_list,
    'ordered_products': ordered_products,
    'address_obj':address_object,
    'status_timeline':status_timeline,
    'total_items':total_items,
    }
    return render(request,'./customer/order_page.html',context)

def confirm_order_view(request):
    if(request.method == 'GET'):
        error = ''
        btn = request.GET.get('btn')
        buy_mode = request.GET.get('buy_mode')
        business_key = request.GET.get('business_key')
        product_type_id = request.GET.get('product_type_id')
        quantity = request.GET.get('quantity')
        business_obj = Business_interface().get_business_obj_by_business_key(business_key)
        delivery_obj = Business_interface().get_delivery_charge(business_obj.id)
        product_obj = Product_type_interface().get_product_type_by_id(product_type_id)
        try:
            address_list = AddressInterface().fetch_all_addresses_for_user(request.user.id)
            default = address_list[len(address_list)-1].id
        except:
            default = 0
            address_list = []
            error = 'no_address'
        total_product_price = int(quantity) * product_obj.cost
        context = {
            'business_obj':business_obj,
            'quantity':quantity,
            'product_obj':product_obj,
            'buy_mode':buy_mode,
            'address_list':address_list,
            'default':default,
            'error':error,
            'total_product_price':total_product_price,
            'delivery_obj':delivery_obj,
        }

        if(btn == 'buy'):
            return render(request,'./customer/catalogue/confirm_order.html',context)
        if (btn == 'address_order_id'):
            state_list = constants.states
            address_type_list = constants.address_type
            context.update({'state_list':state_list,'address_type_list':address_type_list,})
            return render(request, './customer/add_order_address.html',context)
        if (btn == 'new_order_address'):
            address_object = generate_address(request,btn)
            try:
                address_list = AddressInterface().fetch_all_addresses_for_user(request.user.id)
                default = address_list[len(address_list)-1].id
                error = 'address'
            except:
                default = 0
                address_list = []
                error = 'no_address'
            if address_object != None:
                default = address_object.id
                context['default'] = default
                context['address_list']=address_list
            return render(request,'./customer/catalogue/confirm_order.html',context)

def confirm_order_cart(request):
    error = ''
    if(request.method == 'GET'):
        btn = request.GET.get('btn')
        business_key = request.GET.get('business_key')
        buy_mode = request.GET.get('buy_mode')
        business_obj = Business_interface().get_business_obj_by_business_key(business_key)

        delivery_obj = Business_interface().get_delivery_charge(business_obj.id)
        try:
            address_list = AddressInterface().fetch_all_addresses_for_user(request.user.id)
            default = address_list[len(address_list)-1].id
        except:
            default = 0
            address_list = []
            error = 'no_address'
        product_type = cart.product_cart(request,business_key)
        total_item_count = len(product_type['all_cart'])

        context = {
            'business_obj':business_obj,
            'buy_mode':buy_mode,
            'all_cart':product_type['all_cart'],
            'product_in_cart':product_type['product_in_cart'],
            'buy_mode':buy_mode,
            'address_list':address_list,
            'default':default,
            'error':error,
            'total_item_count':total_item_count,
            'delivery_obj':delivery_obj,
        }
        if(btn == 'buy_cart'):
            return render(request,'./customer/catalogue/confirm_order.html',context)

        if (btn == 'address_order_id'):
            state_list = constants.states
            address_type_list = constants.address_type
            context.update({'state_list':state_list,'address_type_list':address_type_list,})
            return render(request, './customer/add_order_address.html',context)

        if (btn == 'new_order_address'):
            address_object = generate_address(request,btn)
            try:
                address_list = AddressInterface().fetch_all_addresses_for_user(request.user.id)
                default = address_list[len(address_list)-1].id
                error = 'address'
            except:
                default = 0
                address_list = []
                error = 'no_address'

            if address_object != None:
                default = address_object.id
                context['default'] = default
                context['address_list']=address_list
            return render(request,'./customer/catalogue/confirm_order.html',context)

def payment(request):
    buy_mode = request.GET.get('buy_mode')
    product_type_id = request.GET.get('product_type_id')
    business_key = request.GET.get('business_key')
    quantity = request.GET.get('quantity')
    selected_address = request.GET.get('selected_address')
    payment_option = request.GET.get('payment_option')

    business_obj = Business_interface().get_business_obj_by_business_key(business_key)
    delivery_obj = Business_interface().get_delivery_charge(business_obj.id)
    payment_choice = Business_interface().get_payment_choice(Business_interface().get_business_obj_by_business_key(business_key).id)
    context = {
                'buy_mode':buy_mode,
                'product_type_id':product_type_id,
                'business_key': business_key,
                'business_obj':business_obj,
                'quantity':quantity,
                'selected_address':selected_address,
                'payment_choice':payment_choice,
                'payment_modes':constants.payment_modes,
    }
    if(buy_mode == 'normal_buy'):
        if(payment_option == 'COD'):
            order_obj = place_order(request,True,payment_option)
            current_stock = decrease_stock_of_order_in_product_type(order_obj.order_id)
            if current_stock == 0:
                Cart_Interface().delete_cart_using_product_type_id(product_type_id)
            return redirect('success',orderid=order_obj.order_id)

        if(payment_option == 'PAYTM'):
            order_obj = place_order(request,False,payment_option)
            total_order_amount = Orders_interface().get_total_order_amount(order_obj.order_id)
            paytm_obj = paytm.paytm(str(order_obj.order_id),str(request.user.id),str(total_order_amount))
            return paytm.send_payment(request,paytm_obj['body']['txnToken'],str(order_obj.order_id),str(request.user.id),str(total_order_amount))
        return render(request,'./customer/catalogue/payment.html',context)

    if(buy_mode == 'cart_buy'):
        if(payment_option == 'COD'):
            order_obj = cart.cart_place_order(request,True,payment_option)
            decrease_stock_of_order_in_product_type(order_obj.order_id)
            return redirect('success',orderid=order_obj.order_id)

        if(payment_option == 'PAYTM'):
            order_obj = cart.cart_place_order(request,False,payment_option)
            total_order_amount = Orders_interface().get_total_order_amount(order_obj.order_id)
            paytm_obj = paytm.paytm(str(order_obj.order_id),str(request.user.id),str(total_order_amount))
            return paytm.send_payment(request,paytm_obj['body']['txnToken'],str(order_obj.order_id),str(request.user.id),str(total_order_amount))
        return render(request,'./customer/catalogue/payment.html',context)
        
    return landing_views.not_found_view(request,True)


def decrease_stock_of_order_in_product_type(order_id):
    order_products =Product_orders_interface().get_product_order_by_order_id(order_id)
    for order_p in order_products:
        stock = Product_type_interface().decrease_stock_for_product_type_id_using_id_and_quantity(order_p.product_type_id, order_p.quantity)
    return stock

def generate_address(request,btn):
    if (btn == 'new_order_address'):
        name = request.GET.get('name')
        mobile = request.GET.get('mobile')
        pincode = request.GET.get('pincode')
        building = request.GET.get('building')
        street = request.GET.get('street')
        landmark = request.GET.get('landmark')
        city = request.GET.get('city')
        state = request.GET.get('state')
        address_type = request.GET.get('address_type')
        quantity = request.GET.get('quantity')
        user_id = request.user.id
        address_object = AddressInterface().create_address(user_id = user_id, name = name, mobile = mobile, pincode = pincode, building = building, street = street, landmark = landmark, city = city, state = state, address_type = address_type)
        return address_object
    return None


@csrf_exempt
def handel_payment_request(request):
    if(request.method == 'POST'):
        orderid = request.POST.get('ORDERID')
        checksumhash = request.POST.get('CHECKSUMHASH')
        txnid = request.POST.get('TXNID')
        txnamount = request.POST.get('TXNAMOUNT')
        paymentmode = request.POST.get('PAYMENTMODE')
        currency = request.POST.get('CURRENCY')
        txndate = request.POST.get('TXNDATE')
        status = request.POST.get('STATUS')
        respcode = request.POST.get('RESPCODE')
        respmsg = request.POST.get('RESPMSG')
        gatewayname = request.POST.get('GATEWAYNAME')
        banktxnid = request.POST.get('BANKTXNID')
        bankname = request.POST.get('BANKNAME')
        paytm_obj = paytm.verify_sumcheck(request)
        if(paytm_obj):
            transaction_interface().create_transaction(orderid,txnid,txnamount,paymentmode,currency,txndate,status,respcode,respmsg,gatewayname,banktxnid,bankname,checksumhash)
            if(status == 'TXN_SUCCESS'):
                try:
                    Orders_interface().change_payment(orderid)
                except:
                    return redirect('failure',orderid=orderid)

                decrease_stock_of_order_in_product_type(orderid)
                return redirect('success',orderid=orderid)
            if(status == 'TXN_FAILURE'):
                Orders_interface().delete_order(orderid)
                return redirect('failure',orderid=orderid)
            if(status == 'PENDING'):
                Orders_interface().delete_order(orderid)
                return redirect('failure',orderid=orderid)
        return landing_views.not_found_view(request,True)

def order_placed_success(request,orderid):
    order_obj = Orders_interface().get_order_obj_by_order_id(orderid)
    if(order_obj == None):
        return landing_views.not_found_view(request,True)

    business_obj = Business_interface().get_business_obj_by_id(order_obj.business_id)

    if(order_obj.payment_mode == 'COD'):
        transaction_obj = None
    else:
        transaction_obj = transaction_interface().get_transaction(orderid)

    context = {
        'order_obj':order_obj,
        'transaction_obj':transaction_obj,
        'business_obj':business_obj,
    }
    return render(request,'./customer/order_placed.html',context)

def order_placed_failure(request,orderid):
    transaction_obj = transaction_interface().get_transaction(orderid)
    if(transaction_obj == None):
        return landing_views.not_found_view(request,True)
    if(transaction_obj.status == 'TXN_SUCCESS'):
         return landing_views.not_found_view(request,True)
    context = {
        'transaction_obj':transaction_obj,
    }
    return render(request,'./customer/payment_fail.html',context)