#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'password')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', 5432)
db_name = os.environ.get('DB_NAME', 'feelflix')

database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Import models after app creation
from models import db, User, Mood, Movie, Profile

# Initialize db
db.init_app(app)

# Configuration des uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Enable CORS
CORS(app, supports_credentials=True)

# Import models and initialize db
from models import db, User, Mood, Movie, Profile

db.init_app(app)


def init_db():
    with app.app_context():
        db.create_all()
        print("✓ Base de données créée avec SQLAlchemy")


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/formulaire')
def formulaire():
    return render_template('formulaire.html')


@app.route('/mood')
def mood():
    if 'user_id' not in session:
        return redirect(url_for('formulaire'))
    return render_template('mood.html')

@app.route('/health')
def health():
    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500
    

@app.route('/api/films/<mood_type>')
def get_films_by_mood(mood_type):
    mood = Mood.query.filter_by(mood_type=mood_type).first()
    if not mood:
        return jsonify({'error': 'Mood not found'}), 404

    films = Movie.query.filter_by(mood_id=mood.id).limit(5).all()
    return jsonify([
    {
        "title": film.title,
        "description": film.description,
        "genre": film.genre,
        "rating": film.rating,
        "poster_url": film.poster_url
    }
    for film in films
])

@app.route('/quiz')
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('formulaire'))
    return render_template('quiz.html')


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('formulaire'))
    return render_template('profile.html')


# API Endpoints - Authentification
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        print(f"DEBUG signup - Data reçue: {data}")
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            msg = 'Champs manquants'
            print(f"DEBUG signup - {msg}")
            return jsonify({'status': 'error', 'message': msg}), 400
        
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()

        default_moods = ["joyeux", "heureux", "très triste", "amoureux", "énervé", "peur"]
        for m in default_moods:
            db.session.add(Mood(mood_type=m, user_id=user.id))
        db.session.commit()
        
        session['user_id'] = user.id
        session['username'] = user.username
        
        print(f"DEBUG signup - User créé: {user.username}")
        return jsonify({'status': 'success', 'user_id': user.id}), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Erreur signup: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = User.query.filter_by(email=data.get('email')).first()
    
    if user and user.check_password(data.get('password')):
        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({'status': 'success', 'user_id': user.id})
    
    return jsonify({'status': 'error', 'message': 'Email ou mot de passe incorrect'}), 401


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'status': 'success'})


@app.route('/api/user-info', methods=['GET'])
def get_user_info():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Non authentifié'}), 401
    return jsonify({'user_id': session['user_id'], 'username': session['username']})


# API Endpoints - Profil
@app.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'Utilisateur non trouvé'}), 404
    
    profile = Profile.query.filter_by(user_id=user_id).first()
    
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        },
        'profile': profile.to_dict() if profile else None
    })


