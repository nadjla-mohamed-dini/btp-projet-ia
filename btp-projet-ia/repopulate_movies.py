#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour repeupler les films avec tmdb_id correctement depuis TMDB
"""

import os
from dotenv import load_dotenv

load_dotenv()

from app import app, db
from models import Movie, Mood
import requests

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

MOOD_GENRE_MAP = {
    'très triste': [18],  # Drama
    'triste': [18, 14],   # Drama, Mystery
    'joyeux': [35, 16],   # Comedy, Animation
    'énervé': [28, 53],   # Action, Thriller
    'heureux': [35, 14],  # Comedy, Mystery
    'amoureux': [10749],  # Romance
    'peur': [27],         # Horror
}

ALLOWED_PLATFORMS = {
    'Netflix', 'Amazon Prime Video', 'Disney+', 
    'Apple TV+', 'Canal+', 'OCS', 'Hulu'
}

def insert_movie_if_valid(tmdb_id, mood_id):
    """Insère un film s'il est valide (a des plateformes, etc.)"""
    
    # Récupérer les détails du film
    url = f"{BASE_URL}/movie/{tmdb_id}"
    params = {"api_key": API_KEY, "language": "fr-FR"}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"  ❌ Impossible de récupérer {tmdb_id}")
        return
    
    data = response.json()
    
    # Extraire les genres
    genres = data.get("genres", [])
    genre_names = [g["name"] for g in genres] if genres else ["Unknown"]
    
    rating = data.get("vote_average", 0)
    
    print(f"✓ {data['title']} (ID: {tmdb_id}) - genres: {', '.join(genre_names)} - note: {rating}")
    
    # Vérifier si le film existe déjà
    existing = Movie.query.filter_by(tmdb_id=tmdb_id, mood_id=mood_id).first()
    if existing:
        print(f"  ℹ️  Film déjà présent")
        return
    
    # Créer et ajouter le film
    movie = Movie(
        tmdb_id=tmdb_id,
        title=data.get("title"),
        description=data.get("overview"),
        genre=", ".join(genre_names) if genre_names else None,
        rating=rating,
        poster_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get("poster_path") else None,
        mood_id=mood_id
    )
    
    try:
        db.session.add(movie)
        db.session.commit()
        print(f"  ✅ Film ajouté avec succès")
    except Exception as e:
        db.session.rollback()
        print(f"  ❌ Erreur: {e}")

def populate_movies():
    """Remplit la base de données avec des films valides"""
    
    with app.app_context():
        print("🎬 Repeuplate des films avec tmdb_id...\n")
        
        for mood_type, genre_ids in MOOD_GENRE_MAP.items():
            mood_obj = Mood.query.filter_by(mood_type=mood_type).first()
            if not mood_obj:
                print(f"❌ Mood '{mood_type}' introuvable")
                continue
            
            print(f"📌 Récupération pour '{mood_type}'...")
            
            for genre_id in genre_ids:
                url = f"{BASE_URL}/discover/movie"
                params = {
                    "api_key": API_KEY,
                    "language": "fr-FR",
                    "sort_by": "popularity.desc",
                    "page": 1,
                    "with_genres": genre_id
                }
                response = requests.get(url, params=params)
                if response.status_code != 200:
                    print(f"  ❌ Erreur API pour genre {genre_id}")
                    continue
                
                films = response.json().get("results", [])
                print(f"  {len(films)} films trouvés pour genre {genre_id}")
                
                for film in films[:5]:  # Limiter à 5 par genre
                    insert_movie_if_valid(film["id"], mood_obj.id)
        
        print("\n✅ Repeuplate terminée!")

if __name__ == "__main__":
    populate_movies()
