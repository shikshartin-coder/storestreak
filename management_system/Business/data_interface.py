from .models import  Business,Category,Product, Product_type
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from landing_website import config_user
from landing_website import constants


class  Business_interface():
    def get_business(self):
        business_list = Business.objects.all()
        return business_list

    def get_delivery_charge(self,business_id):
        business_obj =  Business_interface().get_business_obj_by_id(business_id)
        return {
            'delivery_charge':business_obj.delivery_charge,
            'minimum_amount':business_obj.minimum_delivery_amount,
            'delivery_type':business_obj.delivery_type,
        }

    def set_delivery_charge(self,business_id,delivery_charge,minimum_delivery_amount,delivery_type):
        business_obj =  Business_interface().get_business_obj_by_id(business_id)
        business_obj.delivery_charge = delivery_charge
        business_obj.minimum_delivery_amount = minimum_delivery_amount
        business_obj.delivery_type = delivery_type
        business_obj.save()
        return True

    def create_business_key(self,business_name):
        business_key = config_user.idfy(business_name)
        try:
            business_obj = Business.objects.get(business_key = business_key)
        except ObjectDoesNotExist:
            return business_key
        business_name = business_name +  config_user.random_letter()
        return Business_interface().create_business_key(business_name)

    def get_business_obj_by_business_key(self,business_key):
        try:
            business = Business.objects.get(business_key = business_key)
        except:
            business = None
        return business

    def get_business_by_user_id(self,user_id):
        try:
            business_object = Business.objects.get(user = user_id)
        except ObjectDoesNotExist:
            business_object = None
        return business_object

    def get_business_obj_by_id(self,business_id):
        business_obj = Business.objects.get(id = business_id)
        return business_obj

    def get_user_by_business_key(self, business_key):
        try:
            business_user_id = Business.objects.get(business_key = business_key).user
        except:
            return None
        return business_user_id

    def get_business_mobile(self,mobile):
        obj = Business.objects.filter(mobile = mobile)
        return obj

    def filter_business_key_by_business_key(self,business_key):
        business_key = Business.objects.filter(business_key = business_key)
        return business_key

    def create_business(self,new_business_name,business_key,new_name,new_category,new_mobile,new_user_id):
        try:
            business_obj = Business.objects.create(
                Business_name = new_business_name,
                business_key = business_key,
                name = new_name,
                category = new_category,
                mobile = new_mobile,
                user= new_user_id,
                payment_choice = 'PAYTM',
            )
        except:
            business_obj = None
        return business_obj

    def update_business(self,b_id,business_name,name, business_key,dp_image,cover_image):
        try:
            business_obj = Business.objects.get(id = b_id)
        except ObjectDoesNotExist:
            business_obj = None

        if(business_obj != None):
            business_obj.Business_name = business_name
            business_obj.name = name
            business_obj.business_key=business_key
            business_obj.dp_image = dp_image
            business_obj.cover_image = cover_image
            business_obj.save()
        return business_obj

    def set_payment_choice(self,payment,business_id):
            business_obj = Business_interface().get_business_obj_by_id(business_id)
            business_obj.payment_choice = payment
            business_obj.save()
            return True

    def get_payment_choice(self,business_id):
            business_obj = Business_interface().get_business_obj_by_id(business_id)
            return business_obj.payment_choice

    def get_settings(self,user_id):
        try:
            business_obj = Business.objects.get(user= user_id)
        except ObjectDoesNotExist:
            business_obj = None
        return business_obj

    def update_settings(self,user_id,initial_walet,subscription_amount):
        try:
            business_obj = Business.objects.get(user= user_id)
        except ObjectDoesNotExist:
            business_obj = None
        if(business_obj != None):
            business_obj.initial_walet = initial_walet
            business_obj.subscription_amount = subscription_amount
            business_obj.save()
        return business_obj

    def delete_business(self,b_id):
        try:
            business_obj = Category.objects.get(id = b_id)
        except ObjectDoesNotExist:
            return False
        business_obj.delete()
        return True

    def check_user_is_business(self, mobile):
        business_list = Business_interface().get_business_mobile(mobile = mobile)
        if len(business_list) == 0:
            return False
        return True

    def get_category_list(self):
        category_list = constants.category_list
        return category_list


    def get_businesses_subscribed_by_customer(self, customer_id):
        from Customer.data_interface import Subscribe_Interface
        business_ids = Subscribe_Interface().get_all_business_id_for_a_customer(customer_id)
        business_objects_ids = Business.objects.filter(id__in=business_ids).order_by('id')
        return business_objects_ids


class Category_interface():

    def get_category(self,id):
        category_list = Category.objects.filter(user = id)
        return category_list

    def get_category_by_id(self,id):
        return  Category.objects.get(id=id)


    def create_category(self,new_name,image,user):

        category_obj = Category.objects.create(
                name = new_name,
                image = image,
                status = True,
                user = user,
            )

        return category_obj

    def update_category(self,c_id,new_name,image,new_status):
        try:
            category_obj = Category.objects.get(id = c_id)
        except ObjectDoesNotExist:
            category_obj = None
        if(category_obj != None):
            category_obj.name = new_name
            category_obj.image=image
            category_obj.status = new_status
            category_obj.save()

        return category_obj

    def delete_category(self,c_id):
        try:
            category_obj = Category.objects.get(id = c_id)
        except ObjectDoesNotExist:
            return False
        category_obj.delete()
        return True


