from django.urls import path
from . import views
urlpatterns = [    
    path('', views.home, name='home'),
    path('login/',views.login_view ,name='login'),
    path('signup/',views.signup_view ,name='signup'),
    path('logout/',views.logout_view ,name='logout'),
    path('cart/', views.cart_view, name='cart'),  
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/', views.order_success_view, name='order_success'),
]
