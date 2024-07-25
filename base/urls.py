from django.urls import path
from .views import *

app_name = 'base'

urlpatterns = [
    path('', home_page, name='home'),
    path('products/<url>', shop_page, name='shop'),
    path('digital/product/<pid>/<id>/', detail_product, name='product'),
    path('cart', product_list, name='cart'),
    path('delete_item/<pk>/', delete_item, name='deleteitem'),
    path('add_to_cart/<pk>/<url>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
    #path('seccess/payment/', seccess_pay, name='seccess_pay'),
    #path('failed/payment/', failed_pay, name='failed_pay'),

]
