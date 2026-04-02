from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('catalogos/', include('catalogos.urls')),
    path('ventas/', include('ventas.urls')),
]