class Product_interface():
    def get_product(self,request_id):
        product_list = Product.objects.filter(user = request_id)
        return  product_list

    def get_category_id_from_product_type_id(self,product_type_id):
        product_id = Product_type_interface().get_product_type_by_id(product_type_id).product_id
        Category_id = Product_interface().get_product_id(product_id).category_id
        return Category_id

    def get_product_by_category_id(self,category_id):
        return Product.objects.filter(category_id = category_id)

    def get_product_by_user(self,user):
        return Product.objects.filter(user = user)


    def get_product_id(self,product_id):
        return Product.objects.get(id = product_id)

    def get_product_by_id(self,request,id):
        try:
            product = Product.objects.get(id = id,user = request.user.id)
        except ObjectDoesNotExist:
            return None
        return product


    def create_product(self,new_name,new_category_id,user):
        product_obj = Product.objects.create(
                name = new_name,
                category_id = new_category_id,
                status = True,
                user = user,
            )
        return product_obj


    def update_product(self,product_id,new_name,new_category_id):
        try:
            product_obj = Product.objects.get(id = product_id)
        except ObjectDoesNotExist:
            return None

        product_obj.category_id = new_category_id
        product_obj.name = new_name
        product_obj.status = True
        product_obj.save()

        return product_obj

    def delete_product(self,p_id):
        try:
            product_obj = Category.objects.get(id = p_id)
        except ObjectDoesNotExist:
            return False
        product_obj.delete()
        return True


class Product_type_interface():
    def decrease_stock_for_product_type_id_using_id_and_quantity(self, product_type_id, quantity):
        product_type_object = Product_type.objects.get(id=product_type_id)
        current_stock = product_type_object.stock - quantity
        product_type_object.stock = current_stock
        product_type_object.save()
        return product_type_object.stock

    def get_product_type(self,request):
        product_type_list = Product_type.objects.filter(user = request.user.id)
        return product_type_list

    def change_stock(self,product_type_id,stock):
        product_type_obj = Product_type.objects.get(id = product_type_id)
        product_type_obj.stock = stock
        product_type_obj.save()
        return True

    def change_status(self,product_type_id,status):
        product_type_obj = Product_type.objects.get(id = product_type_id)
        product_type_obj.status = status
        product_type_obj.save()
        return True

    def get_all_product_type(self):
        return  Product_type.objects.filter(status = 1)

    def get_product_type_by_product(self,request,product_id):
        product_type_list = Product_type.objects.filter(user = request.user.id,product_id = product_id)
        return product_type_list

    def get_product_type_by_product_id(self,product_id):
        return Product_type.objects.filter(product_id = product_id, status =1)

    def get_all_product_type_by_product_id(self, product_id):
        return Product_type.objects.filter(product_id = product_id)

    def create_product_type(self,new_Product_id,new_name,new_content,new_stock,new_cost,mrp,product_image,pack_size,unit,user):
        product_type_key = Product_type_interface().create_product_type_key(new_name)
        product_type_obj = Product_type.objects.create(
                product_type_key  = product_type_key ,
                product_id = new_Product_id,
                name = new_name,
                image = product_image,
                content = new_content,
                stock = new_stock,
                cost = new_cost,
                mrp=mrp,
                pack_size = pack_size,
                unit = unit,
                status = True,
                user = user,
            )
        return product_type_obj

    def update_product_type(self,new_Product_id,new_name,product_type_key,new_content,new_stock,new_cost,mrp,product_image,pack_size,unit):
        try:
            product_type_obj = Product_type.objects.get(id = new_Product_id)
        except ObjectDoesNotExist:
            return None
        product_type_obj.name = new_name
        product_type_obj.content=new_content
        product_type_obj.product_type_key = product_type_key
        product_type_obj.stock = new_stock
        product_type_obj.cost = new_cost
        product_type_obj.mrp = mrp
        product_type_obj.image = product_image
        product_type_obj.pack_size = pack_size
        product_type_obj.unit = unit
        product_type_obj.save()

        return product_type_obj

    def create_product_type_key(self,name):
        product_type_name = config_user.idfy(name)
        try:
            product_type_obj = Product_type.objects.get(product_type_key = product_type_name)
        except ObjectDoesNotExist:
            return product_type_name
        product_type_name = product_type_name +  config_user.random_letter()
        return Product_type_interface().create_product_type_key(product_type_name)




    def delete_product_type(self,pt_id):
        try:
            product_tpye_obj = Category.objects.get(id = pt_id)
        except ObjectDoesNotExist:
            return False
        product_tpye_obj.delete()
        return True

    def get_product_type_by_id(self, product_type_id):
        product_type = Product_type.objects.get(id = product_type_id)
        return product_type

    def filter_product_type_by_user_id(self,business_user_id):
        product_types_list = Product_type.objects.filter(user=business_user_id)
        return product_types_list

    def get_product_type_by_user_id(self,business_user_id,product_type_key ):
        try:
            product_type = Product_type.objects.get(product_type_key  = product_type_key ,user=business_user_id)
        except:
            product_type = None
        return product_type

    def get_product_type_object_by_product_type_key(self, product_type_key):
        product_type_object = Product_type.objects.get(product_type_key  = product_type_key)
        return product_type_object