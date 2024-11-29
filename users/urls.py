from django.urls import path
from users.views import RegisterView, LoginView, LogoutView
from .views import *
app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Kullanıcı kayıt
    path('login/', LoginView.as_view(), name='login'),  # Kullanıcı giriş
    path('logout/', LogoutView.as_view(), name='logout'),  # Kullanıcı çıkış
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Yeni token alma
]