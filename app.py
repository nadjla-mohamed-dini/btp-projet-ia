# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request, session, redirect, url_for, send_from_directory
from models import db
from config import get_config
from dotenv import load_dotenv
from sqlalchemy import text
from models import Mood, Movie, User, Profile
from flask_migrate import Migrate
from quiz.quiz_api import get_questions
from flask_cors import CORS
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os




load_dotenv()
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config.from_object(get_config("development"))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db.init_app(app)
migrate = Migrate(app, db)

CORS(app, supports_credentials=True)

db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'password')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', 5432)
db_name = os.environ.get('DB_NAME', 'Fellflix')

database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True


@app.route('/')
def home():
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
    return render_template('quiz.html')


@app.route('/api/questions')
def api_questions():
    questions = get_questions()
    return jsonify([
        {"question": q["question"], "choix": q["choix"]}
        for q in questions
    ])

@app.route('/api/verifier', methods=['POST'])
def verifier_reponse():
    data = request.get_json()
    question_index = data.get('questionIndex')
    reponse_index = data.get('reponseIndex')

    questions = get_questions()
    bonne_reponse_index = questions[question_index]['reponse_correcte']
    bonne_reponse_texte = questions[question_index]['choix'][bonne_reponse_index]

    return jsonify({
        "correct": reponse_index == bonne_reponse_index,
        "bonneReponse": bonne_reponse_texte
    })



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
