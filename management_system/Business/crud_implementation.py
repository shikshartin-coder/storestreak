from .import models
from .models import Business, Product_type, Product

class BusinessImplementation(Business):
    
    def get_business_for_id(self, business_id):
        business = Business.objects.get(id = business_id)
        return business

    def get_business(self):
        business_list = Business.objects.all()
        return business_list

    def create_business(self,new_business_name,new_name,new_mobile,new_user_id):
        try:
            business_obj = Business.objects.create(
                Business_name = new_business_name,
                name = new_name,
                mobile = new_mobile,
                 user= new_user_id,
            )
        except:
            business_obj = None
        return business_obj

    def update_business(self,b_id,new_business_name,new_name,new_mobile):
        try:
            business_obj = Category.objects.get(id = b_id)
        except ObjectDoesNotExist:
            category_obj = None

        if(category_obj != None):
            business_obj.Business_name = new_business_name,
            business_obj.name = new_name,
            business_obj.mobile = mobile,
            business_obj.save()
        
        return business_obj

    def delete_business(self,b_id):
        try:
            business_obj = Category.objects.get(id = b_id)
        except ObjectDoesNotExist:
            return False
        business_obj.delete()
        return True

class ProductImplementation(Product):

    def get_products_for_business(self, business_id):
        business = BusinessImplementation.get_business_for_id(business_id)
        products = business.products.all()
        return products

class ProductTypeImplementation(Product_type):
    
    def get_product_type_by_id(self, product_type_id):
        product_type = Product_type.objects.get(id = product_type_id)
        return product_type

    def get_product_types_for_business(self, business_id):
        business = BusinessImplementation.get_business_for_id(business_id)
        product_types = business.product_types.all()
        return product_types
        