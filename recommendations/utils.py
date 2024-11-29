from collections import Counter
from movies.models import Movie
from recommendations.models import FavoriteMovie


def get_recommended_movies(user, limit=8):
    """
    Kullanıcının favori kategorilerine göre film önerileri oluşturur.
    Eğer favori kategoriler yoksa rastgele filmler önerir.
    """
    # Kullanıcının favori filmlerini al
    favorite_movies = FavoriteMovie.objects.filter(user=user)

    # Favori kategorileri analiz et
    category_counter = Counter()
    for favorite in favorite_movies:
        for category in favorite.movie.category.all():  # ManyToManyField üzerinden kategorilere erişim
            category_counter[category] += 1

    # Eğer favori kategoriler yoksa rastgele filmler döndür
    if not category_counter:
        # Favorilere eklenmemiş rastgele filmleri seç
        random_movies = Movie.objects.exclude(
            favorited_by__user=user  # Kullanıcının favorilerinde olmayan filmleri seç
        ).order_by('?')[:limit]  # Rastgele sırala ve limiti uygula
        return random_movies

    # Toplam kategori sayısını hesapla
    total_categories = sum(category_counter.values())

    # Öneri listesi
    recommendations = []

    # Her kategoriye göre film seçimi yap
    for category, count in category_counter.most_common():
        ratio = count / total_categories  # Kategori oranı
        suggested_count = max(1, int(ratio * limit))  # Önerilecek film sayısı, en az 1
        category_movies = Movie.objects.filter(category=category).exclude(
            favorited_by__user=user  # Kullanıcının favorilerine eklenmemiş filmleri seç
        )[:suggested_count]

        recommendations.extend(category_movies)

    # Toplam öneri sayısını sınırla
    return recommendations[:limit]