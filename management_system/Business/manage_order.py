from django.shortcuts import render,redirect, HttpResponseRedirect,HttpResponse
from Customer.data_interface import Orders_interface,Customer_Interface,order_status_interface,Product_orders_interface,order_address_interface
from .data_interface import Business_interface,Product_type_interface
from landing_website.data_interface import AddressInterface

def order_management(request):
    business_id = Business_interface().get_business_by_user_id(request.user.id).id
    order_dict = {}
    filter_status_dict = order_status_interface().one_time_status
    filter_status_list = create_list_of_dicts_for_filter_types(filter_status_dict)
    filter_type = request.POST.get('filter_type')
    if filter_type == None or filter_type == '':
        filter_type = filter_status_dict['s2']
    orders = Orders_interface().get_orders_by_business_id_and_status(business_id, filter_type)
    order_status_list = {}
    for order in  reversed(orders):
        total_price = 0
        product_orders = Product_orders_interface().get_product_order_by_order_id(order.order_id)
        order_status_list.update({order: order_status_interface().get_active_order_status_by_order_id(order.order_id).status})
        for p_order in product_orders:
            total_price = p_order.total_price + total_price
        order_dict.update({order:{'p_count':len(product_orders),'total_price':total_price}})

    all_customer = Customer_Interface().get_all_customer()
    products =  Product_type_interface().get_all_product_type()

    context = {
        'order_dict':order_dict,
        'products':products,
        'order_status_list':order_status_list,
        'all_customer':all_customer,
        'search_page':'orders',
        'filter_status_list':filter_status_list,
        'filter_type':filter_status_dict['s2'],
    }
    if request.method == 'POST':
        context.update({
            'filter_type':filter_type,
        })
    return render(request,'./business/manage_orders.html',context)

def create_list_of_dicts_for_filter_types(filter_status_dict):
    a = {'name':'Active','val':filter_status_dict['s2']}
    b = {'name':'New','val':filter_status_dict['s1']}
    c = {'name':'Rejected','val':filter_status_dict['s3']}
    d = {'name':'Delivered','val':filter_status_dict['s4']}
    filter_status_list =  [a,b,c,d]
    temp_list = list(filter_status_list )
    return temp_list

def view_order_page(request,order_id):
    otp_error = False
    order = Orders_interface().get_order_obj_by_order_id(order_id)
    if(order == None):
        return redirect('manage_order')
    customer_obj = Customer_Interface().get_customer_by_id(order.customer_id)
    product_order = Product_orders_interface().get_product_order_by_order_id(order_id)
    business_obj = Business_interface().get_business_obj_by_id(order.business_id)
    page = ''
    active_order_status = order_status_interface().get_active_order_status_by_order_id(order_id)
    status_timeline =  order_status_interface().get_order_status_by_order_id(order_id)

    if(active_order_status.status == order_status_interface().one_time_status['s1']):
        page = 'new'
    else:
        if(active_order_status.status == order_status_interface().one_time_status['s3']):
             page = 'rejected'
        else:
            if(active_order_status.status == order_status_interface().one_time_status['s4']):
                page = 'delivered'
            else:
                page = 'accepted'

    active_status_value = None
    if(page == 'accepted'):
        if(active_order_status.status == order_status_interface().one_time_status['s2']):
            active_status_value = order_status_interface().one_time_status['s2']
        else:
            active_status_value = active_order_status.status

    total_cost = 0
    products_list = []
    for val in product_order:
        product_obj = Product_type_interface().get_product_type_by_id(val.product_type_id)
        products_list.append(product_obj)
        total_cost = total_cost + val.total_price

    address_obj = order_address_interface().get_order_address_by_id(order.order_id)
    total_items = len(product_order)

    if(request.method == "POST"):
        btn = request.POST.get('btn')
        if(btn == 'change_status_btn'):
            status = request.POST.get('order_status')
            order_status_interface().create_order_status(order_id,status,'')
            return redirect('order_page',order_id = order_id)

        if(btn == 'accepted'):
            order_status_interface().create_order_status(order_id,order_status_interface().one_time_status['s2'],'')
            return redirect('order_page',order_id = order_id)

        if(btn == 'rejected'):
            reason = request.POST.get('reject_reason')
            order_status_interface().create_order_status(order_id,order_status_interface().one_time_status['s3'],reason)
            Orders_interface().inactive_order_by_order_id(order_id)
            return redirect('order_page',order_id = order_id)

        if(btn == 'Delivered'):
            order_otp = request.POST.get('order_otp')
            if(Orders_interface().verify_otp(order_otp,order_id)):
                Orders_interface().inactive_order_by_order_id(order_id)
                order_status_interface().create_order_status(order_id,order_status_interface().one_time_status['s4'],'')
                return redirect('order_page',order_id = order_id)
            else:
                otp_error = True
    context = {
        'business_obj':business_obj,
        'customer_obj':customer_obj,
        'order':order,
        'order_obj':order,
        'total_cost':total_cost,
        'order_status':order_status_interface().order_status,
        'address_obj':address_obj,
        'total_items':total_items,
        'page':page,
        'active_status_value':active_status_value,
        'status_timeline':status_timeline,
        'otp_error':otp_error,
        'product_order':product_order,
        'products_list':products_list,
    }
    return render(request,'./business/order_page.html',context)
