#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour récupérer automatiquement les films depuis TMDb :
- par destination (Paris, New York, Tokyo)
- par décennie (90s, 2000s, 2010s) avec Discover API
et insérer leurs vraies plateformes de streaming
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
os.environ['PYTHONUTF8'] = '1'

import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_NAME = os.environ.get('DB_NAME', 'Fellflix')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')

# Destinations et mots-clés
destinations = [
    {'name': 'paris', 'keywords': ['Amélie', 'Midnight in Paris', 'Ratatouille', 'Marie-Antoinette', 'The Bourne Identity'], 'count': 5},
    {'name': 'newyork', 'keywords': ['Taxi Driver', 'Home Alone', 'Ghostbusters', 'Spider-Man', 'The Godfather', 'Breakfast at Tiffany\'s'], 'count': 6},
    {'name': 'tokyo', 'keywords': ['Lost in Translation', 'Battle Royale', 'Seven Samurai', 'Shall We Dance', 'Your Name', 'Spirited Away'], 'count': 6},
]

# Décennies (nouvelle logique Discover)
decades = [
    {"name": "years_1990", "start": 1990, "end": 1999},
    {"name": "years_2000", "start": 2000, "end": 2009},
    {"name": "years_2010", "start": 2010, "end": 2019},
]

platform_logos = {
    'netflix': '🎬',
    'disney': '🏰',
    'prime': '🎁',
    'hulu': '📺',
    'apple': '🍎',
    'canal': '📻',
    'crunchyroll': '🍜'
}

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {'api_key': API_KEY, 'language': 'fr-FR'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def search_movies_by_keyword(keyword, limit=5):
    url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': keyword,
        'language': 'fr-FR',
        'sort_by': 'popularity.desc',
        'page': 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['results'][:limit]
    return []

def get_movies_by_decade(start_year, end_year, limit=6):
    """Nouvelle logique pour récupérer les films par décennie"""
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "language": "fr-FR",
        "sort_by": "popularity.desc",
        "primary_release_date.gte": f"{start_year}-01-01",
        "primary_release_date.lte": f"{end_year}-12-31",
        "page": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["results"][:limit]
    return []

def get_watch_providers(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/watch/providers"
    params = {'api_key': API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and 'FR' in data['results']:
            fr_data = data['results']['FR']
            platforms = []
            if 'flatrate' in fr_data:
                for provider in fr_data['flatrate']:
                    provider_name = provider['provider_name'].lower()
                    if 'netflix' in provider_name:
                        platforms.append('netflix')
                    elif 'disney' in provider_name:
                        platforms.append('disney')
                    elif 'prime' in provider_name or 'amazon' in provider_name:
                        platforms.append('prime')
                    elif 'apple' in provider_name:
                        platforms.append('apple')
                    elif 'hulu' in provider_name:
                        platforms.append('hulu')
                    elif 'canal' in provider_name:
                        platforms.append('canal')
                    elif 'crunchyroll' in provider_name:
                        platforms.append('crunchyroll')
            if not platforms and 'buy' in fr_data:
                platforms = ['netflix']
            return list(set(platforms))
    return []

def fetch_new_movies(destination, limit=5):
    """Récupère des films populaires depuis TMDb pour une destination donnée"""
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "sort_by": "popularity.desc",
        "language": "fr-FR",
        "page": 1,
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


def main():
    print("🎬 Recuperation des films depuis TMDb...\n")
    conn = None
    cursor = None
    try:
        print(f"Connexion a PostgreSQL ({DB_HOST}:{DB_PORT}/{DB_NAME})...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            client_encoding='UTF8'
        )
        cursor = conn.cursor()

        print("Suppression des anciennes donnees...\n")
        cursor.execute("DELETE FROM streaming_platforms;")
        cursor.execute("DELETE FROM voyage_films;")
        conn.commit()

        total_inserted = 0

        # --- Destinations (inchangé) ---
        # --- Destinations (nouvelle logique Discover) ---
        for dest in destinations:
            print(f"📍 {dest['name'].upper()}: Recherche films populaires via Discover...\n")
            movies_found = fetch_new_movies(dest['name'], limit=dest['count'])

            for movie in movies_found:
                title = movie.get('title', 'Unknown')
                movie_id = movie.get('id')
                poster_path = movie.get('poster_path')
                year = movie.get('release_date', '')[:4]
                if not poster_path or not movie_id:
                    continue

                details = get_movie_details(movie_id)
                description = details.get('overview', '') if details else movie.get('overview', '')
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                platforms = get_watch_providers(movie_id) or ['netflix']

                cursor.execute(
                    "INSERT INTO voyage_films (title, destination, year, description, poster_url) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                    (title, dest['name'], int(year) if year else 2024, description, poster_url)
                )
                film_id = cursor.fetchone()[0]

                for platform_name in platforms:
                    cursor.execute(
                        "INSERT INTO streaming_platforms (film_id, platform_name, platform_url, platform_logo) VALUES (%s, %s, %s, %s);",
                        (film_id, platform_name, f'https://{platform_name}.com', platform_logos.get(platform_name, ''))
                    )
                conn.commit()
                print(f"  + {title} ({year}) -> {', '.join(platforms)}")
            print()


        # --- Décennies (Discover) ---
        for decade in decades:
            print(f"📅 ANNÉES {decade['start']}s: Recherche films populaires...\n")
            movies_found = get_movies_by_decade(decade["start"], decade["end"], limit=6)

            for movie in movies_found:
                title = movie.get("title", "Unknown")
                movie_id = movie.get("id")
                poster_path = movie.get("poster_path")
                year = movie.get("release_date", "")[:4]
                if not poster_path or not movie_id:
                    continue

                details = get_movie_details(movie_id)
                description = details.get("overview", "") if details else movie.get("overview", "")
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                platforms = get_watch_providers(movie_id) or ["netflix"]

                cursor.execute(
                    "INSERT INTO voyage_films (title, destination, year, description, poster_url) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                    (title, decade["name"], int(year) if year else 2024, description, poster_url)
                )
                film_id = cursor.fetchone()[0]

                for platform_name in platforms:
                    cursor.execute(
                        "INSERT INTO streaming_platforms (film_id, platform_name, platform_url, platform_logo) VALUES (%s, %s, %s, %s);",
                        (film_id, platform_name, f'https://{platform_name}.com', platform_logos.get(platform_name, ''))
                    )
                conn.commit()
                print(f"  + {title} ({year}) -> {', '.join(platforms)}")
                total_inserted += 1
            print()

        print(f"✅ {total_inserted} films inseres avec succes!")

    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Fermer proprement, même en cas d'erreur
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
if __name__ == "__main__":
    main()