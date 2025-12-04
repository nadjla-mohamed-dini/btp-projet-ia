"""
Module de quiz interactif en Python sur le thème du CINÉMA
Permet de poser des questions à choix multiples et de calculer un score
"""


def afficher_question(question, choix, numero):
    """
    Affiche une question avec ses choix de réponses
    
    Args:
        question (str): Le texte de la question
        choix (list): Liste des choix possibles
        numero (int): Numéro de la question
    """
    print(f"\n{'='*60}")
    print(f"Question {numero}")
    print(f"{'='*60}")
    print(f"\n{question}\n")
    
    for i, choix_texte in enumerate(choix, 1):
        print(f"  {i}. {choix_texte}")
    print()


def verifier_reponse(reponse_utilisateur, reponse_correcte):
    """
    Vérifie si la réponse de l'utilisateur est correcte
    
    Args:
        reponse_utilisateur (int): L'index de la réponse choisie par l'utilisateur
        reponse_correcte (int): L'index de la bonne réponse
    
    Returns:
        bool: True si la réponse est correcte, False sinon
    """
    return reponse_utilisateur == reponse_correcte


def obtenir_reponse_utilisateur(nombre_choix):
    """
    Demande à l'utilisateur de sélectionner une réponse et valide l'entrée
    
    Args:
        nombre_choix (int): Nombre de choix disponibles
    
    Returns:
        int: L'index de la réponse choisie (0-based)
    """
    while True:
        try:
            reponse = input(f"Votre réponse (1-{nombre_choix}): ")
            reponse_num = int(reponse)
            
            if 1 <= reponse_num <= nombre_choix:
                return reponse_num - 1  # Convertir en index 0-based
            else:
                print(f"❌ Veuillez entrer un nombre entre 1 et {nombre_choix}")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide")


def compter_points(score_actuel, est_correct):
    """
    Incrémente le score si la réponse est correcte
    
    Args:
        score_actuel (int): Le score actuel
        est_correct (bool): True si la réponse est correcte
    
    Returns:
        int: Le nouveau score
    """
    if est_correct:
        return score_actuel + 1
    return score_actuel


def afficher_resultat_final(score, total_questions):
    """
    Affiche le résultat final du quiz avec le score et le pourcentage
    
    Args:
        score (int): Nombre de réponses correctes
        total_questions (int): Nombre total de questions
    """
    pourcentage = (score / total_questions) * 100
    
    print(f"\n{'='*60}")
    print("RÉSULTATS FINAUX")
    print(f"{'='*60}")
    print(f"\n✅ Réponses correctes: {score}/{total_questions}")
    print(f"📊 Pourcentage: {pourcentage:.1f}%")
    
    # Évaluation selon le pourcentage
    if pourcentage >= 90:
        print("🏆 Excellent ! Vous êtes un véritable cinéphile !")
    elif pourcentage >= 70:
        print("👍 Très bien ! Vous connaissez bien le 7ème art.")
    elif pourcentage >= 50:
        print("📚 Pas mal, mais il y a encore des films à découvrir !")
    else:
        print("💪 Continuez à regarder des films, vous progresserez !")
    
    print(f"{'='*60}\n")


def lancer_quiz():
    """
    Fonction principale qui lance le quiz sur le cinéma
    """
    # Structure de données contenant les questions sur le cinéma
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
        },
        {
            "question": "Dans quel film d'animation Pixar trouve-t-on les personnages Woody et Buzz l'Éclair ?",
            "choix": ["Monstres & Cie", "Cars", "Toy Story", "Vice-Versa"],
            "reponse_correcte": 2
        },
        {
            "question": "Quel réalisateur est connu pour les films 'Inception' et 'The Dark Knight' ?",
            "choix": ["Quentin Tarantino", "Christopher Nolan", "Denis Villeneuve", "Ridley Scott"],
            "reponse_correcte": 1
        },
        {
            "question": "Dans 'Le Seigneur des Anneaux', quel est le nom de l'anneau unique ?",
            "choix": [
                "L'Anneau de Pouvoir",
                "L'Anneau Unique",
                "L'Anneau de Sauron",
                "L'Anneau Maudit"
            ],
            "reponse_correcte": 1
        },
        {
            "question": "Quel acteur français a joué dans 'Intouchables' aux côtés d'Omar Sy ?",
            "choix": ["Gérard Depardieu", "Jean Reno", "François Cluzet", "Vincent Cassel"],
            "reponse_correcte": 2
        },
        {
            "question": "Quel est le genre du film 'Shining' de Stanley Kubrick ?",
            "choix": ["Comédie", "Science-fiction", "Horreur", "Thriller romantique"],
            "reponse_correcte": 2
        }
    ]
    
    # Affichage de l'introduction
    print("\n" + "="*60)
    print("🎬 BIENVENUE AU QUIZ DE CINÉMA 🍿")
    print("="*60)
    print(f"\nVous allez répondre à {len(questions)} questions.")
    print("Testez vos connaissances sur les films, acteurs et réalisateurs !")
    print("\nBonne chance ! 🌟\n")
    input("Appuyez sur Entrée pour commencer...")
    
    score = 0
    
    # Boucle sur chaque question
    for i, q in enumerate(questions, 1):
        afficher_question(q["question"], q["choix"], i)
        
        reponse_utilisateur = obtenir_reponse_utilisateur(len(q["choix"]))
        
        est_correct = verifier_reponse(reponse_utilisateur, q["reponse_correcte"])
        
        if est_correct:
            print("✅ Correct ! Bravo !")
            score = compter_points(score, True)
        else:
            reponse_correcte_texte = q["choix"][q["reponse_correcte"]]
            print(f"❌ Incorrect. La bonne réponse était: {reponse_correcte_texte}")
            score = compter_points(score, False)
    
    # Affichage des résultats finaux
    afficher_resultat_final(score, len(questions))


if __name__ == "__main__":
    lancer_quiz()
