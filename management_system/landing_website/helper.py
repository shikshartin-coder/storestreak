from Business.data_interface import Business_interface

def convert_product_type_to_dict(product_type):
    business_object = Business_interface().get_business_by_user_id(product_type.user)
    return_dict = {
        'name':str(product_type.name),
        'image':str(product_type.image),
        'key':str(business_object.business_key+"/"+product_type.product_type_key),
        'owner':str(business_object.Business_name),
    }

    return return_dict

def convert_business_to_dict(business):
    return_dict = {
        'name':str(business.Business_name),
        'image':str(business.dp_image),
        'key':str(business.business_key),
        'owner':str(business.category),
    }
    return return_dict

def process_product_type_list_for_dict(product_type_list):
    return_list = []
    for product_type in product_type_list:
        return_list.append(convert_product_type_to_dict(product_type))
    return return_list

def process_business_list_for_dict(business_list):
    return_list = []
    for business in business_list:
        return_list.append(convert_business_to_dict(business))

    return return_list
