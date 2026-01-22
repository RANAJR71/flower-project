from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Flower, Order, Profile


# =====================
# 🔐 LOGIN
# =====================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "shop/login.html")


# =====================
# 🔓 LOGOUT (POST only)
# =====================
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("home")


# =====================
# 🏠 HOME
# =====================
@login_required(login_url="login")
def home(request):
    return render(request, "shop/home.html")


# =====================
# 🌸 FLOWERS
# =====================
@login_required(login_url="login")
def flowers(request):
    flowers = Flower.objects.all()
    return render(request, "shop/flowers.html", {"flowers": flowers})


# =====================
# 📊 REPORTS
# =====================
@login_required(login_url="login")
def reports(request):
    return render(request, "shop/reports.html")


# =====================
# 🌿 EXTRA PAGES
# =====================
@login_required(login_url="login")
def shopplants(request):
    return render(request, "shop/shopplants.html")


@login_required(login_url="login")
def weddings(request):
    return render(request, "shop/weddings.html")


@login_required(login_url="login")
def workshop(request):
    return render(request, "shop/workshop.html")


# =====================
# 📝 REGISTER
# =====================
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Username and password required")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        Profile.objects.create(
            user=user,
            phone=phone,
            address=address,
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "shop/register.html")


# =====================
# 🛒 CART
# =====================
@login_required(login_url="login")
def cart_view(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total = 0

    for flower_id, qty in cart.items():
        flower = get_object_or_404(Flower, id=flower_id)
        item_total = flower.price * qty
        total += item_total

        cart_items.append({
            "flower": flower,
            "quantity": qty,
            "total_price": item_total,
        })

    return render(request, "shop/cart.html", {
        "cart_items": cart_items,
        "total": total,
    })


@login_required(login_url="login")
def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    cart[product_id] = cart.get(product_id, 0) + 1
    request.session["cart"] = cart

    return redirect("cart")


@login_required(login_url="login")
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]
        request.session["cart"] = cart

    return redirect("cart")


# =====================
# 📦 ORDERS
# =====================
@login_required(login_url="login")
def orders(request):
    flowers = Flower.objects.all()
    orders = Order.objects.filter(user=request.user).order_by("-id")

    return render(request, "shop/orders.html", {
        "flowers": flowers,
        "orders": orders,
    })


# =====================
# ⚡ BUY NOW
# =====================
@login_required(login_url="login")
def buy_now(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)

    # Direct checkout for one item
    request.session["checkout_cart"] = {
        str(flower.id): 1
    }

    return redirect("payment")


# =====================
# 💳 PAYMENT
# =====================
@login_required(login_url="login")
def payment(request):
    cart = request.session.get("checkout_cart", {})
    cart_items = []
    total = 0

    for flower_id, qty in cart.items():
        flower = get_object_or_404(Flower, id=flower_id)
        item_total = flower.price * qty
        total += item_total

        cart_items.append({
            "flower": flower,
            "quantity": qty,
            "total_price": item_total,
        })

    if request.method == "POST":
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                flower=item["flower"],
                quantity=item["quantity"],
                customer_name=request.user.username,
                phone="N/A",
                address="Pickup",
                order_type="Buy Now",
            )

        request.session["checkout_cart"] = {}
        messages.success(request, "Payment successful!")
        return redirect("payment_success")

    return render(request, "shop/payment.html", {
        "cart_items": cart_items,
        "total": total,
    })


# =====================
# ✅ PAYMENT SUCCESS
# =====================
@login_required(login_url="login")
def payment_success(request):
    orders = Order.objects.filter(user=request.user).order_by("-id")[:5]
    return render(request, "shop/payment_success.html", {
        "orders": orders
    })
