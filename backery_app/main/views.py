# main/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Product, CartItem, Order, OrderItem
from datetime import datetime
from django.db import transaction
from django.db.models import Q

def home(request):
    products = Product.objects.all()
    query = request.GET.get('q') 

    if query:
        
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
        if not products.exists():
            messages.info(request, f"No products found matching '{query}'.")
    
    return render(request, 'home.html', {'products': products, 'query': query})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome!")
            return redirect('home')
        else:
            pass
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price_calculated for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart!")
    return redirect('home')

@login_required
def increase_quantity(request, product_id):
    cart_item = get_object_or_404(CartItem, user=request.user, product__id=product_id)
    cart_item.quantity += 1
    cart_item.save()
    messages.info(request, f"Quantity of {cart_item.product.name} increased.")
    return redirect('cart')

@login_required
def decrease_quantity(request, product_id):
    cart_item = get_object_or_404(CartItem, user=request.user, product__id=product_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.info(request, f"Quantity of {cart_item.product.name} decreased.")
    else:
        product_name = cart_item.product.name
        cart_item.delete()
        messages.warning(request, f"{product_name} removed from cart.")
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, user=request.user, product__id=product_id)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.error(request, f"{product_name} removed from cart.")
    return redirect('cart')

@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect('cart')

    total_price = sum(item.total_price_calculated for item in cart_items)

    current_datetime = datetime.now()

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        upi_id = request.POST.get('upi_id')

        if not payment_method:
            messages.error(request, "Please select a valid payment method.")
            return render(request, 'checkout.html', {
                'cart_items': cart_items,
                'total_price': total_price,
                'current_datetime': current_datetime
            })

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_amount=total_price,
                payment_method=payment_method,
                upi_id=upi_id if payment_method == 'upi' else None
            )

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price_at_purchase=cart_item.product.price
                )

            CartItem.objects.filter(user=request.user).delete()

        messages.success(request, f"Your order has been placed successfully via {payment_method.upper()}!")
        return redirect('order_success')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'current_datetime': current_datetime
    })

def order_success_view(request):
    """
    Displays a success message after an order has been placed.
    """
    return render(request, 'order_success.html')
