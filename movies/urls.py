from django.urls import path
from .views import *

urlpatterns = [
    path('movies/', movie_list, name='movie-list'),  # Tüm filmleri listeleme
    #Listem için
    path('my-list/', user_movie_list, name='user-movie-list'),  # Kullanıcının film listesi
    path('add-to-list/<int:movie_id>/', add_movie_to_list, name='add-movie-to-list'),  # Film ekleme
    path('remove-from-list/<int:movie_id>/', remove_movie_from_list, name='remove-movie-from-list'),  # Film silme
    # İzleme geçmişi için:
    path('watch-history/', user_watch_history, name='user-watch-history'),  # İzleme geçmişini listele
    path('add-to-watch-history/<int:movie_id>/', add_to_watch_history, name='add-to-watch-history')
]