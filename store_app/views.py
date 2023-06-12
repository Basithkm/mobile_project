from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
import razorpay
from mobile_project.settings import (RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET)


# Create your views here.



def index(request):
    product= MobileBrand.objects.all()
    context ={
        'brand_products':product
    }
    return render(request,'store/index.html',context)


def filter_brand(request,id):
    product = PhoneName.objects.filter(brand_name=id)
    context ={
        'phone_product':product
    }
    return render(request,'store/brand_page.html',context)



def filter_phone(request,id):
    product = MobilePouch.objects.filter(phone_name=id)
    context ={
        'pouch_product':product
    }
    return render(request,'store/brand_page.html',context)




def spaceautocomplete(request):
    if request.method == 'GET':
        # Retrieve search query from GET request
        query = request.GET.get('term', '')

        # Filter products based on search query
        products = MobilePouch.objects.filter(
            phone_name__phone_name__icontains=query,
            brand_name__brand_name__icontains=query,
            product_name__icontains=query
        )


        data = []
        for product in products:
            data.append(product.product_name)
            data.append(product.phone_name.phone_name)
            data.append(product.brand_name.brand_name)
            
  
            

        # Remove duplicates and empty strings
        data = list(set(filter(None, data)))

        # Return data as JSON response
        return JsonResponse(data, safe=False)
    

def search(request):
    if request.method == 'GET':
 
        # Retrieve search query from GET request
        query = request.GET.get('query', '')

        # Filter products based on search query
        products = MobilePouch.objects.filter(phone_name__phone_name__icontains=query)

        context = {

            'search_product':products,
        }
           
    context = {

            'search_product':products,
 
        }
    return render(request,'store/brand_page.html', context)


def product_inner_page(request,id):

    product = MobilePouch.objects.get(id=id)
    context ={
        'product':product
    }
    return render(request,'store/product_inner_page.html',context)



# def cart(request):
#     session_key = request.session.session_key
#     cart_items = CartItem.objects.filter(session_key=session_key)
#     total = sum(item.product.offer_price * item.quantity for item in cart_items)
#     return render(request, 'store/cart.html', {'cart_items': cart_items,"total": total})



# def add_to_cart(request, product_id):
#     product = MobilePouch.objects.get(id=product_id)
#     session_key = request.session.session_key
#     if not session_key:
#         request.session.cycle_key()
#         session_key = request.session.session_key
#     cart_item, created = CartItem.objects.get_or_create(session_key=session_key, product=product)
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#     return JsonResponse({'success': True})





def delete_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return JsonResponse({'success': True})


