import requests
from sqlalchemy.exc import IntegrityError
from app import app, db, Movie, Mood

API_KEY = "TON_API_KEY_TMDB"  # 👉 Mets ta clé TMDb ici
BASE_URL = "https://api.themoviedb.org/3"

# Plateformes autorisées
ALLOWED_PLATFORMS = {
    "Netflix", "Amazon Prime Video", "Canal+", "OCS", "HBO Max",
    "Disney Plus", "Crunchyroll", "Paramount+", "Apple TV+","Apple TV", "Google Play Movies"
}

# Mapping Mood → IDs de genres TMDb
MOOD_GENRE_MAP = {
    "triste": [18, 10749],        # Drama, Romance
    "drôle": [35],                # Comedy
    "heureux": [10751, 12],       # Family, Adventure
    "amoureux": [10749],          # Romance
    "énervé": [28, 53],           # Action, Thriller
    "peur": [27]                  # Horror
}

MIN_RATING = 6.0  # 👉 seuil minimum de note

def reset_moods():
    Mood.query.delete()
    db.session.commit()
    moods = ["triste", "drôle", "heureux", "amoureux", "énervé", "peur"]
    for m in moods:
        mood = Mood(user_id=1, mood_type=m)  # 👈 user_id=1 si obligatoire
        db.session.add(mood)
    db.session.commit()
    print("Moods recréés ✅")



def insert_movie_if_valid(tmdb_id, mood_id):
    if not is_available_on_major_platforms(tmdb_id):
        return

    url = f"{BASE_URL}/movie/{tmdb_id}"
    params = {"api_key": API_KEY, "language": "fr-FR"}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return

    data = r.json()
    rating = data.get("vote_average", 0)

    if rating < MIN_RATING:
        print(f"Film {data.get('title')} ignoré ❌ (note trop basse: {rating})")
        return

    if not data.get("title") or not data.get("overview"):
        print(f"Film ignoré ❌ (incomplet: {data.get('title')})")
        return

    genres = [g["name"] for g in data.get("genres", [])]

    print("Insertion tentative:", data["title"], "genres:", genres, "note:", rating, "mood_id:", mood_id)

    # ✅ Vérification avant insertion pour éviter les doublons
    existing = Movie.query.filter_by(tmdb_id=tmdb_id, mood_id=mood_id).first()
    if existing:
        print(f"Film {data.get('title')} déjà présent pour ce mood ❌ (doublon ignoré)")
        return

    movie = Movie(
        tmdb_id=tmdb_id,
        title=data["title"],
        description=data.get("overview"),
        genre=", ".join(genres) if genres else None,
        rating=rating,
        poster_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get("poster_path") else None,
        mood_id=mood_id
    )

    try:
        db.session.add(movie)
        db.session.commit()
        print(f"Film ajouté ✅ {movie.title} (note {rating})")
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de l'insertion de {data.get('title')}: {e}")


def populate_movies_by_genre():
    for mood, genre_ids in MOOD_GENRE_MAP.items():
        mood_obj = Mood.query.filter_by(mood_type=mood).first()
        if not mood_obj:
            print("Mood introuvable:", mood)
            continue

        for genre_id in genre_ids:
            url = f"{BASE_URL}/discover/movie"
            params = {
                "api_key": API_KEY,
                "language": "fr-FR",
                "sort_by": "popularity.desc",
                "page": 1,
                "with_genres": genre_id
            }
            r = requests.get(url, params=params)
            if r.status_code != 200:
                continue

            data = r.json().get("results", [])
            print(f"🎬 {len(data)} films trouvés pour genre {genre_id} ({mood})")

            for film in data:
                insert_movie_if_valid(film["id"], mood_obj.id)

def is_available_on_major_platforms(tmdb_id, region="US"):
    url = f"{BASE_URL}/movie/{tmdb_id}/watch/providers"
    params = {"api_key": API_KEY}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        print(f"❌ TMDb provider API failed for {tmdb_id}")
        return False  # ⚠️ si l'API échoue, on ignore le film

    data = r.json().get("results", {})
    country_data = data.get(region, {})
    providers = country_data.get("flatrate", []) + country_data.get("rent", []) + country_data.get("buy", [])

    provider_names = [p.get("provider_name") for p in providers]
    print(f"🔍 Providers for {tmdb_id} in {region}: {provider_names}")

    for p in providers:
        if p.get("provider_name") in ALLOWED_PLATFORMS:
            return True

    print(f"Film {tmdb_id} ignoré ❌ (pas dispo sur plateformes majeures)")
    return False  # ⚠️ on rejette si aucun provider valide




import traceback

if __name__ == "__main__":
    with app.app_context():
        try:
            reset_moods()
            populate_movies_by_genre()
            print("Base de données de films populée avec succès ! 🎉")
        except Exception as e:
            db.session.rollback()
            print("Erreur globale pendant la population:", e)
            traceback.print_exc()
            

