from .models import Customer,Subscribe,Cart,Orders,Orders_status,Order_Address,Order_products,transaction
from landing_website.data_interface import AddressInterface
from django.core.exceptions import ObjectDoesNotExist
import random

class Customer_Interface():

    def get_customer_id_by_user_id(self,user_id):
        customer_id = Customer.objects.get(user = user_id).id
        return customer_id

    def get_customer_by_id(self,customer_id):
        return Customer.objects.get(id=customer_id)

    def get_customer_by_user_id(self, user_id):
        try:
            customer_object = Customer.objects.get(user = user_id)
        except ObjectDoesNotExist:
            customer_object = None
        return customer_object

    def create_customer(self,new_customer_name,new_mobile,new_user_id):
        customer_object = Customer.objects.create(
                name = new_customer_name,
                mobile = new_mobile,
                user= new_user_id,
            )
        return customer_object

    def get_all_customer(self):
        return Customer.objects.all()

    def get_customer_for_mobile(self, mobile):
        customer_list = Customer.objects.filter(mobile = mobile)
        return customer_list

    def check_user_is_customer(self, mobile):
        customer_list = Customer_Interface().get_customer_for_mobile(mobile = mobile)
        if len(customer_list) == 0:
            return False
        return True

    def update_privacy_settings(self, user_id, bool_val):
        customer_object = Customer.objects.get(user = user_id)
        customer_object.privacy_settings = bool_val
        customer_object.save()

    def get_all_customers_for_a_subscribed_business(self,business_id):
        customer_ids = Subscribe_Interface().get_all_customer_ids_for_a_subscribed_business(business_id)
        customer_objects_list = Customer.objects.filter(id__in=customer_ids).order_by('id')
        return customer_objects_list


class Subscribe_Interface():

    def create_subscribe(self,business_id,customer_id):
        try:
            Subscribe_object =  Subscribe.objects.get( customer_id = customer_id ,business_id = business_id)
        except ObjectDoesNotExist:
            Subscribe_object = Subscribe.objects.create(
                customer_id = customer_id,
                business_id = business_id,
            )
        return Subscribe_object

    def unsubscribe(self,business_id,customer_id):
        try:
            Subscribe_object =  Subscribe.objects.get( customer_id = customer_id ,business_id = business_id)
        except ObjectDoesNotExist:
            return False
        Subscribe_object.delete()
        return True

    def get_user_id_of_subscribe_list(self,user):
        customer_id = Customer_Interface().get_customer_id_by_user_id(user)
        business_id_list = Subscribe.objects.filter(customer_id = customer_id)
        return business_id_list

    def check_subscription(self,customer_id,business_id):
        sub = True
        try:
            sub_obj = Subscribe.objects.get(customer_id=customer_id,business_id=business_id)
        except ObjectDoesNotExist:
            sub = False
        return sub

    def get_all_customer_ids_for_a_subscribed_business(self, business_id):
        return Subscribe.objects.filter(business_id = business_id).values_list('customer_id', flat=True)

    def get_all_business_id_for_a_customer(self, customer_id):
        return Subscribe.objects.filter(customer_id = customer_id).values_list('business_id', flat=True)

    def get_all_subscription_objects_for_business(self, business_id):
        return Subscribe.objects.filter(business_id = business_id).order_by('customer_id')

    def get_all_subscription_objects_for_customer(self, customer_id):
        return Subscribe.objects.filter(customer_id = customer_id).order_by('business_id')


class Cart_Interface():
    def get_customer_cart(self,customer_id,business_id):
        cart = Cart.objects.filter(customer_id = customer_id,business_id = business_id)
        return cart

    def empty_cart(self,all_cart):
        for cart in all_cart:
            Cart.objects.get(id = cart.id)
            cart.delete()


    def create_cart(self,product_type_id,business_id,customer_id,quantity,total_price):
        try:
            cart_obj = Cart.objects.get(product_type_id= product_type_id,business_id=business_id,customer_id =customer_id,quantity=quantity)
        except ObjectDoesNotExist:
            cart_obj = Cart.objects.create(
                product_type_id= product_type_id,
                business_id=business_id,
                customer_id=customer_id,
                quantity=quantity,
                total_price = total_price,
            )
        return cart_obj

    def check_cart_obj(self,product_type_id,business_id,customer_id):
        try:
            cart_obj = Cart.objects.get(product_type_id= product_type_id,business_id=business_id,customer_id =customer_id)
        except ObjectDoesNotExist:
            return None
        return cart_obj

    def get_quantity(self,cart_id):
        cart_obj = Cart.objects.get(id = cart_id)
        return cart_obj.quantity

    def update_quantity(self,cart_id,quantity,total_price):
        cart_obj = Cart.objects.get(id = cart_id)
        cart_obj.quantity = quantity
        cart_obj.total_price = int(total_price)
        cart_obj.save()

        if(int(cart_obj.quantity)<=0):
            cart_obj.delete()

        return cart_obj

