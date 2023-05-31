from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Account as User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404






# Create your views here.

def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email = email, password = password)

        if user is not None:
            login(request, user)
            return redirect("/")

        else:
            messages.info(request, 'invalid credentials')
            return redirect('signin')

    else:
        return render(request, 'registration/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name'] 
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        print(first_name, phone_number)

        if password1 == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request, 'email taken')
                return redirect('register')

            elif User.objects.filter(phone_number = phone_number).exists():
                messages.info(request,'phone number taken')
                return redirect('register')
            
            else:
                user = User.objects.create_user(phone_number = phone_number, password  = password1, email = email, first_name = first_name)
                user.save()
                messages.success(request, 'Account registered succesfully. Please to signin...')
                return redirect('signin')      
        else:
            messages.info(request, 'Password not match')
            return redirect('register')

    else:
        return render(request, 'registration/register.html')
    


def signout(request):
    logout(request)
    messages.success(request, 'Account Logout Successfully .....')
    return redirect('signin')


    

# user activation email verification
# def activate_email(request,uidb64, token):
#     try:
#         uid=urlsafe_base64_decode(uidb64).decode()
#         user=User.objects.get(pk=uid) 

#     except(TypeError,ValueError,OverflowError,User.DoesNotExist):
#         user=None

#     if user is not None and default_token_generator.check_token(user,token):
#         user.is_active=True
#         user.save()
#         messages.success(request, 'Account registered succesfully. Please to signin...')
#         return redirect('signin')
#     else:
#         messages.error(request, 'Link expired! Please try again ..')
#         return redirect('register')

# # def home(request):
# #     return render(request, 'index.html')    




# def add_post(request):
#     if request.user.is_authenticated:
#         return render(request,'add_post.html')
#     else:
#         return redirect('signin')


# def get_my_account(request):
#     if request.user.is_authenticated:
#         user = User.objects.get(email=request.user.email)
#         user =request.user
#         sale_products =SellProperty.objects.filter(user=user)
#         rent_products = RentProperty.objects.filter(user=user) 
#         form =User.objects.get(id=user.id)
#         context ={
#             'form':form ,
#             'rent_products':rent_products,
#             'sale_products':sale_products
#         }
#         if request.method == 'POST':
#             phone_number =request.POST['phone_number']
#             user.phone_number = phone_number
#             if User.objects.filter(phone_number = phone_number).exists():
#                 messages.info(request, 'phone already number taken')
#                 return redirect('get_my_account')
#             user.save()
#             messages.success(request, 'phone number added successfully')
#             return redirect('get_my_account')
#         # person = get_object_or_404(User,id=pk)
#         return render(request,'my_account.html',context)
#     else:
#         return redirect('signin')
    

# def update_account(request):
#     user = User.objects.get(email=request.user.email)
#     if request.method == 'POST':
#         phone_number =request.POST['phone_number']
#         user.phone_number = phone_number
#         user.save()
#         return redirect('get_my_account')
#     return render(request,'update_account.html')







