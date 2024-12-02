from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from users.models import User
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

# Kullanıcı kayıt endpoint'i


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not email or not username or not password:
            return Response({"error": "Tüm alanlar gereklidir"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Bu email zaten kayıtlı"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "Geçersiz email formatı"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(password)  # Şifre validasyonu
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=email, username=username, password=password)
        return Response({"message": "Kullanıcı başarıyla oluşturuldu", "user_id": user.id}, status=status.HTTP_201_CREATED)


# Kullanıcı giriş endpoint'i
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return Response({"error": "Email ve şifre gereklidir"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user is not None:
            if not user.is_active:
                return Response({"error": "Hesabınız aktif değil"}, status=status.HTTP_403_FORBIDDEN)

            # JWT token oluştur
            refresh = RefreshToken.for_user(user)

            # movie_list endpoint'inin URL'sini al
            movie_list_url = reverse('movie-list')  # 'movie-list' URL adını kullanıyoruz.

            return Response({
                "message": "Giriş başarılı",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user_id": user.id,
                "username": user.username,
                "redirect_url": movie_list_url  # movie_list URL'sini döndür
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Geçersiz email veya şifre"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Refresh token'ı al
            refresh_token = request.data["refresh_token"]
            if not refresh_token:
                return Response({"error": "Refresh token eksik"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            # Blacklist'e ekle
            token.blacklist()
            return Response({"message": "Çıkış yapıldı."}, status=200)
        except Exception as e:
            return Response({"error": "Çıkış sırasında hata oluştu."}, status=400)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        tokens = response.data

        # Refresh token'ı cookie'ye ekle
        response.set_cookie(
            "refresh_token",
            tokens["refresh_token"],
            httponly=True,
            secure=False,  # HTTPS kullanıyorsanız True yapın
            max_age=30 * 24 * 60 * 60,  # 30 gün
        )
        return response
