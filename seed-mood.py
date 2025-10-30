# -*- coding: utf-8 -*-
from models import db, User, Mood
from datetime import datetime

# 🔹 Étape 1 : Créer un utilisateur simple
user = User(
    username='nadjla',
    email='nadjla@example.com',
    password='test123',  # mot de passe en clair pour test
    created_at=datetime.utcnow()
)
db.session.add(user)
db.session.commit()

print(f"✅ Utilisateur créé avec ID : {user.id}")

# 🔹 Étape 2 : Ajouter les moods liés à cet utilisateur
moods = ["joyeux", "heureux", "très triste", "amoureux", "énervé", "peur"]

for m in moods:
    db.session.add(Mood(
        mood_type=m,
        user_id=user.id,
        created_at=datetime.utcnow()
    ))

db.session.commit()
print("✅ Moods ajoutés avec succès !")
