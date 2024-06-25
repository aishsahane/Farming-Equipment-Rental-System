# Create your views here.
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.http import JsonResponse
import pickle
import pandas as pd
from django.contrib import messages
from .forms import SignUpForm, LoginForm, ProductForm, BookingForm , CategorySearchForm
from .models import Product, Booking , Profile
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView , PasswordResetView



def homeView(request):
    return render(request, 'rentalApp/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # Send email notification to the user upon successful registration
            subject = 'Welcome to Our Platform'
            message = f'Hello {username},\n\nYour account has been created.\nThank you for signing up on farmer equipment rental system. We are excited to have you as  user!'
            sender_email = settings.DEFAULT_FROM_EMAIL
            recipient_email = user.email
            send_mail(subject, message, sender_email, [recipient_email])
            messages.success(request, 'Registration successful!')
            return redirect('home')  # Redirect to home page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'rentalApp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print("working")
                login(request, user)
                request.session['login_success'] = True
                # Send email notification to the user upon successful login
                subject = 'Login Successful'
                message = f'Hello {username},\n\nYou have successfully logged in to farmer equipment rental system.'
                sender_email = settings.DEFAULT_FROM_EMAIL
                recipient_email = user.email
                send_mail(subject, message, sender_email, [recipient_email])
                messages.success(request, 'Login successful!')
                return redirect('home')  # Redirect to home page after successful login
    else:
        print("not working")
        form = LoginForm()
    return render(request, 'rentalApp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home') 


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('login')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'rentalApp/forgot_password.html'
    email_template_name = 'registration/password_reset_email.html'  # Use Django's default email template
    subject_template_name = 'registration/password_reset_subject.txt'  # Use Django's default subject template
    success_url = 'password_reset_done'  # URL to redirect after submitting the password reset form


@login_required(login_url='/login/')
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # Set the user attribute
            product.save()
            return redirect('home')  # Redirect to product list page after successful creation
    else:
        form = ProductForm()
    return render(request, 'rentalApp/addproduct.html', {'form': form})


def product_list(request):
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    return render(request, 'rentalApp/productlist.html', {'products': products})



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'rentalApp/product_detail.html', {'product': product})

@login_required(login_url='/login/')
def book_product(request, pk):
    product = Product.objects.get(pk=pk)  # Retrieve the product
    print(product)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        print("reached")
        if form.is_valid():
            booking = form.save(commit=False)
            booking.save()
            print(product.user.email)
            # send booking mail
            subject = 'New Booking for Your Product'
            message = f'Hello {product.user.username},\n\nA new booking has been made for your product "{product.name}".Kindly check your profile for booking details.\n\nThank you!'
            sender_email = settings.DEFAULT_FROM_EMAIL
            recipient_email = product.user.email

            send_mail(subject, message, sender_email, [recipient_email])
            messages.success(request, 'Booking successful!')
            return redirect('home')  # Redirect to success page
        else:
            print(form.errors)
    else:
        form = BookingForm(initial={'rent': product.daily_rental})
    return render(request, 'rentalApp/bookingform.html', {'form': form, 'product': product})


def profile_view(request):
    # Retrieve the profile associated with the current user
    profile = Profile.objects.get(user=request.user)
    
    # Retrieve the products added by the user
    user_products = Product.objects.filter(user=request.user)
    
    # Retrieve the bookings made for the user's products
    bookings_for_products = Booking.objects.filter(product__in=user_products)
    
    # Render the profile template with the profile information and other data
    return render(request, 'rentalApp/profile.html', {
        'profile': profile,
        'user_products': user_products,
        'bookings_for_products': bookings_for_products
    })



def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST' and request.user == product.user:
        product.delete()
    return redirect('profile')


def product_search(request):
    products = Product.objects.all()  # Retrieve all products initially

    if request.method == 'GET':
        form = CategorySearchForm(request.GET)
        if form.is_valid():
            category = form.cleaned_data.get('category')
            if category:
                products = products.filter(category=category)

    return render(request, '_.html', {'form': form, 'products': products})



# for crop prediction

import pickle
from django.shortcuts import render
import numpy as np

def predict_crop(request):
    if request.method == 'POST':
        # Get the input parameters from the form submission
        N = request.POST.get('N')
        P = request.POST.get('P')
        K = request.POST.get('K')
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        ph = request.POST.get('ph')
        rainfall = request.POST.get('rainfall')

        # Check if any of the input parameters are None
        if None in (N, P, K, temperature, humidity, ph, rainfall):
            # Handle the case where any input parameter is missing
            return render(request, 'rentalApp/predict_crop.html', {'error': 'Please provide all input parameters'})

        # Convert input parameters to float
        try:
            N = float(N)
            P = float(P)
            K = float(K)
            temperature = float(temperature)
            humidity = float(humidity)
            ph = float(ph)
            rainfall = float(rainfall)
        except ValueError:
            return render(request, 'rentalApp/predict_crop.html', {'error': 'Invalid input format'})

        # Load the trained Random Forest model
        with open('MLmodel/RandomForest.pkl', 'rb') as file:
            RF_model = pickle.load(file)

        # Predict the crop using the input parameters
        predicted_crop = RF_model.predict([[N, P, K, temperature, humidity, ph, rainfall]])

        # Return the predicted crop to the template
        return render(request, 'rentalApp/predict_crop.html', {'predicted_crop': predicted_crop})

    # Handle the case for GET request or if the form is not submitted
    return render(request, 'rentalApp/predict_crop.html')







