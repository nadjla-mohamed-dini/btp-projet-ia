#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour ajouter la colonne tmdb_id à la table movies
"""

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_NAME = os.environ.get('DB_NAME', 'feelflix')

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
        print("⏳ Ajout de la colonne tmdb_id à la table movies...")
        c.execute("""
            ALTER TABLE movies ADD COLUMN tmdb_id INTEGER
        """)
        conn.commit()
        print("✅ Colonne tmdb_id ajoutée avec succès!")
    else:
        print("ℹ️  La colonne tmdb_id existe déjà")
    
    c.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
