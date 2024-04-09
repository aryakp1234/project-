
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Customer
from django.contrib import messages

def sign_out(request):
    logout(request)
    return redirect('home')

def show_account(request):
    context = {}

    if request.method == 'POST':
        if 'register_submit' in request.POST:
            try:
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email')
                address = request.POST.get('address')
                phone = request.POST.get('phone')

                if User.objects.filter(username=username).exists():
                    messages.error(request, 'User already exists!!!')
                    return redirect('show_account')

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )

                customer = Customer.objects.create(
                    user=user,
                    phone=phone,
                    address=address
                )

                success_message = "User registered successfully!!"
                messages.success(request, success_message)

            except Exception as e:
                error_message = "Invalid credentials"
                messages.error(request, error_message)

        elif 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid user credentials')

    return render(request, 'account.html', context)
