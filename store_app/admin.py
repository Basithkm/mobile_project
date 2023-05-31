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



# admin.site.register(Cart)
admin.site.register(CartItem)