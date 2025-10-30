# -*- coding: utf-8 -*-
from dotenv import load_dotenv
load_dotenv()

from tmdbv3api import TMDb, Movie
from models import db, Movie as MovieModel
from app import app
import os


# Configuration TMDB
tmdb = TMDb()
tmdb.api_key = os.getenv("TMDB_API_KEY")  # ← remplace par ta vraie cle
tmdb.language = "fr-FR"

movie_api = Movie()

with app.app_context():
    # Selectionne uniquement les films sans affiche
    films = MovieModel.query.filter_by(poster_url=None).all()

    for film in films:
        results = movie_api.search(film.title)
        if results:
            poster_path = results[0].poster_path
            if poster_path:
                film.poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                print(f" {film.title} → {film.poster_url}")
            else:
                print(f" Pas d'affiche pour {film.title}")
        else:
            print(f" Film non trouve : {film.title}")

    db.session.commit()
    print(" Affiches manquantes ajoutes avec succes")
