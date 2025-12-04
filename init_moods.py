#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour initialiser les moods par défaut
"""

import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

# Créer app et db directement pour éviter config.py
app = Flask(__name__)

db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'password')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', 5432)
db_name = os.environ.get('DB_NAME', 'feelflix')

database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Mood

MOODS = [
    'très triste',
    'triste', 
    'joyeux',
    'énervé',
    'heureux',
    'amoureux',
    'peur'
]

print("🔧 Initialisation des moods...")

with app.app_context():
    try:
        # Vérifier si les moods existent déjà
        existing_moods = Mood.query.all()
        
        if existing_moods:
            print(f"ℹ️  {len(existing_moods)} moods déjà existants")
        else:
            # Créer les moods par défaut avec user_id=1
            for mood_type in MOODS:
                mood = Mood(mood_type=mood_type, user_id=1)
                db.session.add(mood)
            
            db.session.commit()
            print(f"✅ {len(MOODS)} moods créés avec succès!")
            
            for mood in Mood.query.all():
                print(f"   - {mood.mood_type}")
                
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        try:
            db.session.rollback()
        except:
            pass
