from django.db import models
from django.conf import settings
from movies.models import Movie  # Movie modelini kullanıyoruz

class FavoriteMovie(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")  # Kullanıcı
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="favorited_by")  # Film
    added_at = models.DateTimeField(auto_now_add=True)  # Favorilere eklenme zamanı

    class Meta:
        unique_together = ("user", "movie")  # Aynı kullanıcı aynı filmi birden fazla kez ekleyemez
        verbose_name = "Favorite Movie"
        verbose_name_plural = "Favorite Movies"

    def __str__(self):
        return f"{self.user.username} favorited {self.movie.name}"