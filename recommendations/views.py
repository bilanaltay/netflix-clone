from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from movies.models import Movie
from .models import FavoriteMovie
from django.core.exceptions import ObjectDoesNotExist
from .utils import get_recommended_movies  # get_recommended_movies fonksiyonunu içe aktar

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_favorites(request, movie_id):
    user = request.user
    try:
        movie = Movie.objects.get(id=movie_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Film bulunamadı."}, status=404)

    # Favorilere ekle
    obj, created = FavoriteMovie.objects.get_or_create(user=user, movie=movie)
    if created:
        return JsonResponse({"message": f"'{movie.name}' favorilerinize eklendi."}, status=201)
    else:
        return JsonResponse({"message": f"'{movie.name}' zaten favorilerinizde."}, status=200)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    user = request.user
    favorites = FavoriteMovie.objects.filter(user=user)

    # Favori filmleri JSON formatına dönüştür
    favorites_list = []
    for favorite in favorites:
        movie = favorite.movie
        favorites_list.append({
            "id": movie.id,
            "name": movie.name,
            "image": movie.image,
            "description": movie.description,
            "category": [category.name for category in movie.category.all()],
            "added_at": favorite.added_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    return JsonResponse(favorites_list, safe=False, json_dumps_params={'ensure_ascii': False})

@api_view(["GET"])
@permission_classes([IsAuthenticated])  # Sadece giriş yapan kullanıcılar erişebilir
def recommended_movies_view(request):
    """
    Kullanıcının favori kategorilerine göre önerilen filmleri döner.
    Eğer favori kategoriler yoksa rastgele filmler döndürülür.
    """
    user = request.user

    # get_recommended_movies fonksiyonunu çağır
    recommended_movies = get_recommended_movies(user)

    # Eğer önerilecek film yoksa bir mesaj döndür
    if not recommended_movies:
        return JsonResponse({"message": "Öneri oluşturmak için favorilere film ekleyin."}, status=200)

    # Filmleri JSON formatına dönüştür
    recommendations = []
    for movie in recommended_movies:
        recommendations.append({
            "id": movie.id,
            "name": movie.name,
            "image":  movie.image,  # Görsel varsa ekle
            "description": movie.description,
            "duration": movie.duration,
            "director": movie.director,
            "cast": [actor.name for actor in movie.cast.all()],  # Oyuncu listesi
            "category": [category.name for category in movie.category.all()],  # Kategori listesi
        })

    return JsonResponse(recommendations, safe=False, json_dumps_params={'ensure_ascii': False})