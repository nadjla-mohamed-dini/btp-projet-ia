#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script d'initialisation de la base de données Feelflix
Crée toutes les tables nécessaires
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement AVANT d'importer app
load_dotenv()

from app import app, db

def init_database():
    """Initialise la base de données"""
    print("🔧 Initialisation de la base de données Feelflix...")
    
    try:
        with app.app_context():
            print("📊 Création des tables...")
            db.create_all()
            print("✅ Tables créées avec succès!")
            
            print("\n📋 Tables créées:")
            print("   - users")
            print("   - moods")
            print("   - movies")
            print("   - profiles")
            
            print("\n✨ Base de données initialisée!")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = init_database()
    exit(0 if success else 1)
