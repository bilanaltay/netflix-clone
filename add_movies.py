import os
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Projenizde settings.py'nin yolunu belirtin
django.setup()

from movies.models import Movie, Actor, Category

# Film verileri
film_listesi = [
    {
        "name": "Inside Out",
        "image": "https://upload.wikimedia.org/wikipedia/en/0/0a/Inside_Out_%282015_film%29_poster.jpg",
        "description": "The emotions inside a young girl's mind navigate her life.",
        "duration": 95,
        "director": "Pete Docter",
        "cast": ["Amy Poehler", "Phyllis Smith", "Bill Hader"],
        "category": ["Animasyon", "Aile (Family)", "Komedi"]
    },
    {
        "name": "Inception",
        "image": "https://upload.wikimedia.org/wikipedia/en/7/7f/Inception_ver3.jpg",
        "description": "A thief who steals corporate secrets through dream-sharing technology.",
        "duration": 148,
        "director": "Christopher Nolan",
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
        "category": ["Bilim Kurgu (Sci-Fi)", "Gerilim (Thriller)", "Aksiyon"]
    },
    {
        "name": "The Dark Knight",
        "image": "https://upload.wikimedia.org/wikipedia/en/8/8a/Dark_Knight.jpg",
        "description": "Batman faces the Joker in his fight against crime in Gotham City.",
        "duration": 152,
        "director": "Christopher Nolan",
        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
        "category": ["Aksiyon", "Suç (Crime)", "Dram"]
    },
    {
        "name": "Interstellar",
        "image": "https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg",
        "description": "A team of explorers travel beyond the galaxy to save humanity.",
        "duration": 169,
        "director": "Christopher Nolan",
        "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
        "category": ["Bilim Kurgu (Sci-Fi)", "Dram", "Tarihi"]
    },
    {
        "name": "The Lion King",
        "image": "https://upload.wikimedia.org/wikipedia/en/3/3d/The_Lion_King_poster.jpg",
        "description": "A lion cub's journey to adulthood and acceptance of his destiny.",
        "duration": 88,
        "director": "Roger Allers",
        "cast": ["Matthew Broderick", "Jeremy Irons", "James Earl Jones"],
        "category": ["Animasyon", "Aile (Family)", "Müzikal"]
    },
    {
        "name": "The Matrix",
        "image": "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg",
        "description": "A computer hacker learns about the true nature of his reality.",
        "duration": 136,
        "director": "The Wachowskis",
        "cast": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
        "category": ["Bilim Kurgu (Sci-Fi)", "Aksiyon", "Gerilim (Thriller)"]
    },
    {
        "name": "Schindler's List",
        "image": "https://upload.wikimedia.org/wikipedia/en/3/38/Schindler%27s_List_movie.jpg",
        "description": "The story of Oskar Schindler and his efforts to save Jewish lives.",
        "duration": 195,
        "director": "Steven Spielberg",
        "cast": ["Liam Neeson", "Ralph Fiennes", "Ben Kingsley"],
        "category": ["Tarihi", "Dram", "Biyografi (Biopic)"]
    },
    {
        "name": "Finding Nemo",
        "image": "https://upload.wikimedia.org/wikipedia/en/2/29/Finding_Nemo.jpg",
        "description": "A clownfish searches for his missing son in the ocean.",
        "duration": 100,
        "director": "Andrew Stanton",
        "cast": ["Albert Brooks", "Ellen DeGeneres", "Alexander Gould"],
        "category": ["Animasyon", "Aile (Family)", "Macera"]
    },
    {
        "name": "Pulp Fiction",
        "image": "https://upload.wikimedia.org/wikipedia/en/8/82/Pulp_Fiction_cover.jpg",
        "description": "The lives of two mob hitmen, a boxer, and others intertwine in Los Angeles.",
        "duration": 154,
        "director": "Quentin Tarantino",
        "cast": ["John Travolta", "Uma Thurman", "Samuel L. Jackson"],
        "category": ["Suç (Crime)", "Dram", "Gerilim (Thriller)"]
    },
    {
        "name": "The Avengers",
        "image": "https://upload.wikimedia.org/wikipedia/en/f/f9/TheAvengers2012Poster.jpg",
        "description": "Earth's mightiest heroes must come together to stop Loki.",
        "duration": 143,
        "director": "Joss Whedon",
        "cast": ["Robert Downey Jr.", "Chris Evans", "Scarlett Johansson"],
        "category": ["Aksiyon", "Fantastik", "Bilim Kurgu (Sci-Fi)"]
    },
    {
        "name": "Frozen",
        "image": "https://upload.wikimedia.org/wikipedia/en/0/05/Frozen_%282013_film%29_poster.jpg",
        "description": "A young woman must embrace her magical powers to save her kingdom.",
        "duration": 102,
        "director": "Jennifer Lee",
        "cast": ["Kristen Bell", "Idina Menzel", "Josh Gad"],
        "category": ["Animasyon", "Müzikal", "Aile (Family)"]
    },
    {
        "name": "The Godfather",
        "image": "https://upload.wikimedia.org/wikipedia/en/1/1c/Godfather_ver1.jpg",
        "description": "The aging patriarch of an organized crime dynasty transfers control to his son.",
        "duration": 175,
        "director": "Francis Ford Coppola",
        "cast": ["Marlon Brando", "Al Pacino", "James Caan"],
        "category": ["Suç (Crime)", "Dram"]
    },
    {
        "name": "The Pursuit of Happyness",
        "image": "https://upload.wikimedia.org/wikipedia/en/8/81/Poster-pursuithappyness.jpg",
        "description": "A struggling salesman takes custody of his son as he begins a life-changing journey.",
        "duration": 117,
        "director": "Gabriele Muccino",
        "cast": ["Will Smith", "Jaden Smith"],
        "category": ["Dram", "Biyografi (Biopic)"]
    },
    {
        "name": "Spirited Away",
        "image": "https://upload.wikimedia.org/wikipedia/en/3/30/Spirited_Away_poster.JPG",
        "description": "A young girl becomes trapped in a mysterious, magical world.",
        "duration": 125,
        "director": "Hayao Miyazaki",
        "cast": ["Rumi Hiiragi", "Miyu Irino", "Mari Natsuki"],
        "category": ["Animasyon", "Fantastik", "Macera"]
    },
    {
        "name": "The Shawshank Redemption",
        "image": "https://upload.wikimedia.org/wikipedia/en/8/81/ShawshankRedemptionMoviePoster.jpg",
        "description": "Two imprisoned men bond over a number of years.",
        "duration": 142,
        "director": "Frank Darabont",
        "cast": ["Tim Robbins", "Morgan Freeman"],
        "category": ["Dram", "Suç (Crime)"]
    }
]

# Verileri ekleme
for film in film_listesi:
    # Film nesnesini oluştur
    movie_obj = Movie.objects.create(
        name=film["name"],
        image=film["image"],
        description=film["description"],
        duration=film["duration"],
        director=film["director"]
    )

    # Oyuncuları ekle
    for actor_name in film["cast"]:
        actor_obj, _ = Actor.objects.get_or_create(name=actor_name)
        movie_obj.cast.add(actor_obj)

    # Kategorileri ekle
    for category_name in film["category"]:
        category_obj, _ = Category.objects.get_or_create(name=category_name)
        movie_obj.category.add(category_obj)

    # Film kaydını tamamla
    movie_obj.save()

print("Filmler başarıyla eklendi!")