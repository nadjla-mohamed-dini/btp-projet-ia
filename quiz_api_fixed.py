from flask import Flask, jsonify, request

app = Flask(__name__, static_folder='.', static_url_path='')

# Questions du quiz
questions = [
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

@app.route('/')
def index():
    return app.send_static_file('accueil.html')

@app.route('/api/questions')
def get_questions():
    questions_sans_reponses = []
    for q in questions:
        questions_sans_reponses.append({
            "question": q["question"],
            "choix": q["choix"]
        })
    return jsonify(questions_sans_reponses)

@app.route('/api/verifier', methods=['POST'])
def verifier_reponse():
    data = request.json
    question_index = data.get('questionIndex')
    reponse_index = data.get('reponseIndex')

    if question_index is None or reponse_index is None:
        return jsonify({"error": "Données manquantes"}), 400

    if not (0 <= question_index < len(questions)):
        return jsonify({"error": "Question invalide"}), 400

    est_correct = questions[question_index]["reponse_correcte"] == reponse_index
    bonne_reponse = questions[question_index]["choix"][questions[question_index]["reponse_correcte"]]

    return jsonify({
        "correct": est_correct,
        "bonneReponse": bonne_reponse
    })

@app.route('/api/films/<mood>')
def get_films_by_mood(mood):
    # Exemple simple de films par humeur (demo)
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
        ]
    }

    key = mood.lower()
    aliases = {
        'enerve': 'énervé',
        'enervé': 'énervé',
        'énervé': 'énervé'
    }
    if key in aliases:
        key = aliases[key]

    return jsonify(films.get(key, []))

if __name__ == '__main__':
    app.run(debug=True)
