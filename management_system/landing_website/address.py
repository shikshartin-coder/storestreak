from django.shortcuts import render,redirect
from .data_interface import AddressInterface, UserInterface
from . import config_user
from .constants import BUSINESS,CUSTOMER,states
from . import constants
def add_address(request, id):
    username = UserInterface().get_username_for_id(request.user.id)
    user_type = config_user.get_user_type(username)
    if(user_type != None):
        if(user_type == CUSTOMER):
            path_to_user_base = "./customer/catalogue/base.html"
        else:
            path_to_user_base = "./business/base.html"
    else:
        return redirect('homepage')
    state_list = states
    address_type_list = constants.address_type
    context = {
        'address': None,
        'id':'new',
        'address_type_list':address_type_list,
        'state_list':state_list,
        'user_type': user_type,
        'state_list':state_list,
        'path_to_user_base' : path_to_user_base,
    }
    if id != 'new':
        address_object = AddressInterface().get_address_by_id(id)
        context['address'] = address_object
        context['id'] = id
    if request.method == 'POST':
        btn = request.POST.get('btn')
        if btn != 'delete':
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pincode = request.POST.get('pincode')
            building = request.POST.get('building')
            street = request.POST.get('street')
            landmark = request.POST.get('landmark')
            city = request.POST.get('city')
            state = request.POST.get('state')
            address_type = request.POST.get('address_type')
            user_id = request.user.id
        if btn == 'new':
            address_object = AddressInterface().create_address(user_id = user_id, name = name, mobile = mobile, pincode = pincode, building = building, street = street, landmark = landmark, city = city, state = state, address_type = address_type)
            if address_object != None:
                if user_type == BUSINESS:
                    return redirect('profile_view',user_id=request.user.id)
                return redirect("address-list")
        if btn == 'edit':
            address_object = AddressInterface().update_address(id = id, user_id = user_id, name = name, mobile = mobile, pincode = pincode, building = building, street = street, landmark = landmark, city = city, state = state, address_type = address_type)
            if address_object != None:
                if user_type == BUSINESS:
                    return redirect('profile_view', user_id=request.user.id)
                return redirect("address-list")
        if btn == 'delete':
            AddressInterface().delete_address_by_id(id)
            return redirect("address-list")

    return render(request, './landing_website/address/add-address.html', context)

def address_list(request):
    username = UserInterface().get_username_for_id(request.user.id)
    user_type = config_user.get_user_type(username)
    address_object_list = AddressInterface().fetch_all_addresses_for_user(user_id=request.user.id)
    path_to_user_base = "../"+user_type+"/base.html"
    context = {
        'path_to_user_base' : path_to_user_base,
        'address_list':address_object_list,
    }
    return render(request, './landing_website/address/address_list.html', context)
