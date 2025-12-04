# 🎬 Feelflix - Stack Complète

## 📋 Structure du Projet

```
btp-projet-ia/
├── app.py                    # Backend Flask + SQLAlchemy
├── config.py                 # Configuration par environnement
├── models.py                 # Models SQLAlchemy (User, Mood, Movie)
├── init_db.py                # Script d'init DB
├── .env                       # Variables d'environnement
├── templates/
│   ├── index.html            # Page d'accueil
│   ├── formulaire.html       # Connexion & Inscription
│   └── profile.html          # Profil utilisateur
├── static/
│   └── profile.css           # Styles CSS
├── start.bat / start.sh      # Scripts de démarrage
└── feelflix.db               # Base de données SQLite
```

## 🚀 Démarrage Rapide

### 1. Installation des dépendances
```bash
pip install flask flask-sqlalchemy python-dotenv
```

### 2. Lancer l'application
```bash
python app.py
```

Ou double-cliquez `start.bat` (Windows)

L'app sera disponible sur: **http://localhost:5000**

## 🗄️ Base de Données (SQLAlchemy + SQLite)

### Tables créées automatiquement:
- **users** - Profils utilisateurs avec authentification
  - username, email, password (hashé)
  - favorite_quote, favorite_actor, favorite_director, favorite_movie, favorite_series
- **moods** - Humeurs associées aux utilisateurs
- **movies** - Films recommandés par humeur

## 🔧 API Endpoints

### Authentification
- `POST /api/auth/signup` - Inscription
- `POST /api/auth/login` - Connexion
- `POST /api/auth/logout` - Déconnexion

### Profil
- `GET /api/profile/<user_id>` - Récupère le profil
- `PUT /api/profile/<user_id>` - Met à jour le profil

### Films
- `GET /api/movies` - Liste tous les films
- `GET /api/movies?mood=joyeux` - Films par humeur

## 🔐 Sécurité

- ✅ Mots de passe hashés avec werkzeug
- ✅ Sessions HTTP-only
- ✅ Variables d'environnement
- ✅ CSRF protection (à ajouter)

## 💡 Comment ça marche?

### Frontend
- **formulaire.html** - Connexion/Inscription avec fetch API
- **profile.html** - Profil avec save/cancel
- **index.html** - Accueil avec grille d'humeurs

### Backend (Flask + SQLAlchemy)
- ORM simple et puissant
- Pas de queries raw SQL complexes
- Migrations faciles

### Base de données (SQLite)
- Un fichier `feelflix.db` créé automatiquement
- Parfait pour développement
- Migratable vers PostgreSQL en prod

## ✅ À tester à chaque étape

1. **Jour 1-2**: 
   - ✓ Inscription/Connexion fonctionnent
   - ✓ Profil sauvegarde données

2. **Jour 3-4**: 
   - Quiz + API films
   - Recommandations par humeur

3. **Jour 5-7**: 
   - Playlists
   - Filtres avancés

4. **Jour 8-10**: 
   - Polish UI
   - Tests

## 📝 Prochaines étapes

1. **Ajouter des films** à la DB (seed data)
2. **Créer page Quiz** 
3. **Implémenter recommandations** d'humeur
4. **Créer Playlists**
5. **Spotify integration**

---

**Stack final:**
- Backend: **Flask + SQLAlchemy** (ORM)
- Frontend: **HTML/CSS/JS vanilla**
- DB: **SQLite** (fichier local)

**Avantages:**
- ✅ Zéro déploiement, fonctionne en local
- ✅ Facile à débugger
- ✅ ORM robuste pour complexité future
- ✅ Authentification sécurisée
- ✅ Testable à chaque étape

