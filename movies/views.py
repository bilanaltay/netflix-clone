from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from movies.models import Movie, UserMovieList, WatchHistory
from django.core.exceptions import ObjectDoesNotExist


# Tüm filmleri listeleme
@api_view(["GET"])
def movie_list(request):
    # Tüm filmleri al
    movies = Movie.objects.all()

    # Verileri manuel olarak JSON formatına dönüştür
    movies_list = []
    for movie in movies:
        movies_list.append({
            "id": movie.id,
            "name": movie.name,
            "image": movie.image,
            "description": movie.description,
            "duration": movie.duration,
            "director": movie.director,
            "cast": [actor.name for actor in movie.cast.all()],  # Oyuncular
            # Kategoriler
            "category": [category.name for category in movie.category.all()]
        })

    # JSON olarak döndür ve Türkçe karakter desteği ekle
    return JsonResponse(movies_list, safe=False, json_dumps_params={'ensure_ascii': False})


# Kullanıcının listesindeki filmleri görüntüleme
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_movie_list(request):
    user_movies = UserMovieList.objects.filter(user=request.user)

    # Kullanıcının listesindeki filmleri JSON formatına dönüştür
    movies_list = []
    for user_movie in user_movies:
        movie = user_movie.movie
        movies_list.append({
            "id": movie.id,
            "name": movie.name,
            "image": movie.image,
            "description": movie.description,
            "duration": movie.duration,
            "director": movie.director,
            "cast": [actor.name for actor in movie.cast.all()],  # Oyuncular
            # Kategoriler
            "category": [category.name for category in movie.category.all()],
            # Tarihi formatla
            "added_at": user_movie.added_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    # JSON olarak döndür
    return JsonResponse(movies_list, safe=False, json_dumps_params={'ensure_ascii': False})


# Kullanıcının listesine film ekleme
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_movie_to_list(request, movie_id):
    user = request.user  # Giriş yapan kullanıcı
    try:
        movie = Movie.objects.get(id=movie_id)  # Film var mı kontrol et
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Film bulunamadı."}, status=404)

    # Kullanıcının listesine filmi ekle
    obj, created = UserMovieList.objects.get_or_create(user=user, movie=movie)
    if created:
        return JsonResponse({"message": f"'{movie.name}' listenize eklendi."}, status=201)
    else:
        return JsonResponse({"message": f"'{movie.name}' zaten listenizde."}, status=200)


# Kullanıcının listesinden filmi kaldırma
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_movie_from_list(request, movie_id):
    user = request.user  # Giriş yapan kullanıcı
    try:
        user_movie = UserMovieList.objects.get(
            user=user, movie_id=movie_id)  # Film listede var mı kontrol et
        user_movie.delete()  # Filmi listeden kaldır
        return JsonResponse({"message": "Film listenizden kaldırıldı."}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Film listenizde bulunamadı."}, status=404)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_watch_history(request, movie_id):
    user = request.user  # Giriş yapan kullanıcı
    try:
        movie = Movie.objects.get(id=movie_id)  # Film var mı kontrol et
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Film bulunamadı."}, status=404)

    # Kullanıcının izleme geçmişine filmi ekle veya güncelle
    obj, created = WatchHistory.objects.get_or_create(user=user, movie=movie)
    if not created:
        # Eğer film zaten izlenmişse, izleme zamanını güncelle
        obj.watched_at = timezone.now()
        obj.save()

    return JsonResponse({"message": f"'{movie.name}' izleme geçmişinize eklendi."}, status=201)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_watch_history(request):
    user = request.user  # Giriş yapan kullanıcı
    watch_history = WatchHistory.objects.filter(user=user).order_by("-watched_at")

    # İzleme geçmişini JSON formatına dönüştür
    history_list = []
    for history in watch_history:
        movie = history.movie
        history_list.append({
            "id": movie.id,
            "name": movie.name,
            "image": movie.image,
            "description": movie.description,
            "duration": movie.duration,
            "director": movie.director,
            "cast": [actor.name for actor in movie.cast.all()],  # Oyuncular
            "category": [category.name for category in movie.category.all()],  # Kategoriler
            "watched_at": history.watched_at.strftime('%Y-%m-%d %H:%M:%S')  # İzleme zamanı
        })

    return JsonResponse(history_list, safe=False, json_dumps_params={'ensure_ascii': False})