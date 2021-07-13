from django.contrib.auth.models import User
from .models import OneTimePassword, Address
from django.core.exceptions import ObjectDoesNotExist

class UserInterface():

    def get_for_username(self, username):
        user_list = User.objects.filter(username = username)
        return user_list

    def get_username_for_id(self, id):
        user_object = User.objects.get(id = id)
        return user_object.username
    
    def get_user_for_id(self, id):
        try:
            user_object = User.objects.get(id = id)
        except ObjectDoesNotExist:
            user_object = None
        return user_object
        
    def get_user_for_username(self,username):
        try:
            user_object = User.objects.get(username = username)
        except ObjectDoesNotExist:
            user_object = None
        return user_object



class OneTimePasswordInterface():

    def create_one_time_password(self, mobile, otp, status):
        print(mobile)
        print(otp)
        print(status)
        otp_obj = OneTimePassword.objects.create(mobile = mobile, otp = otp, status = 1)
        return otp_obj

    def otp_by_id(self,otp_id):
        try:
            otp_object = OneTimePassword.objects.get(id = otp_id)
        except ObjectDoesNotExist:
            otp_object = None
        return otp_object

    def disable_otp(self, otp_id):
        otp_object = OneTimePasswordInterface().otp_by_id(otp_id)
        otp_object.status = 0
        otp_object.save()

    def verify_otp(self, otp, mobile,otp_id):
        error = False
        otp_object = OneTimePasswordInterface().otp_by_id(otp_id)
        if otp_object == None:
            error = True

        if otp_object.otp != otp or otp_object.status == 0:
            error = True
        
        return error

    def fetch_all_active_otp_for_mobile(self, mobile):
        otp_list = OneTimePassword.objects.filter(mobile = mobile, status = 1) 
        return otp_list

    def disable_all_active_otp_for_mobile(self, mobile):
        otp_list = OneTimePasswordInterface().fetch_all_active_otp_for_mobile(mobile)
        for otp_object in otp_list:
            OneTimePasswordInterface().disable_otp(otp_object.id)

class AddressInterface():
    
    def create_address(self, user_id, name, mobile, pincode, building, street, landmark, city, state, address_type):
        try:
            address_object = Address.objects.get(user_id = user_id, name = name, mobile = mobile, pincode = pincode, building = building, street = street, landmark = landmark, city = city, state = state, address_type = address_type)
        except ObjectDoesNotExist:
            try:
                address_object = Address.objects.create(user_id = user_id, name = name, mobile = mobile, pincode = pincode, building = building, street = street, landmark = landmark, city = city, state = state, address_type = address_type)
            except:
                address_object = None
        return address_object

    def update_address(self, id, user_id, name, mobile, pincode, building, street, landmark, city, state, address_type):
        try:
            address_object = Address.objects.get(id = id)
            address_object.user_id = user_id
            address_object.name = name
            address_object.mobile = mobile
            address_object.pincode = pincode
            address_object.building = building
            address_object.street = street
            address_object.landmark = landmark
            address_object.city = city
            address_object.state = state
            address_object.address_type = address_type
            address_object.save()
        except ObjectDoesNotExist:
            address_object = None
        return address_object

    def fetch_all_addresses_for_user(self, user_id):
        address_objects_list = Address.objects.filter(user_id = user_id)
        return address_objects_list

    def get_address_by_id(self, id):
        try:
            address_object = Address.objects.get(id = id)
        except ObjectDoesNotExist:
            address_object = None
        return address_object

    def delete_address_by_id(self, id):
        address_object = Address.objects.get(id = id)
        address_object.delete()
