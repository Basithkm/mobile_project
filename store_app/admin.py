from django.contrib import admin
from . models import *
from . import models


# Register your models here.



@admin.register(models.MobilePouch)
class MobileModelAdmin(admin.ModelAdmin):
    list_filter =['brand_name','phone_name','cover_type']
    list_display =['product_name','phone_name','brand_name','cover_type','price','offer_price','available']
    search_fields =['product_name','phone_name__phone_name__exact','brand_name__brand_name__exact']


    list_per_page = 25


@admin.register(models.MobileBrand)
class MobileBranchAdmin(admin.ModelAdmin):
    list_display =['id','brand_name','cover_image_brand']
    list_per_page = 25
    search_fields =['brand_name']
    



@admin.register(models.CoverType)
class CoverTypeAdmin(admin.ModelAdmin):
    list_display =['id','cover_type']
    list_per_page = 25
    search_fields =['cover_type']


@admin.register(models.PhoneName)
class PhoneNameAdmin(admin.ModelAdmin):
    list_display =['phone_name','brand_name']
    list_per_page = 25
    list_filter =['brand_name','phone_name']
    search_fields =['phone_name','brand_name__brand_name__exact']



@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display =['id','user','product','offer_price','quantity','total_cost']
    list_per_page = 25
    # search_fields =['cover_type']


    def offer_price(self,product):
        return product.product.offer_price



@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display =['id','user','created_at']
    list_per_page = 25



@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display =['id','product','delivary_address','offer_price','quantity','total','user']
    list_per_page = 25


    def offer_price(self,product):
        return product.product.offer_price
    

    def user(self,product):
        return product.order.user




@admin.register(models.Address)
class AddressItemAdmin(admin.ModelAdmin):
    list_display =['name','phone','place','district','payment_type','total_checkout_price']
    list_per_page = 25



# admin.site.register(Cart)
# admin.site.register(CartItem)
# admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(Address)