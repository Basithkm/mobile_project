from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.decorators import login_required

# Create your views here.



# def index(request):
#     product= MobilePuoch.objects.all()
#     context ={
#         'product':product
#     }
#     return render(request,'store/index.html',context)


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



def cart(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)


    total = sum(item.product.offer_price * item.quantity for item in cart_items)

    return render(request, 'store/cart.html', {'cart_items': cart_items,"total": total})



def add_to_cart(request, product_id):
    product = MobilePouch.objects.get(id=product_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
        session_key = request.session.session_key
    cart_item, created = CartItem.objects.get_or_create(session_key=session_key, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return JsonResponse({'success': True})


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return JsonResponse({'success': True})



from django.views.decorators.http import require_POST

@require_POST
def update_cart_item_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    new_quantity = int(request.POST.get('quantity', 0))
    if new_quantity > 0:
        cart_item.quantity = new_quantity
        cart_item.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    


# sum(item.product.offer_price * item.quantity for item in cart_items)