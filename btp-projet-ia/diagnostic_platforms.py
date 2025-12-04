#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de diagnostic pour les plateformes de streaming
"""

import os
from dotenv import load_dotenv
import psycopg2
import requests

load_dotenv()

DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_NAME = os.environ.get('DB_NAME', 'feelflix')

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

print("📋 DIAGNOSTIC DES PLATEFORMES DE STREAMING\n")

# 1. Vérifier la colonne tmdb_id
print("1️⃣ Vérification de la colonne tmdb_id...")
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
    c = conn.cursor()
    
    # Check if column exists
    c.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='movies' AND column_name='tmdb_id'
    """)
    
    if c.fetchone() is None:
        print("  ❌ Colonne tmdb_id manquante, création en cours...")
        c.execute("ALTER TABLE movies ADD COLUMN tmdb_id INTEGER")
        conn.commit()
        print("  ✅ Colonne tmdb_id créée")
    else:
        print("  ✅ Colonne tmdb_id existe")
    
    # 2. Vérifier les films avec tmdb_id
    print("\n2️⃣ Vérification des films avec tmdb_id...")
    c.execute("SELECT COUNT(*) FROM movies WHERE tmdb_id IS NOT NULL")
    count_with_tmdb = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM movies")
    total_count = c.fetchone()[0]
    
    print(f"  Films avec tmdb_id: {count_with_tmdb}/{total_count}")
    
    if count_with_tmdb == 0 and total_count > 0:
        print("  ⚠️  Aucun film avec tmdb_id, vous devez réexécuter import_film.py ou popular_db.py")
    
    # 3. Vérifier un film avec tmdb_id
    if count_with_tmdb > 0:
        print("\n3️⃣ Test de l'API /api/movie/<tmdb_id>...")
        c.execute("SELECT tmdb_id, title FROM movies WHERE tmdb_id IS NOT NULL LIMIT 1")
        result = c.fetchone()
        if result:
            tmdb_id, title = result
            print(f"  Film test: {title} (ID: {tmdb_id})")
            
            url = f"{BASE_URL}/movie/{tmdb_id}/watch/providers"
            params = {"api_key": API_KEY}
            r = requests.get(url, params=params)
            
            if r.status_code == 200:
                data = r.json()
                print(f"  ✅ TMDB API répond correctement")
                
                if "results" in data and "FR" in data["results"]:
                    fr_data = data["results"]["FR"]
                    providers = fr_data.get("flatrate", []) + fr_data.get("rent", []) + fr_data.get("buy", [])
                    if providers:
                        print(f"  ✅ Plateformes trouvées: {len(providers)}")
                        for p in providers[:3]:
                            print(f"      - {p.get('provider_name')} (logo: {p.get('logo_path')})")
                    else:
                        print("  ⚠️  Aucune plateforme trouvée pour la France")
                else:
                    print("  ⚠️  Données France non disponibles dans TMDB")
            else:
                print(f"  ❌ Erreur TMDB API: {r.status_code}")
    
    c.close()
    conn.close()
    
    print("\n✅ Diagnostic terminé")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
