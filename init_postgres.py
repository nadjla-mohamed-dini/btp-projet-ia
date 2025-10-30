#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour créer les tables dans PostgreSQL
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configuration PostgreSQL
db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'password')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', 5432)
db_name = os.environ.get('DB_NAME', 'feelflix')

database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Mood(db.Model):
    __tablename__ = 'moods'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    mood_id = db.Column(db.Integer, db.ForeignKey('moods.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(100))
    rating = db.Column(db.Float)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    citation = db.Column(db.String(255))
    acteur = db.Column(db.String(120))
    realisateur = db.Column(db.String(120))
    film = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

if __name__ == '__main__':
    print("🔧 Initialisation de la base de données PostgreSQL Feelflix...")
    print(f"📍 Connecté à: {db_host}:{db_port}/{db_name}")
    
    try:
        with app.app_context():
            print("📊 Création des tables...")
            db.create_all()
            print("✅ Tables créées avec succès!")
            print("📋 Tables: users, moods, movies, profiles")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print("\n⚠️  Vérifiez que:")
        print(f"   - PostgreSQL est en cours d'exécution sur {db_host}:{db_port}")
        print(f"   - La base de données '{db_name}' existe")
        print(f"   - Les paramètres de connexion sont corrects dans .env")
        import traceback
        traceback.print_exc()
