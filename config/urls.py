"""
URL configuration for config project.

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
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin paneline erişim
    path('', include('movies.urls')),  # Movies uygulamasının URL'lerini dahil et
    path('', include('recommendations.urls')),  # Recommendation app URL'leri
    path('users/', include('users.urls')),  # Users uygulamasının URL'lerini dahil et
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token endpoint
]