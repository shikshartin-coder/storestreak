from django.urls import path,include
from  Customer import views

urlpatterns = [
    path('customer-settings', views.customer_settings, name="customer_settings"),
    path('subscribed-businesses',views.subscribed_businesses, name='subscribed_businesses'),
    path('customer-signup',views.customer_signup,name="customer-signup"),
    path('customer-login',views.login_view,name="customer-login"),
    path('customer-login/<return_link>',views.login_view,name="customer-login"),
    path('customer-logout',views.logout_view,name="customer-logout"),
    path('homepage', views.homepage, name="homepage"),
    path('cart/<business_key>', views.cart_view, name="cart"),
    path('confirm-order', views.confirm_order, name="confirm_order"),
    path('orders', views.order_view, name="order"),
    path('orders/<order_id>', views.customer_order_page, name="customer_order_page"),
    path('subscribe/<business_key>/<action>', views.subscribe, name="subscribe"),
    path('customer-signup/<return_link>',views.inside_signup,name="inside_signup"),
    path('customer-verify',views.inside_signup,name="inside_signup"),
    path('payment',views.payment_view,name="payment_view"),
    path('handel-payment',views.handelpayment,name="handelpayment"),
    path('order_placed/<orderid>', views.success, name="success"),
    path('payment-failure/<orderid>',views.failure, name="failure"),
    path('<business_key>', views.catalog, name="catalog"),
    path('<business_key>/<product_key>', views.product, name="product"),
    path('<business_key>/', views.catalog, name="catalog"),
    path('<business_key>/<product_key>/', views.product, name="product"),
]