class Product_orders_interface():
    def create_product_order(self,order_id,product_type_id,quantity,total_price):
        order_product = Order_products.objects.create(
            order_id=order_id,
            product_type_id=product_type_id,
            quantity=quantity,
            total_price=total_price,
            )
        return order_product

    def get_product_order_by_order_id(self,order_id):
        return Order_products.objects.filter(order_id = order_id)
    
    def get_product_orders_grouped_by_product_type_id_using_business_id_and_active_order_ids(self, business_id):
        order_ids_for_business = Orders_interface().get_order_ids_for_active_orders_using_business_id(business_id=business_id)
        result = Order_products.objects.filter(order_id__in=order_ids_for_business).values('product_type_id').annotate(total_quantity=Sum('quantity'), total_orders=Count('product_type_id'), total_amount=Sum('total_price')).order_by()
        return result

class Orders_interface():
    def create_order(self,product_type_id,business_id,customer_id,quantity,address_id,total_price,order_otp,total_order_amount,delivery_charge,payment,payment_mode):
        order_id = Orders_interface().generate_order_id()
        order_address_id = order_address_interface().copy_address_from_address_table(address_id,order_id)
        order_obj = Orders.objects.create(
            order_id = order_id,
            business_id=business_id,
            customer_id=customer_id,
            address_id = order_address_id.id,
            order_otp = order_otp,
            active = True,
            delivery_charge=delivery_charge,
            total_order_amount = total_order_amount,
            payment=payment,
            payment_mode = payment_mode,
        )
        Product_orders_interface().create_product_order(order_id,product_type_id,quantity,total_price)
        order_status_interface().create_order_status(order_obj.order_id,order_status_interface().one_time_status['s1'],'')
        return order_obj

    def create_cart_order(self,all_cart,address_id,customer_id,business_id,delivery_obj,payment,payment_mode):
        otp = Orders_interface().generate_order_otp()
        order_id = Orders_interface().generate_order_id()
        order_address_id = order_address_interface().copy_address_from_address_table(address_id,order_id)
        total_item_amount = 0
        for cart in all_cart:
            total_item_amount =  total_item_amount + cart.total_price
        delivery_charge_amount = delivery_obj['delivery_charge']
        total_amount =  total_item_amount + delivery_charge_amount
        if(delivery_obj['delivery_type'] == 'custom'):
            if(total_item_amount > delivery_obj['minimum_amount']):
                 total_amount  =  total_item_amount
                 delivery_charge_amount = 0
        order_obj = Orders.objects.create(
            order_id = order_id,
            business_id=business_id,
            customer_id=customer_id,
            address_id = order_address_id.id,
            delivery_charge=delivery_charge_amount,
            total_order_amount = total_amount,
            order_otp = otp,
            active = True,
            payment=payment,
            payment_mode = payment_mode,
            )
        for cart in all_cart:
           order_product =  Product_orders_interface().create_product_order(order_id,cart.product_type_id,cart.quantity,cart.total_price)
        order_status_interface().create_order_status(order_obj.order_id,order_status_interface().one_time_status['s1'],'')
        return order_obj

    def get_total_order_amount(self,order_id):
        return Orders.objects.get(order_id=order_id).total_order_amount

    def change_payment(self,order_id):
        order_obj = Orders.objects.get(order_id = order_id)
        order_obj.payment = True
        order_obj.save()
        return order_obj

    def delete_order(self,order_id):
        order_obj = Orders.objects.get(order_id = order_id,payment=False)
        order_product = Order_products.objects.filter(order_id = order_obj.order_id)
        order_status_obj = Orders_status.objects.filter(order_id = order_obj.order_id)
        order_address_obj = Order_Address.objects.filter(order_id = order_obj.order_id)
        for address in order_address_obj:
            address.delete()
        for status in order_status_obj:
            status.delete()
        for order in order_product:
            order.delete()
        order_obj.delete()

    def check_order_otp(self,otp):
        try:
           order_obj =  Orders.objects.get(order_otp = otp)
        except:
            return False
        return True

    def generate_order_otp(self):
        otp = random.randint(100001,999999)
        if(Orders_interface().check_order_otp(otp)):
            Orders_interface().generate_order_otp()
        return otp

    def verify_otp(self,order_otp,order_id):
        order_obj = Orders_interface().get_order_obj_by_order_id(order_id)
        if(order_obj != None):
            if(int(order_obj.order_otp)==int(order_otp)):
                return True
            else:
                return False
        else:
            return False

    def generate_order_id(self):
        order_id = random.randint(1111,9999)
        try:
            order_obj = Orders.objects.get(order_id = order_id)
        except ObjectDoesNotExist:
            return order_id
        Orders_interface().generate_order_id()


    def get_customer_orders(self,customer_id):
        orders_obj = Orders.objects.filter(customer_id=customer_id,payment=True)
        return orders_obj

    def get_orders_by_business_id_and_status(self, business_id, status):
        order_ids_by_status = order_status_interface().get_order_ids_for_status(status=status)
        return Orders.objects.filter(order_id__in=order_ids_by_status, business_id = business_id, payment=True)


    def get_orders_by_business_id(self,business_id):
        return Orders.objects.filter(business_id = business_id,payment=True)

    def get_order_obj_by_order_id(self,order_id):
        try:
            order = Orders.objects.get(order_id = order_id,payment=True)
        except:
            return None
        return order

    def inactive_order_by_order_id(self,order_id):
        order_list = Orders_interface().get_order_obj_by_order_id(order_id)
        order_list .active = False
        order_list .save()
        return True
    
    def get_all_orders_grouped_by_order_id_annotating_total_price_using_business_id(self, business_id):
        order_ids_for_business = Orders_interface().get_order_ids_for_active_orders_using_business_id(business_id=business_id)
        result = Orders.objects.filter(order_id__in=order_ids_for_business).values('order_id','customer_id').annotate(total_amount=Sum('total_order_amount')).order_by('customer_id')
        #print(result)
        return result


    def get_all_active_orders_using_business_id(self, business_id):
        active_order_ids = order_status_interface().get_order_ids_for_active_orders()
        orders = Orders.objects.filter(order_id__in=active_order_ids, business_id = business_id)
        return orders

    def get_order_ids_for_active_orders_using_business_id(self, business_id):
        active_order_ids = order_status_interface().get_order_ids_for_active_orders()
        order_ids_for_business = Orders.objects.filter(order_id__in=active_order_ids, business_id=business_id).values_list('order_id', flat=True)
        return order_ids_for_business

