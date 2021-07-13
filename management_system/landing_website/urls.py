from django.urls import path,include
from  landing_website import views

urlpatterns = [
    path('',views.homepage,name="home"),
    path('forgot-password', views.forgot_password, name="forgot-password"),
    path('add-address/<id>', views.add_address_view, name="add-address"),
    path('address-list', views.address_list_view, name="address-list"),
    path('change-password', views.change_password, name="change-pass"),    
    path('change-password/<message>', views.change_password, name="change-password"),
    path('contact-us',views.contact,name="contact"),
    path('about-us',views.about,name="about"),
    path('search',views.search, name="search"),
]

