#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour ajouter la colonne photo_url à la table profiles
"""

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

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
        WHERE table_name = 'profiles' AND column_name = 'photo_url'
    """)
    
    if cursor.fetchone() is None:
        print("Ajout de la colonne photo_url...")
        cursor.execute("""
            ALTER TABLE profiles ADD COLUMN photo_url VARCHAR(255)
        """)
        conn.commit()
        print("✅ Colonne photo_url ajoutée avec succès!")
    else:
        print("ℹ️  La colonne photo_url existe déjà.")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur: {e}")
