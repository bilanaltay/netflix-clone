from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Kullanıcı yöneticisi
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email alanı zorunludur")
        if not username:
            raise ValueError("Kullanıcı adı alanı zorunludur")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Süper kullanıcı oluşturur.
        """
        user = self.create_user(email=email, username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# Kullanıcı modeli
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)  # Benzersiz email adresi
    username = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Kullanıcı aktif mi?
    is_admin = models.BooleanField(default=False)  # Admin kullanıcı mı? (varsayılan False)

    # Kullanıcı modelinde özel bir yöneticiyi bağladık
    objects = UserManager()

    # Email alanını kullanıcı adı olarak belirtiyoruz
    USERNAME_FIELD = 'email'  # Giriş için kullanılacak alan
    REQUIRED_FIELDS = ['username']  # createsuperuser için ek zorunlu alanlar

    # Kullanıcıyı string olarak temsil eden method
    def __str__(self):
        return self.email