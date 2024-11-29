from django.db import models
from django.conf import settings  # Kullanıcı modelini almak için


class Actor(models.Model):
    name = models.CharField(max_length=255)  # Oyuncu adı

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)  # Kategori adı

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=255)  # Film adı
    image = models.URLField()  # Film afişi (URL)
    description = models.TextField()  # Film açıklaması
    # Süre (dakika) (PositiveIntegerField de kullanılabilir)
    duration = models.IntegerField()
    director = models.CharField(max_length=255)  # Yönetmen
    cast = models.ManyToManyField(Actor, related_name="movies")  # Oyuncular
    category = models.ManyToManyField(
        Category, related_name="movies")  # Kategoriler

    def __str__(self):
        return self.name


class UserMovieList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="movie_list")  # Kullanıcı
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="user_list")  # Film
    added_at = models.DateTimeField(auto_now_add=True)  # Eklenme zamanı

    class Meta:
        # Aynı kullanıcı aynı filmi birden fazla kez ekleyemez
        unique_together = ("user", "movie")
        verbose_name = "User Movie List"  # Admin paneli için isim
        verbose_name_plural = "User Movie Lists"

    def __str__(self):
        return f"{self.user.username}'s list: {self.movie.name}"


class WatchHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watch_history")  # Kullanıcı
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="watch_history")  # Film
    watched_at = models.DateTimeField(auto_now=True)  # İzleme zamanı (son izlenme)

    class Meta:
        # Aynı kullanıcı aynı filmi birden fazla kez ekleyemez
        unique_together = ("user", "movie")
        verbose_name = "Watch History"
        verbose_name_plural = "Watch Histories"

    def __str__(self):
        return f"{self.user.username} watched {self.movie.name}"
