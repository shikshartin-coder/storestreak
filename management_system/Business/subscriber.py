from Customer.data_interface import Customer_Interface, Subscribe_Interface
from .data_interface import Business_interface
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse

def fetch_subscribers(request):
    business_object = Business_interface().get_business_by_user_id(request.user.id)
    customer_objects_list = Customer_Interface().get_all_customers_for_a_subscribed_business(business_object.id)
    subscription_objects_list_for_business = Subscribe_Interface().get_all_subscription_objects_for_business(business_object.id)
    result_list = generate_list_of_customer_subscribers(customer_objects_list, subscription_objects_list_for_business)
    context  = {
        'subscribers_list':result_list,
        'total_count':len(result_list)
    }
    return render(request, './business/subscribers.html',context)

def generate_list_of_customer_subscribers(customer_objects_list, subscription_objects_list_for_business):
    print(customer_objects_list)
    print(subscription_objects_list_for_business)
    result_list = []
    length = len(customer_objects_list)
    for i in range(length):
        mobile = customer_objects_list[i].mobile
        if customer_objects_list[i].privacy_settings:
            mobile = None
        customer_dict = {
            'name':customer_objects_list[i].name,
            'mobile':mobile,
            'timestamp':subscription_objects_list_for_business[i].timestamp,
        }
        result_list.append(customer_dict)
    result_list_sorted_by_timestamp = sorted(result_list, key=lambda k: k['timestamp'], reverse=True)
    return result_list_sorted_by_timestamp
