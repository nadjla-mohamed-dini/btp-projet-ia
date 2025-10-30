from flask import Flask, jsonify, request
import os

app = Flask(__name__, static_folder='.', static_url_path='')

# Questions du quiz (importées du quiz.py)
questions = [
    {
        "question": "Qui a réalisé le film 'Titanic' (1997) ?",
        "choix": ["Steven Spielberg", "James Cameron", "Christopher Nolan", "Martin Scorsese"],
        "reponse_correcte": 1
    },
    {
        "question": "Quel acteur joue le rôle de Jack Sparrow dans 'Pirates des Caraïbes' ?",
        "choix": [
            "Orlando Bloom",
            "Brad Pitt",
            "Johnny Depp",
            "Tom Cruise"
        ],
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
    # Retourne uniquement la question et les choix (pas la réponse)
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

if __name__ == '__main__':
    app.run(debug=True)