# Ubicación: core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Login como página de inicio
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # 2. Rutas de autenticación de Django
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 3. Tus aplicaciones (Sin namespaces para que los botones funcionen directo)
    path('dashboard/', include('dashboard.urls')),
    path('catalogos/', include('catalogos.urls')),
    path('ventas/', include('ventas.urls')), 
    ]