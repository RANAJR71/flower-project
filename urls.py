from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # 🔐 Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # 🌸 Pages
    path('flowers/', views.flowers, name='flowers'),
    path('shopplants/', views.shopplants, name='shopplants'),
    path('weddings/', views.weddings, name='weddings'),
    path('workshop/', views.workshop, name='workshop'),

    # 📦 Orders & Reports
    path('orders/', views.orders, name='orders'),
    path('reports/', views.reports, name='reports'),

    # 🛒 Cart
    path('cart/', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # ⚡ Buy Now
    path('buy/<int:flower_id>/', views.buy_now, name='buy_now'),

    # 💳 Checkout & Payment
    path('checkout/', views.payment, name='checkout'),   # ✅ ADD THIS LINE
    path('payment/', views.payment, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
]
