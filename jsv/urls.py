"""
URL configuration for jsv project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403
from django.shortcuts import render
from django.conf import settings    # import settings to use DEBUG and MEDIA_URL
from django.conf.urls.static import static  # import static to use static files    
from accounts.views import home 

def custom_permission_denied_view(request, exception):  # custom 403 view function to render custom_403.html
    return render(request, 'custom_403.html', status=403)

handler403 = custom_permission_denied_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # This makes the home page accessible at /
    path('accounts/', include('accounts.urls')),
    path('requisitions/', include('requisitions.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
