from django.urls import path
from . import views




urlpatterns = [
    path('',views.index,name='index'),
    path('filter_brand/<int:id>/',views.filter_brand,name='filter_brand'),
    path('filter_phone/<int:id>/',views.filter_phone,name='filter_phone'),
    path('spaceautocomplete/', views.spaceautocomplete, name='spaceautocomplete'),
    path('search/', views.search, name='search'),
    path('product_inner_page/<int:id>/', views.product_inner_page, name='product_inner_page'),

    # path('add-to-cart/<int:product_id>/',views.add_to_cart, name='add_to_cart'),
    # path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.delete_from_cart, name='remove_from_cart'),

    # path('c', views.collect, name='collect'),
    

    path("additem/<int:id>/",views. add_to_cart_item, name="add_to_cart_item"),
    path("add/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:id>/",views. remove_from_cart, name="remove_from_cart"),
    path("cart",views. cart_detail,name="cart_detail"),

    
    path("ch",views. checkout, name="checkout"),


    path("o",views. my_order, name="my_order"),


    
    
    


]