class order_status_interface():
    one_time_status = {
        's1':'ordered',
        's2':'accepted',
        's3':'rejected',
        's4':'delivered'
    }

    order_status = {
        's1':'Packing',
        's2':'Ready',
        's3':'Out For Delivery',
    }

    def create_order_status(self, order_id,status,reason):
        order_status = False
        if(order_status_interface().deactive_active_status(order_id)):
            order_status = Orders_status.objects.create(
                    order_id = order_id,
                    status = status,
                    active = True,
                    reason = reason,
            )
        return order_status

    def deactive_active_status(self,order_id):
        order_status = Orders_status.objects.filter(order_id = order_id)
        for orders in order_status:
            orders.active = False
            orders.save()
        return True

    def get_active_order_status_by_order_id(self,order_id):
        return Orders_status.objects.get(order_id = order_id,active = True)

    def get_order_status_by_order_id(self,order_id):
        return Orders_status.objects.filter(order_id = order_id)

    def get_order_ids_for_active_orders(self):
        return Orders_status.objects.values_list('order_id', flat=True).filter(active = True, status = order_status_interface().one_time_status['s2'])

    def get_order_ids_for_status(self, status):
        return Orders_status.objects.values_list('order_id', flat=True).filter(status = status, active = True)


class order_address_interface():

    def create_order_address(self,order_id,user_id, name, mobile, pincode, building, street, landmark, city, state, address_type):
        try:
            address_object = Order_Address.objects.create(order_id=order_id,user_id = user_id, name = name, mobile = mobile, pincode = pincode, building = building, street = street, landmark = landmark, city = city, state = state, address_type = address_type)
        except:
            address_object = None
        return address_object

    def copy_address_from_address_table(self,address_id,order_id):
       address_obj =  AddressInterface().get_address_by_id(address_id)
       address_object = order_address_interface().create_order_address(order_id,address_obj.user_id, address_obj.name, address_obj.mobile, address_obj.pincode, address_obj.building, address_obj.street, address_obj.landmark, address_obj.city, address_obj.state, address_obj.address_type)
       return address_object

    def get_order_address_by_id(self,order_id):
        return Order_Address.objects.get(order_id = order_id)

class transaction_interface():

    def create_transaction(self,order_id,txnid,txnamount,paymentmode,currency,txndate,status,respcode,respmsg,gatewayname,banktxnid,bankname,checksumhash):
        try:
            trans_obj = transaction.objects.get(order_id = order_id)
        except:
            trans_obj = transaction.objects.create(
                order_id = order_id,
                txnid=txnid,
                txnamount=txnamount,
                paymentmode=paymentmode,
                currency=currency,
                txndate=txndate,
                status=status,
                respcode=respcode,
                respmsg=respmsg,
                gatewayname=gatewayname,
                banktxnid=banktxnid,
                bankname=bankname,
                checksumhash=checksumhash,
                )

        return trans_obj

    def get_transaction(self,order_id):
        try:
            trans_obj = transaction.objects.get(order_id=order_id)
        except:
            trans_obj = None
        return trans_obj

