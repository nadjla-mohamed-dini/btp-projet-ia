import requests
import os

from models import Movie, db

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

import random
MOOD_GENRE_IDS = {
    "tres_triste": [18],        # Drame
    "joyeux": [35],             # Comédie
    "enerve": [28, 53],         # Action + Thriller
    "heureux": [16, 35],        # Animation + Comédie
    "amoureux": [10749],        # Romance
    "peur": [27]                # Horreur
}



def fetch_new_movies(destination, limit=5):
    """Récupère des films populaires depuis TMDb pour une destination donnée"""
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "sort_by": "popularity.desc",
        "language": "fr-FR",
        "page": random.randint(1, 7),  # 👈 change de page à chaque appel
        "region": "FR"
    }

    if destination == "paris":
        params["with_keywords"] = "Paris"
    elif destination == "tokyo":
        params["with_keywords"] = "Tokyo"
    elif destination == "newyork":
        params["with_keywords"] = "New York"

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])[:limit]
    return []


def get_movie_details(movie_id):
    """Récupère les détails d’un film (overview, etc.)"""
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY, "language": "fr-FR"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def get_watch_providers(movie_id):
    """Récupère les plateformes de streaming pour un film"""
    url = f"{BASE_URL}/movie/{movie_id}/watch/providers"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and "FR" in data["results"]:
            fr_data = data["results"]["FR"]
            platforms = []
            if "flatrate" in fr_data:
                for provider in fr_data["flatrate"]:
                    platforms.append(provider["provider_name"])
            return platforms
    return []

import random
import requests

def add_popular_movies_to_db(mood, limit=5):
    genre_ids = MOOD_GENRE_IDS.get(mood.mood_type, [])
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "language": "fr-FR",
        "sort_by": "popularity.desc",
        "page": random.randint(1, 5)
    }
    if genre_ids:
        params["with_genres"] = ",".join(map(str, genre_ids))

    r = requests.get(url, params=params)
    if r.status_code != 200:
        return

    movies = r.json().get("results", [])[:limit]

    for m in movies:
        tmdb_id = m.get("id")
        if not tmdb_id:
            continue

        # Vérifier si déjà présent
        existing = Movie.query.filter_by(tmdb_id=tmdb_id, mood_id=mood.id).first()
        if existing:
            # Mettre à jour si besoin
            existing.rating = m.get("vote_average")
            if m.get("poster_path"):
                existing.poster_url = f"https://image.tmdb.org/t/p/w500{m['poster_path']}"
            continue

        # Sinon insérer
        movie = Movie(
            tmdb_id=tmdb_id,
            mood_id=mood.id,
            title=m.get("title"),
            description=m.get("overview"),
            genre=mood.mood_type,
            rating=m.get("vote_average"),
            poster_url=f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None
        )
        db.session.add(movie)

    db.session.commit()

import requests

def get_watch_providers(tmdb_id, region="FR"):
    url = f"{BASE_URL}/movie/{tmdb_id}/watch/providers"
    params = {"api_key": API_KEY}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return []

    data = r.json().get("results", {})
    country_data = data.get(region, {})

    providers = country_data.get("flatrate", []) + country_data.get("rent", []) + country_data.get("buy", [])

    # 👉 Liste blanche des plateformes
    allowed_platforms = {
        "Canal+", "Netflix", "HBO Max", "Paramount+", "Amazon Prime Video",
        "Disney Plus", "Crunchyroll", "Apple TV+"
    }

    results = []
    for p in providers:
        if p.get("provider_name") in allowed_platforms:
            results.append({
                "platform_name": p.get("provider_name"),
                "platform_logo": f"https://image.tmdb.org/t/p/w92{p['logo_path']}" if p.get("logo_path") else None,
                "platform_url": f"https://www.themoviedb.org/movie/{tmdb_id}/watch"
            })

    if not results:
        results.append({
            "platform_name": "Actuellement au cinéma",
            "platform_logo": None,
            "platform_url": None
        })

    return results


