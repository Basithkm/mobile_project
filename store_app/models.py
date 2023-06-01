from typing import Any
from django.db import models
from PIL import Image
from registration.models import Account
# Create your models here.



class MobileBrand(models.Model):
    brand_name= models.CharField(max_length=255,blank=True,null=True)
    cover_image_brand=models.ImageField(upload_to='main_images_branch',blank=False,null=False)

    def save(self):
        if self.cover_image_brand:          
            super(MobileBrand, self).save()
            cover_image_brand = Image.open(self.cover_image_brand)
            (width , height) = cover_image_brand.size     
            size = (720,480)
            image = cover_image_brand.resize(size, Image.ANTIALIAS)
            image.save(self.cover_image_brand.path)

    def __str__(self) -> str:
        return self.brand_name
    

    

class PhoneName(models.Model):
    brand_name=models.ForeignKey(MobileBrand,on_delete=models.CASCADE)
    phone_name = models.CharField(max_length=255,blank=False,null=False)
    phone_image = models.ImageField(upload_to='phone_images',null=False,blank=False)

    def __str__(self) -> str:
        return self.phone_name  


class CoverType(models.Model):
    cover_type =models.CharField(max_length=255,blank=True,null=True)

    def __str__(self) -> str:
        return self.cover_type

class MobilePouch(models.Model):
    brand_name= models.ForeignKey(MobileBrand,on_delete=models.CASCADE)
    phone_name= models.ForeignKey(PhoneName,on_delete=models.CASCADE)
    product_name =models.CharField(max_length=255,null=False,blank=False)
    cover_type = models.ForeignKey(CoverType,on_delete=models.CASCADE)
    price =  models.DecimalField(max_digits=10, decimal_places=2)
    offer_price =  models.DecimalField(max_digits=10, decimal_places=2)
    cover_image=models.ImageField(upload_to='main_images',blank=False,null=False)
    image1=models.ImageField(upload_to='images',blank=True,null=True)
    image2=models.ImageField(upload_to='images',blank=True,null=True)
    image3=models.ImageField(upload_to='images',blank=True,null=True)
    image4=models.ImageField(upload_to='images',blank=True,null=True)
    available = models.BooleanField(default=True)



    def save(self):
        if self.cover_image:          
            super(MobilePouch, self).save()
            cover_image = Image.open(self.cover_image)
            (width , height) = cover_image.size     
            size = (720,480)
            image = cover_image.resize(size, Image.ANTIALIAS)
            image.save(self.cover_image.path)

        if self.image1:          
            super(MobilePouch, self).save()
            image1 = Image.open(self.image1)
            (width , height) = image1.size     
            size = (720,480)
            image = image1.resize(size, Image.ANTIALIAS)
            image.save(self.image1.path)

        if self.image2:          
            super(MobilePouch, self).save()
            image2 = Image.open(self.image2)
            (width , height) = image2.size     
            size = (720,480)
            image = image2.resize(size, Image.ANTIALIAS)
            image.save(self.image2.path)

        if self.image3:          
            super(MobilePouch, self).save()
            image3 = Image.open(self.image3)
            (width , height) = image3.size     
            size = (720,480)
            image = image3.resize(size, Image.ANTIALIAS)
            image.save(self.image3.path)

        if self.image4:          
            super(MobilePouch, self).save()
            image4 = Image.open(self.image4)
            (width , height) = image4.size     
            size = (720,480)
            image = image4.resize(size, Image.ANTIALIAS)
            image.save(self.image4.path)


    def __str__(self) -> str:
        return self.product_name   





# class CartItem(models.Model):
#     # user = models.ForeignKey(Account, on_delete=models.CASCADE,blank=False,null=False)
#     session_key = models.CharField(max_length=50)
#     product = models.ForeignKey(MobilePouch, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)


#     @property
#     def total_cost(self):
#         return self.quantity * self.product.offer_price


# class Cart(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(Account,on_delete=models.CASCADE)


class CartItem(models.Model):
    product=models.ForeignKey(MobilePouch,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1,null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)

    @property
    def price(self):
        return self.product.offer_price
    
    @property
    def total_cost(self):
        return self.quantity * self.product.offer_price

    def __str__(self):
        return f"{self.quantity} of {self.product.phone_name}"
    


class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.first_name}"







class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    total_checkout_price =models.DecimalField(max_digits=10, decimal_places=2,blank=False,null=False)
    name = models.CharField(max_length=100,blank=False,null=False)
    address = models.CharField(max_length=200,blank=False,null=False)
    phone = models.CharField(max_length=20,blank=False,null=False)
    place = models.CharField(max_length=100,blank=False,null=False)
    district = models.CharField(max_length=100,blank=False,null=False)
    payment_type = models.CharField(max_length=10,blank=False,null=False)
    



    def __str__(self):
        return f"{self.user.first_name}'s Address - {self.name}"



class OrderItem(models.Model):
    delivary_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(MobilePouch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total(self):
        return self.quantity * self.product.offer_price





    
    def __str__(self):
        return f"Order {self.order.id} - {self.product.brand_name}"



# class Checkout(models.Model):
#     user =models.ForeignKey(Account,on_delete=models.CASCADE,null=False)
#     cartitem =models.ForeignKey(CartItem,on_delete=models.CASCADE,null=True)
#     total_checkout_price =models.DecimalField(max_digits=10, decimal_places=2,blank=False,null=False)
#     name = models.CharField(max_length=100,blank=False,null=False)
#     address = models.CharField(max_length=200,blank=False,null=False)
#     phone = models.CharField(max_length=20,blank=False,null=False)
#     place = models.CharField(max_length=100,blank=False,null=False)
#     district = models.CharField(max_length=100,blank=False,null=False)
#     payment_type = models.CharField(max_length=10,blank=False,null=False)

 
#     def __str__(self):
#         return self.name