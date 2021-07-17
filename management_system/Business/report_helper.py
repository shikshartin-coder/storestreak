from .data_interface import Product_type_interface, Product_interface, Category_interface, Business_interface
from Customer.data_interface import Customer_Interface, order_address_interface, Product_orders_interface, Orders_interface
from downloads.downloads import export_report_xls


def convert_product_report_attributes_to_list(report_query):
    product_object = Product_type_interface().get_product_type_by_id(report_query['product_type_id'])
    category_id = Product_interface().get_category_id_from_product_type_id(report_query['product_type_id'])
    category_object = Category_interface().get_category_by_id(category_id)
    returned_list = [
        str(report_query['product_type_id']),
        str(product_object.name),
        str(category_object.name),
        str(report_query['total_quantity']),
        str(report_query['total_orders']),
        str(report_query['total_amount']),
    ]
    return returned_list

def convert_delivery_report_attributes_to_list(request, report_query):
    customer = Customer_Interface().get_customer_by_id(report_query['customer_id'])
    #customer_order_address = order_address_interface().get_order_address_using_user_id(request.user.id)
    customer_address_object = order_address_interface().get_order_address_by_id(report_query['order_id'])
    customer_address = get_customer_address_for_display_from_address_object(customer_address_object)
    returned_list = [
        str(report_query['order_id']),
        str(report_query['customer_id']),
        str(customer.name),
        None,
        str(report_query['total_amount']),
        str(customer.mobile),
        customer_address,
    ]    
    return returned_list

def process_report_list(request, report_type, report_queryset):
    report_list = []
    for report_query in report_queryset:
        if report_type == 'product':
            returned_list = convert_product_report_attributes_to_list(report_query)
        elif report_type == 'delivery':
            returned_list = convert_delivery_report_attributes_to_list(request, report_query)
        report_list.append(returned_list)
    return report_list

def process_general_report_list(request, report1_queryset):
    report_list = []
    for report1_object in report1_queryset:
        customer = Customer_Interface().get_customer_by_id(report1_object.customer_id)
        customer_id = report1_object.customer_id
        customer_name = customer.name
        order_id = report1_object.order_id
        payment_method = report1_object.payment_mode
        order_amount = report1_object.total_order_amount
        customer_phone = customer.mobile
        customer_address_object = order_address_interface().get_order_address_by_id(order_id)
        customer_address = get_customer_address_for_display_from_address_object(customer_address_object)
        counter = 0
        report2_queryset = Product_orders_interface().get_product_order_by_order_id(order_id)
        for report_objects_num in range(len(list(report2_queryset))):
                if counter != 0:
                    customer_id = None
                    customer_name = None
                    order_id = None
                    payment_method = None
                    order_amount = None
                    customer_phone = None
                    customer_address = None

                product_id = report2_queryset[report_objects_num].product_type_id
                product_object = Product_type_interface().get_product_type_by_id(product_id)
                product_name = product_object.name
                category_id = Product_interface().get_category_id_from_product_type_id(product_id)
                category_object = Category_interface().get_category_by_id(category_id)
                category_name = category_object.name
                total_quantity = report2_queryset[report_objects_num].quantity
                total_amount = report2_queryset[report_objects_num].total_price

                report_list.append([customer_id,customer_name,order_id,payment_method,order_amount,customer_phone,customer_address,product_id,product_name,category_name,total_quantity,total_amount])
                counter += 1
    return report_list

def get_customer_address_for_display_from_address_object(customer_address_object):
    customer_address = str(customer_address_object.building) + ", " + str(customer_address_object.street) + ", " + str(customer_address_object.city) + ", " + str(customer_address_object.state) + "-" + str(customer_address_object.pincode)
    return customer_address

def generate_report(request):
        report_type = request.POST.get('report_type')
        business_object = Business_interface().get_business_by_user_id(request.user.id)
        if report_type == 'product':
            result_list = Product_orders_interface(
            ).get_product_orders_grouped_by_product_type_id_using_business_id_and_active_order_ids(business_object.id)
            #print(result_list)
            report_list = process_report_list(request,
                'product', result_list)
            table_headers_list = ['Product Id', 'Product Name',
                'Category', 'Total Quantity', 'Total Orders', 'Total Amount']
            #print(report_list)

        if report_type == 'delivery':
            result_list = Orders_interface(
            ).get_all_orders_grouped_by_order_id_annotating_total_price_using_business_id(business_object.id)
            report_list = process_report_list(request,
                'delivery', result_list)

            table_headers_list = ['Order Id', 'Customer Id', 'Customer Name', 'Payment Method', 'Order Amount', 'Customer Phone', 'Customer Address']

        if report_type == 'general':
            result_list = Orders_interface().get_all_active_orders_using_business_id(business_object.id)
            report_list = process_general_report_list(request, result_list)

            table_headers_list = ['Customer Id', 'Customer Name', 'Order Id', 'Payment Method', 'Order Amount', 'Customer Phone', 'Customer Address', 'Product Id', 'Product Name',
                'Category', 'Total Quantity', 'Total Amount']

        return export_report_xls(request, report_list, table_headers_list)
