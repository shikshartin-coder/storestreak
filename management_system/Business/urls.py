from django.urls import path,include
from  Business import views

urlpatterns = [
    path('business-signup',views.business_signup,name="business-signup"),
    path('business-login',views.login_view,name="business-login"),
    path('business-logout',views.logout_view,name="business-logout"),
    path('business-inventory',views.inventory_view,name="inventory"),
    path('business-inventory/<part>',views.inventory_view,name="inventory_view"),
    path('edit-category/<category_id>',views.edit_category,name="edit_category"),
    path('business-edit/<product_id>',views.inventory_edit,name="inventory_edit"),
    path('edit-product/<product_type_id>',views.edit_product_type,name="edit_product"),
    path('manage-orders',views.manage_orders,name="manage_order"),
    path('manage-orders/<order_id>',views.order_page,name="order_page"),
    path('subscribers',views.subscribers,name="subscribers"),
    path('settings',views.settings_view,name="settings"),
    path('profile-business/<user_id>',views.profile_view,name="profile_view"),
    #path('payment-settings',views.payment_settings,name="payment_settings"),
    path('delivery-settings',views.delivery_settings,name="delivery_settings"),

]