@app.route('/api/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'Utilisateur non trouvé'}), 404
    
    data = request.get_json()
    print(f"DEBUG - Mise à jour profil user_id={user_id}, data={data}")
    
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        print(f"DEBUG - Création nouveau profil pour user_id={user_id}")
        profile = Profile(user_id=user_id)
        db.session.add(profile)
    
    profile.citation = data.get('favorite_quote', profile.citation)
    profile.acteur = data.get('favorite_actor', profile.acteur)
    profile.realisateur = data.get('favorite_director', profile.realisateur)
    profile.film = data.get('favorite_movie', profile.film)
    
    db.session.commit()
    print(f"DEBUG - Profil sauvegardé: citation={profile.citation}, acteur={profile.acteur}, realisateur={profile.realisateur}, film={profile.film}")
    return jsonify({'status': 'success', 'profile': profile.to_dict()})


@app.route('/api/profile/<int:user_id>/photo', methods=['POST'])
def upload_profile_photo(user_id):
    if 'photo' not in request.files:
        return jsonify({'status': 'error', 'message': 'Aucun fichier photo'}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'Fichier vide'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'status': 'error', 'message': 'Format de fichier non autorisé'}), 400
    
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'status': 'error', 'message': 'Utilisateur non trouvé'}), 404
        
        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            profile = Profile(user_id=user_id)
            db.session.add(profile)
        
        # Créer un nom de fichier unique
        filename = secure_filename(f"{user_id}_{datetime.utcnow().timestamp()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Créer le dossier s'il n'existe pas
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Sauvegarder le fichier
        file.save(filepath)
        
        # Enregistrer l'URL dans la base de données
        profile.photo_url = f"/uploads/{filename}"
        db.session.commit()
        
        print(f"DEBUG - Photo uploadée: user_id={user_id}, filename={filename}")
        return jsonify({'status': 'success', 'photo_url': profile.photo_url})
    except Exception as e:
        db.session.rollback()
        print(f"Erreur upload photo: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Quiz Questions
QUIZ_QUESTIONS = [
    {
        "question": "Qui a réalisé le film 'Titanic' (1997) ?",
        "choix": ["Steven Spielberg", "James Cameron", "Christopher Nolan", "Martin Scorsese"],
        "reponse_correcte": 1
    },
    {
        "question": "Quel acteur joue le rôle de Jack Sparrow dans 'Pirates des Caraïbes' ?",
        "choix": ["Orlando Bloom", "Brad Pitt", "Johnny Depp", "Tom Cruise"],
        "reponse_correcte": 2
    },
    {
        "question": "Dans quel film trouve-t-on la réplique culte 'Que la Force soit avec toi' ?",
        "choix": ["Star Trek", "Star Wars", "Guardians of the Galaxy", "Interstellar"],
        "reponse_correcte": 1
    },
    {
        "question": "Quel film a remporté l'Oscar du meilleur film en 2020 ?",
        "choix": ["1917", "Joker", "Parasite", "Once Upon a Time in Hollywood"],
        "reponse_correcte": 2
    },
    {
        "question": "Qui joue le rôle de Tony Stark / Iron Man dans l'univers Marvel ?",
        "choix": ["Chris Evans", "Chris Hemsworth", "Robert Downey Jr.", "Mark Ruffalo"],
        "reponse_correcte": 2
    }
]


# API Endpoints - Quiz
@app.route('/api/quiz/questions', methods=['GET'])
def get_quiz_questions():
    questions_sans_reponses = []
    for q in QUIZ_QUESTIONS:
        questions_sans_reponses.append({
            "question": q["question"],
            "choix": q["choix"]
        })
    return jsonify(questions_sans_reponses)


@app.route('/api/quiz/verifier', methods=['POST'])
def verify_quiz_answer():
    data = request.get_json()
    question_index = data.get('questionIndex')
    reponse_index = data.get('reponseIndex')
    
    if question_index is None or reponse_index is None:
        return jsonify({'status': 'error', 'message': 'Données manquantes'}), 400
    
    if not (0 <= question_index < len(QUIZ_QUESTIONS)):
        return jsonify({'status': 'error', 'message': 'Question invalide'}), 400
    
    est_correct = QUIZ_QUESTIONS[question_index]["reponse_correcte"] == reponse_index
    bonne_reponse = QUIZ_QUESTIONS[question_index]["choix"][QUIZ_QUESTIONS[question_index]["reponse_correcte"]]
    
    return jsonify({
        'status': 'success',
        'correct': est_correct,
        'bonneReponse': bonne_reponse
    })


# API Endpoints - Films/Mood
@app.route('/api/mood/films', methods=['GET'])
def get_mood_films():
    mood_value = request.args.get('mood')
    if not mood_value:
        return jsonify({'status': 'error', 'message': 'Mood manquant'}), 400
    
    try:
        mood_value = int(mood_value)
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Mood doit être un nombre'}), 400
    
    # Mapper les valeurs de mood aux types
    mood_map = {
        0: 'très triste',
        20: 'triste',
        35: 'joyeux',
        50: 'énervé',
        75: 'heureux',
        85: 'amoureux',
        100: 'peur'
    }
    
    # Trouver le mood_type le plus proche
    mood_type = mood_map.get(mood_value)
    
    if not mood_type:
        # Trouver le mood_type le plus proche
        closest_mood = min(mood_map.items(), key=lambda x: abs(x[0] - mood_value))
        mood_type = closest_mood[1]
    
    # Chercher les films associés à ce mood
    moods = Mood.query.filter_by(mood_type=mood_type).all()
    
    if not moods:
        # Créer un mood s'il n'existe pas
        new_mood = Mood(mood_type=mood_type, user_id=session.get('user_id', 1))
        db.session.add(new_mood)
        db.session.commit()
        moods = [new_mood]
    
    movies = []
    for m in moods:
        movies.extend([movie.to_dict() for movie in m.movies])
    
    return jsonify({
        'status': 'success',
        'mood_type': mood_type,
        'movies': movies
    })


@app.route('/api/movies')
def get_movies():
    mood = request.args.get('mood')
    if mood:
        moods = Mood.query.filter_by(mood_type=mood).all()
        movies = []
        for m in moods:
            movies.extend([movie.to_dict() for movie in m.movies])
        return jsonify(movies)
    else:
        movies = Movie.query.all()
        return jsonify([m.to_dict() for m in movies])


if __name__ == '__main__':
    with app.app_context():
        init_db()
    print("🎬 Feelflix démarre sur http://localhost:5000")
    app.run(debug=True, port=5000)
