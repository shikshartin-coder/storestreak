from django.shortcuts import render,redirect, HttpResponseRedirect,HttpResponse
from .data_interface import Business_interface
from landing_website import constants

def settings(request):
    settings_value = Business_interface().get_settings(request.user.id)
    if(request.method == 'POST'):
        btn = request.POST.get('btn')
        if(btn == 'edit_settings'):
            initial_walet = request.POST.get('initial_amount')
            subscription_amount = request.POST.get('sub_amount')

            settings_obj = Business_interface().update_settings(request.user.id,initial_walet,subscription_amount)
            return redirect('settings')
    context = {
        'settings_value':settings_value,
    }
    return render(request,'./business/settings.html',context)

def paymentsettings(request):
    payment_choice = Business_interface().get_payment_choice(Business_interface().get_business_by_user_id(request.user.id).id)
    if(request.method == 'POST'):
        payment = request.POST.get('payment')
        Business_interface().set_payment_choice(payment,Business_interface().get_business_by_user_id(request.user.id).id)
        return redirect('payment_settings')
    context = {
        'payment_choice':payment_choice,
        'payment_modes':constants.payment_modes,
    }
    return render(request,'./business/payment_settings.html',context)

def delivery_settings(request):
    delivery = request.GET.get('delivery',None)
    delivery_charge = request.GET.get('delivery_charge',None)
    minimum_charge = request.GET.get('minimum_charge',None)
    delivery_charge1 = request.GET.get('delivery_charge1',None)

    delivery_obj = Business_interface().get_delivery_charge(Business_interface().get_business_by_user_id(request.user.id).id)

    if(delivery == 'free'):
        Business_interface().set_delivery_charge(Business_interface().get_business_by_user_id(request.user.id).id,0,0,delivery)    
        return redirect('delivery_settings')

    if(delivery == 'fixed'):
        if(delivery_charge == ""):
            delivery_charge = 0
        Business_interface().set_delivery_charge(Business_interface().get_business_by_user_id(request.user.id).id,delivery_charge,0,delivery) 
        return redirect('delivery_settings')

    if(delivery == 'custom'):
        if(delivery_charge1 == ""):
           delivery_charge1 = 0
        if(minimum_charge == ""):
            minimum_charge = 0
        Business_interface().set_delivery_charge(Business_interface().get_business_by_user_id(request.user.id).id,delivery_charge1,minimum_charge,delivery) 
        return redirect('delivery_settings')

    delivery = delivery_obj['delivery_type']
    context = {
       'delivery':delivery,
       'delivery_charge': delivery_obj['delivery_charge'],
       'minimum_amount': delivery_obj['minimum_amount'],

    }
    return render(request,'./business/delivery-settings.html',context)