# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request
from models import db
from config import get_config
from dotenv import load_dotenv
from sqlalchemy import text
from models import Mood, Movie
from flask_migrate import Migrate


load_dotenv()

app = Flask(__name__)
app.config.from_object(get_config("development"))
db.init_app(app)
migrate = Migrate(app, db)



@app.route('/')
def home():
    return jsonify({"message": "Bienvenue sur Feelflix - Application Flask avec PostgreSQL"})


@app.route('/mood')
def mood():
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
