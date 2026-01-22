from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔐 Login / Logout using built-in Django auth views
    path('login/', auth_views.LoginView.as_view(
        template_name='shop/login.html'  # Login template path
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'  # Logout गरेपछि login page मा redirect
    ), name='logout'),

    # 🏠 Shop app URLs
    path('', include('shop.urls')),  # shop app को urls.py include गरियो
]

# ✅ Media files serve in development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
