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
    limit = request.args.get('limit', type=int, default=16)  # Default to 16 films for carousel
    
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
            {"title": "Sourires Partout", "description": "Une histoire qui redonne le sourire.", "genre": "Comédie", "rating": 6.8, "poster_url": "https://via.placeholder.com/300x450?text=Sourires+Partout"},
            {"title": "La Fête Continue", "description": "Une célébration de la joie.", "genre": "Comédie", "rating": 7.5, "poster_url": "https://via.placeholder.com/300x450?text=La+Fete+Continue"},
            {"title": "Rires Garantis", "description": "Comédie hilarante.", "genre": "Comédie", "rating": 7.1, "poster_url": "https://via.placeholder.com/300x450?text=Rires+Garantis"},
            {"title": "Le Bonheur Simple", "description": "Une histoire réconfortante.", "genre": "Comédie", "rating": 6.9, "poster_url": "https://via.placeholder.com/300x450?text=Le+Bonheur+Simple"},
            {"title": "Soleil et Joie", "description": "Film ensoleillé.", "genre": "Comédie", "rating": 7.3, "poster_url": "https://via.placeholder.com/300x450?text=Soleil+et+Joie"},
            {"title": "Éclats de Rire", "description": "Comédie légère.", "genre": "Comédie", "rating": 6.7, "poster_url": "https://via.placeholder.com/300x450?text=Eclats+de+Rire"},
            {"title": "La Vie en Rose", "description": "Optimisme et bonne humeur.", "genre": "Comédie", "rating": 7.4, "poster_url": "https://via.placeholder.com/300x450?text=La+Vie+en+Rose"}
        ],
        "heureux": [
            {"title": "Voyage en fête", "description": "Aventure joyeuse.", "genre": "Aventure", "rating": 7.5, "poster_url": "https://via.placeholder.com/300x450?text=Voyage+en+fete"},
            {"title": "Horizons Lointains", "description": "Découverte et émerveillement.", "genre": "Aventure", "rating": 7.8, "poster_url": "https://via.placeholder.com/300x450?text=Horizons+Lointains"},
            {"title": "L'Esprit d'Aventure", "description": "Exploration passionnante.", "genre": "Aventure", "rating": 7.6, "poster_url": "https://via.placeholder.com/300x450?text=LEsprit+dAventure"},
            {"title": "Chemins de Joie", "description": "Parcours inspirant.", "genre": "Aventure", "rating": 7.2, "poster_url": "https://via.placeholder.com/300x450?text=Chemins+de+Joie"},
            {"title": "Découvertes", "description": "Nouvelles expériences.", "genre": "Aventure", "rating": 7.0, "poster_url": "https://via.placeholder.com/300x450?text=Decouvertes"},
            {"title": "Le Monde Attend", "description": "Aventure épique.", "genre": "Aventure", "rating": 7.7, "poster_url": "https://via.placeholder.com/300x450?text=Le+Monde+Attend"},
            {"title": "Étapes Heureuses", "description": "Voyage émotionnel.", "genre": "Aventure", "rating": 7.3, "poster_url": "https://via.placeholder.com/300x450?text=Etapes+Heureuses"},
            {"title": "Lumières Nouvelles", "description": "Éclairage positif.", "genre": "Aventure", "rating": 7.1, "poster_url": "https://via.placeholder.com/300x450?text=Lumieres+Nouvelles"}
        ],
        "très triste": [
            {"title": "Nuit Silencieuse", "description": "Drame contemplatif.", "genre": "Drame", "rating": 7.9, "poster_url": "https://via.placeholder.com/300x450?text=Nuit+Silencieuse"},
            {"title": "Larmes Secrètes", "description": "Émotions profondes.", "genre": "Drame", "rating": 8.1, "poster_url": "https://via.placeholder.com/300x450?text=Larmes+Secretes"},
            {"title": "L'Adieu", "description": "Séparation douloureuse.", "genre": "Drame", "rating": 7.8, "poster_url": "https://via.placeholder.com/300x450?text=LAdieu"},
            {"title": "Mélancolie", "description": "Réflexion intime.", "genre": "Drame", "rating": 7.6, "poster_url": "https://via.placeholder.com/300x450?text=Melancolie"},
            {"title": "Ombres du Passé", "description": "Souvenirs douloureux.", "genre": "Drame", "rating": 7.7, "poster_url": "https://via.placeholder.com/300x450?text=Ombres+du+Passe"},
            {"title": "Le Poids des Mots", "description": "Drame poignant.", "genre": "Drame", "rating": 8.0, "poster_url": "https://via.placeholder.com/300x450?text=Le+Poids+des+Mots"},
            {"title": "Solitude", "description": "Isolement émotionnel.", "genre": "Drame", "rating": 7.5, "poster_url": "https://via.placeholder.com/300x450?text=Solitude"},
            {"title": "Cœur Brisé", "description": "Perte et acceptation.", "genre": "Drame", "rating": 7.9, "poster_url": "https://via.placeholder.com/300x450?text=Coeur+Brise"}
        ],
        "amoureux": [
            {"title": "Coeurs Entrelacés", "description": "Romance touchante.", "genre": "Romance", "rating": 7.0, "poster_url": "https://via.placeholder.com/300x450?text=Coeurs+Entrelaces"},
            {"title": "Premier Regard", "description": "Rencontre magique.", "genre": "Romance", "rating": 7.4, "poster_url": "https://via.placeholder.com/300x450?text=Premier+Regard"},
            {"title": "L'Amour en Fleurs", "description": "Romance printanière.", "genre": "Romance", "rating": 7.2, "poster_url": "https://via.placeholder.com/300x450?text=LAmour+en+Fleurs"},
            {"title": "Sous les Étoiles", "description": "Nuit romantique.", "genre": "Romance", "rating": 7.6, "poster_url": "https://via.placeholder.com/300x450?text=Sous+les+Etoiles"},
            {"title": "Passion Éternelle", "description": "Amour durable.", "genre": "Romance", "rating": 7.3, "poster_url": "https://via.placeholder.com/300x450?text=Passion+Eternelle"},
            {"title": "Deux Destins", "description": "Rencontre du destin.", "genre": "Romance", "rating": 7.5, "poster_url": "https://via.placeholder.com/300x450?text=Deux+Destins"},
            {"title": "Le Baiser", "description": "Moment parfait.", "genre": "Romance", "rating": 7.1, "poster_url": "https://via.placeholder.com/300x450?text=Le+Baiser"},
            {"title": "Cœur à Cœur", "description": "Intimité romantique.", "genre": "Romance", "rating": 7.4, "poster_url": "https://via.placeholder.com/300x450?text=Coeur+a+Coeur"}
        ],
        "énervé": [
            {"title": "Tempête Urbaine", "description": "Action intense.", "genre": "Action", "rating": 6.9, "poster_url": "https://via.placeholder.com/300x450?text=Tempete+Urbaine"},
            {"title": "Rage Contrôlée", "description": "Tension explosive.", "genre": "Action", "rating": 7.2, "poster_url": "https://via.placeholder.com/300x450?text=Rage+Controlee"},
            {"title": "Fureur", "description": "Conflit intense.", "genre": "Action", "rating": 7.0, "poster_url": "https://via.placeholder.com/300x450?text=Fureur"},
            {"title": "Révolte", "description": "Résistance.", "genre": "Action", "rating": 7.3, "poster_url": "https://via.placeholder.com/300x450?text=Revolte"},
            {"title": "L'Explosion", "description": "Action brutale.", "genre": "Action", "rating": 6.8, "poster_url": "https://via.placeholder.com/300x450?text=LExplosion"},
            {"title": "Combat Final", "description": "Confrontation ultime.", "genre": "Action", "rating": 7.1, "poster_url": "https://via.placeholder.com/300x450?text=Combat+Final"},
            {"title": "Vengeance", "description": "Justice personnelle.", "genre": "Action", "rating": 7.4, "poster_url": "https://via.placeholder.com/300x450?text=Vengeance"},
            {"title": "Intensité", "description": "Action pure.", "genre": "Action", "rating": 6.9, "poster_url": "https://via.placeholder.com/300x450?text=Intensite"}
        ],
        "peur": [
            {"title": "Ombres", "description": "Film d'horreur pour frissonner.", "genre": "Horreur", "rating": 6.4, "poster_url": "https://via.placeholder.com/300x450?text=Ombres"},
            {"title": "La Maison Hantée", "description": "Terreur nocturne.", "genre": "Horreur", "rating": 6.8, "poster_url": "https://via.placeholder.com/300x450?text=La+Maison+Hantee"},
            {"title": "Cri dans la Nuit", "description": "Suspense terrifiant.", "genre": "Horreur", "rating": 6.6, "poster_url": "https://via.placeholder.com/300x450?text=Cri+dans+la+Nuit"},
            {"title": "L'Inconnu", "description": "Mystère effrayant.", "genre": "Horreur", "rating": 6.9, "poster_url": "https://via.placeholder.com/300x450?text=LInconnu"},
            {"title": "Frissons", "description": "Peur constante.", "genre": "Horreur", "rating": 6.5, "poster_url": "https://via.placeholder.com/300x450?text=Frissons"},
            {"title": "L'Épouvante", "description": "Horreur psychologique.", "genre": "Horreur", "rating": 6.7, "poster_url": "https://via.placeholder.com/300x450?text=LEpouvante"},
            {"title": "Ténèbres", "description": "Obscurité menaçante.", "genre": "Horreur", "rating": 6.8, "poster_url": "https://via.placeholder.com/300x450?text=Tenebres"},
            {"title": "Le Cauchemar", "description": "Terreur onirique.", "genre": "Horreur", "rating": 6.6, "poster_url": "https://via.placeholder.com/300x450?text=Le+Cauchemar"}
        ],
        "neutre": [
            {"title": "Le Voyage", "description": "Film universel pour tous les goûts.", "genre": "Aventure", "rating": 6.8, "poster_url": "https://via.placeholder.com/300x450?text=Le+Voyage"},
            {"title": "Équilibre", "description": "Histoire équilibrée.", "genre": "Drame", "rating": 7.0, "poster_url": "https://via.placeholder.com/300x450?text=Equilibre"},
            {"title": "Moment Présent", "description": "Réflexion calme.", "genre": "Drame", "rating": 6.9, "poster_url": "https://via.placeholder.com/300x450?text=Moment+Present"},
            {"title": "Sérénité", "description": "Paix intérieure.", "genre": "Drame", "rating": 7.1, "poster_url": "https://via.placeholder.com/300x450?text=Serenite"},
            {"title": "L'Horizon", "description": "Vue d'ensemble.", "genre": "Aventure", "rating": 6.9, "poster_url": "https://via.placeholder.com/300x450?text=LHorizon"},
            {"title": "Calme", "description": "Tranquillité.", "genre": "Drame", "rating": 7.0, "poster_url": "https://via.placeholder.com/300x450?text=Calme"},
            {"title": "Perspective", "description": "Point de vue neutre.", "genre": "Drame", "rating": 6.8, "poster_url": "https://via.placeholder.com/300x450?text=Perspective"},
            {"title": "L'Essentiel", "description": "Simplicité.", "genre": "Drame", "rating": 7.1, "poster_url": "https://via.placeholder.com/300x450?text=LEssentiel"}
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

    def make_no_poster_data_url(title: str) -> str:
            # small SVG fallback so the browser always finds an image
            if not title:
                title = 'No poster'
            svg = (
                f"<svg xmlns='http://www.w3.org/2000/svg' width='300' height='450' viewBox='0 0 300 450'>"
                "<rect width='100%' height='100%' fill='%23f3f4f6'/>"
                f"<text x='50%' y='50%' font-size='16' text-anchor='middle' fill='%23666' font-family='Arial, Helvetica, sans-serif' dy='.3em'>{title}</text>"
                "</svg>"
            )
            import urllib.parse
            data = 'data:image/svg+xml;utf8,' + urllib.parse.quote(svg)
            return data

    def is_placeholder_url(url: str) -> bool:
        if not url:
            return True
        url = url.lower()
        return ('placeholder.com' in url) or ('via.placeholder' in url)

    try:
        with app.app_context():
            results = Movie.query.join(Mood).filter(Mood.mood_type == mood).all()
            if results:
                movies_list = []
                for m in results:
                    poster = getattr(m, 'poster_url', None)
                    if is_placeholder_url(poster):
                        poster = None
                    movies_list.append({
                        'title': m.title,
                        'description': m.description or '',
                        'genre': m.genre or '',
                        'rating': m.rating or 0,
                        'poster_url': poster
                    })
                # Enrich with TMDB poster when missing
                for movie in movies_list:
                        if not movie.get('poster_url'):
                            tmdb_url = fetch_tmdb_poster(movie.get('title'))
                            if tmdb_url:
                                movie['poster_url'] = tmdb_url
                            else:
                                movie['poster_url'] = make_no_poster_data_url(movie.get('title'))
                # Limit results if specified
                if limit and len(movies_list) > limit:
                    movies_list = movies_list[:limit]
                return jsonify(movies_list)
    except Exception:
        # If anything goes wrong while accessing DB, fall back to demo mapping
        pass

    key = mood if mood in films else 'neutre'
    demo_list = films.get(key, [])
    # Enrich demo mapping posters with TMDB posters if placeholder used
    enriched = []
    for f in demo_list:
        poster = f.get('poster_url')
        if is_placeholder_url(poster):
            tmdb_p = fetch_tmdb_poster(f.get('title'))
            if tmdb_p:
                poster = tmdb_p
            else:
                poster = make_no_poster_data_url(f.get('title'))
        enriched.append({
            'title': f.get('title'),
            'description': f.get('description'),
            'genre': f.get('genre'),
            'rating': f.get('rating'),
            'poster_url': poster
        })
    # Limit results if specified
    if limit and len(enriched) > limit:
        enriched = enriched[:limit]
    return jsonify(enriched)


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
