import requests
import os

from models import Movie, db

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

import random

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

def add_popular_movies_to_db(mood_id, limit=5):
    url = f"{BASE_URL}/movie/popular"
    params = {
        "api_key": API_KEY,
        "language": "fr-FR",
        "page": random.randint(1, 5)  # varie les pages pour plus de diversité
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        movies = response.json().get("results", [])[:limit]
        for m in movies:
            movie = Movie(
                mood_id=mood_id,   # 👈 associer au mood demandé
                title=m.get("title"),
                description=m.get("overview"),
                genre="Popular",
                rating=m.get("vote_average"),
                poster_url=f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None
            )
            db.session.add(movie)
        db.session.commit()

