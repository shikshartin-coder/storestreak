from .data_interface import Category_interface, Product_interface, Product_type_interface,Business_interface
from django.shortcuts import render,redirect, HttpResponseRedirect,HttpResponse
from django.core.files.storage import default_storage
from landing_website.data_interface import AddressInterface
from . import config_account
from landing_website import views as landing_views
from image_compressor import image_compressor

def Business_profile(request,user_id):
    if(int(user_id) != int(request.user.id)):
        return landing_views.not_found_view(request,True)

    business_obj = Business_interface().get_business_by_user_id(user_id)

    if(request.method == 'POST'):
        btn = request.POST.get('btn')
        if(btn == 'edit-profile'):
            cover_image  = image_compressor.compress( request.POST.get('cover_image'),'cover/cover_'+user_id+'.jpeg')
            dp_image = image_compressor.compress( request.POST.get('dp_image'),'logo/logo_'+user_id+'.jpeg')
            business_name = request.POST.get('business_name')
            name = request.POST.get('name')
            business_key = Business_interface().create_business_key(business_name)
            mobile = request.POST.get('mobile')

            if(cover_image == None):
                cover_image = business_obj.cover_image
            if(business_obj.cover_image != cover_image):
                try:
                    path =  business_obj.cover_image.path
                    default_storage.delete(path)
                except:
                    print('no file found')

            if(dp_image == None):
                dp_image = business_obj.dp_image
            if(business_obj.dp_image != dp_image):
                try:
                    path =  business_obj.dp_image.path
                    default_storage.delete(path)
                except:
                    print('no file found')
            Business_interface().update_business(business_obj.id,business_name,name, business_key,dp_image,cover_image)
            return redirect('profile_view',user_id=request.user.id)

    context = {
        'business_obj':business_obj,
    }
    address_list = AddressInterface().fetch_all_addresses_for_user(request.user.id)
    if len(address_list) == 0:
        context.update({
            'address_id':'new'
        })
    else:
        context.update({
            'address':address_list[0],
            'address_id':address_list[0].id,
        })
    return render(request,'./business/profile.html',context)