def add_to_cart_item(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(MobilePouch, id=id)
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            user=request.user,
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse({'success': True})
    else:
        return render(request,'registration/login.html')
    


def add_to_cart(request, id):
    cart_item = get_object_or_404(CartItem, id=id,user=request.user)
    if request.user.is_authenticated:
        user=request.user
        cart_item.quantity += 1
        cart_item.save()
        return redirect("cart_detail")
        # return JsonResponse({'success': True})
    else:
        url = reverse('signin') 
        return redirect(url)
    


def remove_from_cart(request, id):
    cart_item = get_object_or_404(CartItem, id=id, user=request.user)
    if request.user.is_authenticated:
        user=request.user
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect("cart_detail")
        # return JsonResponse({'success': True})
    else:
        url = reverse('signin') 
        return redirect(url)
    

def cart_detail(request):
    if request.user.is_authenticated:
        user=request.user
        cart_items = CartItem.objects.filter(user=request.user)

        total = sum(item.product.offer_price * item.quantity for item in cart_items)

        return render(request,"store/cart.html", {
            "cart_items": cart_items,
            "total": total, 
        })
    
    else:
        url = reverse('signin') 
        return redirect(url)






def checkout(request):
    if request.user.is_authenticated:
        user=request.user
        cart_items = CartItem.objects.filter(user=request.user)
        total = sum(item.product.offer_price * item.quantity for item in cart_items)
        if request.method == 'POST':
            if request.POST.get('total_checkout_price') != '0':
                if request.POST.get('payment_type')=="cod":
                    total_checkout_price = request.POST.get('total_checkout_price')
                    name = request.POST.get('name')
                    address = request.POST.get('address','')
                    phone = request.POST.get('phone')
                    place = request.POST.get('place')
                    district = request.POST.get('district')
                    payment_type = request.POST.get('payment_type')
            
                    if total_checkout_price:
                        add = Address.objects.create(user=request.user,
                                                total_checkout_price=total_checkout_price,
                                                  address=address,name=name,phone=phone,
                                                  place=place,district=district,
                                                  payment_type=payment_type)



                        order = Order.objects.create(user=request.user)
                        for cart_item in cart_items:
                            OrderItem.objects.create(user=user,order=order, delivary_address=add,product=cart_item.product, quantity=cart_item.quantity)
                        
                        cart_items.delete()

                        return HttpResponse("cod ordersuccess")
                    
                elif request.POST.get('payment_type')=="paypal":

                    total_checkout_price = request.POST.get('total_checkout_price')
                    name = request.POST.get('name')
                    address = request.POST.get('address')
                    phone = request.POST.get('phone')
                    place = request.POST.get('place')
                    district = request.POST.get('district')
                    payment_type = request.POST.get('payment_type')

                    client = razorpay.Client(auth=('rzp_test_8UagrbDvjbAaIv','GF9RtYsotv4MB175buR2udiP'))
                    razorpay_order = client.order.create(
                        {"amount": float(total_checkout_price) * 100, "currency": "INR", "payment_capture": "1"}
                    )
                    order = Address.objects.create(
                            total_checkout_price=total_checkout_price,
                                                    address=address,name=name,phone=phone,
                                                    place=place,district=district,
                                                    payment_type=payment_type,
                                                        provider_order_id=razorpay_order["id"]
                        )
                    order.save()
                    return render(request,"pay/payment.html",{"callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
                        "razorpay_key": "rzp_test_8UagrbDvjbAaIv",
                        "order": order,
                        },
                        )
                return render(request, "pay/payment.html")

                        

                    

                    # if address:
                    #     order = Order.objects.create(user=request.user)
                    #     for cart_item in cart_items:
                    #         OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
                    #     Address.objects.create(user=request.user,
                    #                                 total_checkout_price=total_checkout_price,
                    #                                 address=address,name=name,phone=phone,
                    #                                 place=place,district=district,
                    #                                 payment_type=payment_type)
                        
                    #     cart_items.delete()
                    #     return HttpResponse("paypal ordersuccess")   

            # else:
            #     return HttpResponse("your amount zero")





        context ={
            "cart_items": cart_items,
            "total": total, 
        }

        return render(request, "store/checkout.html",context)
    else:
        url = reverse('signin') 
        return redirect(url)




def my_order(request):
    if request.user.is_authenticated:
        user=request.user
        orders = OrderItem.objects.filter(user=request.user)
        
        # a= orders.request.quantity

        # print(orders)
        total = sum(item.product.offer_price * item.quantity for item in orders)
        return render(request, "store/my_order.html", {
            "orders": orders,
            "total": total, 
        })
    else:
        url = reverse('signin') 
        return redirect(url)



# def order_payment(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         amount = request.POST.get("amount")
#         client = razorpay.Client(auth=('rzp_test_8UagrbDvjbAaIv','GF9RtYsotv4MB175buR2udiP'))
#         razorpay_order = client.order.create(
#             {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
#         )
#         order = Order.objects.create(
#             name=name, amount=amount, provider_order_id=razorpay_order["id"]
#         )
#         order.save()

#         return render(request,"payment.html",{"callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
#                 "razorpay_key": "rzp_test_8UagrbDvjbAaIv",
#                 "order": order,
#             },
#         )
    

#     return render(request, "pay/payment.html")




@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=('rzp_test_8UagrbDvjbAaIv','GF9RtYsotv4MB175buR2udiP'))
        print(response_data)
        return client.utility.verify_payment_signature(response_data)
        
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        
        order = Address.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()

        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()

            return render(request, "pay/callback.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()

            return render(request, "pay/callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Address.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE

        return render(request, "pay/callback.html", context={"status": order.status})