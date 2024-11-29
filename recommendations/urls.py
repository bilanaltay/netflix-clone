from django.urls import path
from .views import add_to_favorites, list_favorites, recommended_movies_view

urlpatterns = [
    path('favorites/', list_favorites, name='list-favorites'),  # Favori filmleri listele
    path('add-to-favorites/<int:movie_id>/', add_to_favorites, name='add-to-favorites'),  # Favorilere film ekle
    path('recommendations/', recommended_movies_view, name='recommended-movies'),
]
