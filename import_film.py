#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour importer les films depuis TMDB
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Ajouter le répertoire courant au PATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Movie, Mood
from datetime import datetime
import requests

API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    print("❌ Erreur: TMDB_API_KEY non trouvée dans .env")
    sys.exit(1)

# Dictionnaire mood → genre TMDb
mood_genres = {
    "très triste": 18,      # Drama
    "triste": 18,           # Drama
    "joyeux": 35,           # Comedy
    "énervé": 28,           # Action
    "heureux": 12,          # Adventure
    "amoureux": 10749,      # Romance
    "peur": 27              # Horror
}

print("🎬 Début de l'importation des films...")

with app.app_context():
    try:
        for mood_type, genre_id in mood_genres.items():
            print(f"\n📂 Traitement du mood: {mood_type}")
            
            # Vérifier si le mood existe
            mood = Mood.query.filter_by(mood_type=mood_type).first()
            
            if not mood:
                print(f"   ↳ Création du mood: {mood_type}")
                mood = Mood(mood_type=mood_type, user_id=1)
                db.session.add(mood)
                db.session.commit()
            else:
                print(f"   ↳ Mood trouvé: {mood.id}")
            
            # Vérifier s'il y a déjà des films pour ce mood
            existing_movies = Movie.query.filter_by(mood_id=mood.id).count()
            if existing_movies > 0:
                print(f"   ↳ {existing_movies} films déjà présents, passage...")
                continue
            
            # Requête TMDB
            print(f"   ↳ Téléchargement des films (genre_id={genre_id})...")
            url = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre_id}&language=fr-FR&sort_by=popularity.desc'
            
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if 'results' not in data:
                    print(f"   ❌ Erreur TMDB: {data}")
                    continue
                
                # Ajouter les films
                added_count = 0
                for film in data['results'][:5]:
                    try:
                        # Récupérer l'affiche si disponible
                        poster_url = None
                        if film.get('poster_path'):
                            poster_url = f"https://image.tmdb.org/t/p/w500{film['poster_path']}"
                        
                        new_movie = Movie(
                            title=film.get('title', 'Unknown'),
                            description=film.get('overview', ''),
                            genre=str(film.get('genre_ids', [None])[0]) if film.get('genre_ids') else 'Unknown',
                            rating=film.get('vote_average', 0.0),
                            image_url=poster_url,
                            poster_url=poster_url,
                            mood_id=mood.id,
                            created_at=datetime.utcnow()
                        )
                        db.session.add(new_movie)
                        added_count += 1
                    except Exception as e:
                        print(f"      ⚠️  Erreur lors du traitement du film: {e}")
                        continue
                
                db.session.commit()
                print(f"   ✅ {added_count} films importés pour {mood_type}")
                
            except requests.RequestException as e:
                print(f"   ❌ Erreur lors de la requête TMDB: {e}")
                continue
        
        print("\n✅ Importation terminée!")
        
        # Afficher les statistiques
        total_moods = Mood.query.count()
        total_movies = Movie.query.count()
        print(f"\n📊 Statistiques:")
        print(f"   - Total moods: {total_moods}")
        print(f"   - Total films: {total_movies}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()