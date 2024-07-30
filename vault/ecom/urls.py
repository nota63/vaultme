from django.urls import path
from .views import *

urlpatterns=[

    path("home_page/",home_page,name='home_page'),
    path('item/<int:pk>/', item_detail, name='item_detail'),
    path("address/<int:item_id>/",address,name='address'),
    path("orders/",orders,name='orders'),
    path('add-to-cart/<int:item_id>/',add_to_cart, name='add_to_cart'),
    path('cart/',cart_view, name='cart_view'),
    path("remove_cart/<int:pk>/",remove_cart,name='remove_cart'),
    path("coming_soon/",coming_soon,name='coming_soon'),
    path("cancel/<int:pk>/",cancel,name='cancel'),
    path("change_address/<int:pk>/",change_address,name='change_address'),
    path("raise_help/<int:pk>/",raise_help,name='raise_help'),
    path('request_item/',request_item,name='request_item'),
    path("seller_page/",seller_page,name='seller_page'),
    path("agreement/",agreement,name='agreement'),
    path("set_account/",set_account,name='set_account'),
    path("view_account/",view_account,name='view_account'),
    path("edit_account/<int:pk>/",edit_account,name='edit_account'),
    path("sell_products/",sell_products,name='sell_products'),
    path("delete_products/<int:pk>/",delete_products,name='delete_products'),
    path('update_product/<int:pk>/',update_product,name='update_product'),
    path("notices/",notices,name='notices')

]
