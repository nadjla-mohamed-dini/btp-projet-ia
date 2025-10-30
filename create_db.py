#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour créer la base de données directement
"""

import sqlite3
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

DATABASE = 'feelflix.db'

# Remove old database if exists
if os.path.exists(DATABASE):
    os.remove(DATABASE)

print("🔧 Initialisation de la base de données Feelflix...")

conn = sqlite3.connect(DATABASE)
c = conn.cursor()

# Create users table
c.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

# Create moods table
c.execute('''CREATE TABLE moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    mood_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)''')

# Create movies table
c.execute('''CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    genre TEXT,
    rating REAL,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(mood_id) REFERENCES moods(id)
)''')

# Create profiles table
c.execute('''CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    citation TEXT,
    acteur TEXT,
    realisateur TEXT,
    film TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)''')

conn.commit()

# Verify
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()

print(f"✅ Tables créées avec succès!")
print(f"✓ {len(tables)} tables dans la base de données:")
for table in tables:
    print(f"   - {table[0]}")

conn.close()



