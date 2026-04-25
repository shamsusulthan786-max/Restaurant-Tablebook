"""
URL configuration for restaurant_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import JsonResponse
import cloudinary.uploader
import os

def debug_cloudinary(request):
    return JsonResponse({
        'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME', 'NOT SET'),
        'api_key': os.environ.get('CLOUDINARY_API_KEY', 'NOT SET'),
        'api_secret_set': 'YES' if os.environ.get('CLOUDINARY_API_SECRET') else 'NOT SET',
    })

def debug_cloudinary_upload(request):
    try:
        result = cloudinary.uploader.upload(
            "https://res.cloudinary.com/demo/image/upload/sample.jpg",
            folder="test"
        )
        return JsonResponse({'status': 'success', 'url': result['secure_url']})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


urlpatterns = [
    path('debug-cloud/', debug_cloudinary),
    path('debug-upload/', debug_cloudinary_upload),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('bookings/', include('bookings.urls')),
    path('adminpanel/', include('adminpanel.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

