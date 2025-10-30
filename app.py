#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Enable CORS
CORS(app, supports_credentials=True)

# Configuration
db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'password')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', 5432)
db_name = os.environ.get('DB_NAME', 'feelflix')

database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Import models and initialize db
from models import db, User, Mood, Movie, Profile

# Initialize db with app
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


# API Endpoints - Films
@app.route('/api/movies')
def get_movies():
    mood = request.args.get('mood')
    if mood:
        moods = Mood.query.filter_by(mood_type=mood).all()
        movies = []
        for m in moods:
            movies.extend([movie.__dict__ for movie in m.movies])
        return jsonify(movies)
    else:
        movies = Movie.query.all()
        return jsonify([{
            'id': m.id,
            'title': m.title,
            'description': m.description,
            'genre': m.genre,
            'rating': m.rating,
            'image_url': m.image_url
        } for m in movies])


if __name__ == '__main__':
    with app.app_context():
        init_db()
    print("🎬 Feelflix démarre sur http://localhost:5000")
    app.run(debug=True, port=5000)
