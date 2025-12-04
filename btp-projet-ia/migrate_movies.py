#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour ajouter la colonne poster_url à la table movies
"""

import os
from dotenv import load_dotenv

load_dotenv()

import psycopg2

# Configuration PostgreSQL
db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'password')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', 5432)
db_name = os.environ.get('DB_NAME', 'feelflix')

print(f"Connexion à {db_host}:{db_port}/{db_name}")

try:
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    
    cursor = conn.cursor()
    
    # Vérifier si la colonne existe déjà
    cursor.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name = 'movies' AND column_name = 'poster_url'
    """)
    
    if cursor.fetchone() is None:
        print("Ajout de la colonne poster_url...")
        cursor.execute("""
            ALTER TABLE movies ADD COLUMN poster_url VARCHAR(255)
        """)
        conn.commit()
        print("✅ Colonne poster_url ajoutée avec succès!")
    else:
        print("ℹ️  La colonne poster_url existe déjà.")
    
    # Vérifier si la colonne image_url existe
    cursor.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name = 'movies' AND column_name = 'image_url'
    """)
    
    if cursor.fetchone() is None:
        print("Ajout de la colonne image_url...")
        cursor.execute("""
            ALTER TABLE movies ADD COLUMN image_url VARCHAR(255)
        """)
        conn.commit()
        print("✅ Colonne image_url ajoutée avec succès!")
    else:
        print("ℹ️  La colonne image_url existe déjà.")
    
    cursor.close()
    conn.close()
    print("✅ Migration terminée!")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
