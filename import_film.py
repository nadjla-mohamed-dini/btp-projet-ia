# -*- coding: utf-8 -*-
import requests
from models import db, Movie, Mood
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()


API_KEY = os.getenv("TMDB_API_KEY")  # Remplace par ta vraie clé

# Dictionnaire mood → genre TMDb
mood_genres = {
    "joyeux": 35,
    "heureux": 12,
    "très triste": 18,
    "amoureux": 10749,
    "énervé": 28,
    "peur": 27
}

for mood_type, genre_id in mood_genres.items():
    print(f"Importation des films pour le mood : {mood_type}")
    
    # Requête TMDb
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre_id}&language=fr-FR'
    response = requests.get(url)
    data = response.json()

    # Récupérer le mood dans la base
    mood = Mood.query.filter_by(mood_type=mood_type).first()
    if not mood:
        print(f"⚠️ Mood '{mood_type}' introuvable en base.")
        continue

    # Ajouter les films
    for film in data['results'][:5]:
        new_movie = Movie(
            title=film['title'],
            description=film['overview'],
            genre=film.get('genre_ids', [])[0],  # ou 'genre' fixe si tu préfères
            rating=film.get('vote_average', 0),
            mood_id=mood.id,
            created_at=datetime.utcnow()
        )
        db.session.add(new_movie)

    db.session.commit()
    print(f"✅ Films ajoutés pour le mood : {mood_type}\n")
