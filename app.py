from flask import Flask, jsonify, request
import os
import requests
from models import db, Movie, Mood
from config import get_config

app = Flask(__name__, static_folder='.', static_url_path='')
app.config.from_object(get_config())
db.init_app(app)


@app.route('/')
def home():
    # Serve the interactive home page
    return app.send_static_file('accueil.html')


def map_value_to_mood(value: int) -> str:
    if value <= 10:
        return 'très triste'
    if value <= 30:
        return 'peur'
    if value <= 45:
        return 'énervé'
    if value <= 55:
        return 'neutre'
    if value <= 70:
        return 'heureux'
    if value <= 85:
        return 'joyeux'
    return 'amoureux'


@app.route('/api/films')
def get_films_by_mood_api():
    # Accept either ?value=0-100 or ?mood=string
    value = request.args.get('value')
    mood = request.args.get('mood')
    if value is not None:
        try:
            value = int(value)
            mood = map_value_to_mood(value)
        except ValueError:
            pass

    if mood:
        mood = mood.lower()

    # Simple demo mapping; replace with real DB query if needed
    films = {
        "joyeux": [
            {"title": "Le Grand Saut", "description": "Une comédie optimiste.", "genre": "Comédie", "rating": 7.2, "poster_url": "https://via.placeholder.com/300x450?text=Le+Grand+Saut"},
            {"title": "Sourires Partout", "description": "Une histoire qui redonne le sourire.", "genre": "Comédie", "rating": 6.8, "poster_url": "https://via.placeholder.com/300x450?text=Sourires+Partout"}
        ],
        "heureux": [
            {"title": "Voyage en fête", "description": "Aventure joyeuse.", "genre": "Aventure", "rating": 7.5, "poster_url": "https://via.placeholder.com/300x450?text=Voyage+en+fete"}
        ],
        "très triste": [
            {"title": "Nuit Silencieuse", "description": "Drame contemplatif.", "genre": "Drame", "rating": 7.9, "poster_url": "https://via.placeholder.com/300x450?text=Nuit+Silencieuse"}
        ],
        "amoureux": [
            {"title": "Coeurs Entrelacés", "description": "Romance touchante.", "genre": "Romance", "rating": 7.0, "poster_url": "https://via.placeholder.com/300x450?text=Coeurs+Entrelaces"}
        ],
        "énervé": [
            {"title": "Tempête Urbaine", "description": "Action intense.", "genre": "Action", "rating": 6.9, "poster_url": "https://via.placeholder.com/300x450?text=Tempete+Urbaine"}
        ],
        "peur": [
            {"title": "Ombres", "description": "Film d'horreur pour frissonner.", "genre": "Horreur", "rating": 6.4, "poster_url": "https://via.placeholder.com/300x450?text=Ombres"}
        ],
        "neutre": [
            {"title": "Le Voyage", "description": "Film universel pour tous les goûts.", "genre": "Aventure", "rating": 6.8, "poster_url": "https://via.placeholder.com/300x450?text=Le+Voyage"}
        ]
    }

    # If a database exists and movies table contains entries, try to query DB first
    def fetch_tmdb_poster(title: str):
        api_key = os.environ.get('TMDB_API_KEY')
        if not api_key or not title:
            return None
        try:
            url = 'https://api.themoviedb.org/3/search/movie'
            params = {'api_key': api_key, 'query': title, 'language': 'fr-FR'}
            resp = requests.get(url, params=params, timeout=4)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('results'):
                    poster_path = data['results'][0].get('poster_path')
                    if poster_path:
                        return f'https://image.tmdb.org/t/p/w500{poster_path}'
        except Exception:
            pass
        return None

    try:
        with app.app_context():
            results = Movie.query.join(Mood).filter(Mood.mood_type == mood).all()
            if results:
                movies_list = []
                for m in results:
                    movies_list.append({
                        'title': m.title,
                        'description': m.description or '',
                        'genre': m.genre or '',
                        'rating': m.rating or 0,
                        'poster_url': getattr(m, 'poster_url', None)
                    })
                # Enrich with TMDB poster when missing
                for movie in movies_list:
                    if not movie.get('poster_url'):
                        tmdb_url = fetch_tmdb_poster(movie.get('title'))
                        if tmdb_url:
                            movie['poster_url'] = tmdb_url
                        else:
                            movie['poster_url'] = f'https://via.placeholder.com/300x450?text={movie.get("title", "Movie").replace(" ", "+")}'
                return jsonify(movies_list)
    except Exception:
        # If anything goes wrong while accessing DB, fall back to demo mapping
        pass

    key = mood if mood in films else 'neutre'
    return jsonify(films.get(key, []))


@app.route('/health')
def health():
    try:
        with app.app_context():
            db.session.execute('SELECT 1')
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
