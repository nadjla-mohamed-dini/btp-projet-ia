from flask import Flask
import os

app = Flask(__name__, static_folder='.', static_url_path='')

# Questions du quiz (importées du quiz.py)
def get_questions():
    return [
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
