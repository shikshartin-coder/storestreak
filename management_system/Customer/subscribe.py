from django.shortcuts import render,redirect, HttpResponseRedirect,HttpResponse
from .data_interface import Customer_Interface,Subscribe_Interface
from Business.data_interface import Business_interface


def subscribe_view(request,business_name,action):
    customer_id = Customer_Interface().get_customer_id_by_user_id(request.user.id)
    business = Business_interface().get_business_obj_by_business_key(business_name)
    if(action == 'subscribe'):
        subscribe_obj = Subscribe_Interface().create_subscribe(business.id,customer_id)
        return redirect('catalog',business_key=business.business_key)
    else:
        if(action == 'unsubscribe'):
            unsubscribe_obj = Subscribe_Interface().unsubscribe(business.id,customer_id)
            return redirect('catalog',business_key=business.business_key)
        else:
            return redirect('homepage')


def get_all_subscribe_list(user_id):
    business_id_list =  Subscribe_Interface().get_user_id_of_subscribe_list(user_id)
    business_list = []
    for business_id in business_id_list:
        business_list.append(Business_interface().get_business_obj_by_id(business_id.business_id))
    return business_list

def get_unsubscribed_list(user_id):
    business_list = Business_interface().get_business()
    subscribed_business_list = get_all_subscribe_list(user_id)
    unsubscribed_business_list = set(business_list).difference(set(subscribed_business_list))
    return unsubscribed_business_list

def get_all_business():
    return Business_interface().get_business()

def fetch_subscribed_businesses_list(request):
    customer_object = Customer_Interface().get_customer_by_user_id(request.user.id)
    business_objects_list = Business_interface().get_businesses_subscribed_by_customer(customer_object.id)
    subscription_objects_list_for_customer = Subscribe_Interface().get_all_subscription_objects_for_customer(customer_object.id)
    result_list = generate_list_of_businesses_subscribed(business_objects_list, subscription_objects_list_for_customer)
    context  = {
        'subscribed_list':result_list,
        'total_count':len(result_list)
    }
    return render(request, './customer/subscribed_businesses.html',context)

def generate_list_of_businesses_subscribed(business_objects_list, subscription_objects_list_for_customer):
    print(business_objects_list)
    print(subscription_objects_list_for_customer)
    result_list = []
    length = len(business_objects_list)
    for i in range(length):
        business_dict = {
            'name':business_objects_list[i].Business_name,
            'category':business_objects_list[i].category,
            'business_key':business_objects_list[i].business_key,
            'timestamp':subscription_objects_list_for_customer[i].timestamp,
        }
        result_list.append(business_dict)
    result_list_sorted_by_timestamp = sorted(result_list, key=lambda k: k['timestamp'], reverse=True)
    return result_list_sorted_by_timestamp

