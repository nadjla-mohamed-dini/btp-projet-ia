# 🎬 Quiz de Cinéma - Documentation

## 📝 Description

Module de quiz interactif en Python sur le thème du cinéma. Testez vos connaissances sur les films, acteurs, réalisateurs et scènes cultes !

## ✨ Fonctionnalités

- **10 questions** variées sur le cinéma (films, acteurs, réalisateurs, genres)
- **Choix multiples** pour chaque question (4 options)
- **Validation automatique** des réponses avec feedback immédiat
- **Calcul du score** en temps réel
- **Résultats détaillés** : score, pourcentage et évaluation qualitative
- **Interface conviviale** avec émojis et mise en forme claire

## 🚀 Utilisation

### Lancer le quiz

```bash
python quiz.py
```

### Comment jouer

1. Le quiz affiche une introduction avec le nombre de questions
2. Pour chaque question :
   - Lisez la question et les choix proposés
   - Entrez le numéro de votre réponse (1, 2, 3 ou 4)
   - Recevez un feedback immédiat (✅ Correct ou ❌ Incorrect)
3. À la fin, consultez vos résultats :
   - Nombre de bonnes réponses
   - Pourcentage de réussite
   - Évaluation qualitative

### Exemple d'interaction

```
============================================================
Question 1
============================================================

Qui a réalisé le film 'Titanic' (1997) ?

  1. Steven Spielberg
  2. James Cameron
  3. Christopher Nolan
  4. Martin Scorsese

Votre réponse (1-4): 2
✅ Correct ! Bravo !
```

## 📊 Système d'évaluation

- **90% et plus** : 🏆 Excellent ! Vous êtes un véritable cinéphile !
- **70% à 89%** : 👍 Très bien ! Vous connaissez bien le 7ème art.
- **50% à 69%** : 📚 Pas mal, mais il y a encore des films à découvrir !
- **Moins de 50%** : 💪 Continuez à regarder des films, vous progresserez !

## 🔧 Fonctions principales

### `afficher_question(question, choix, numero)`
Affiche une question formatée avec ses choix de réponses.

### `obtenir_reponse_utilisateur(nombre_choix)`
Récupère et valide la réponse de l'utilisateur (gestion des erreurs incluse).

### `verifier_reponse(reponse_utilisateur, reponse_correcte)`
Vérifie si la réponse sélectionnée est correcte.

### `compter_points(score_actuel, est_correct)`
Met à jour le score en fonction de la réponse.

### `afficher_resultat_final(score, total_questions)`
Affiche les résultats finaux avec score, pourcentage et évaluation.

### `lancer_quiz()`
Fonction principale qui orchestre l'ensemble du quiz.

## 🎯 Thèmes des questions

- Réalisateurs célèbres
- Acteurs et actrices
- Films cultes et répliques
- Récompenses (Oscars)
- Films d'animation
- Cinéma français et international
- Genres cinématographiques

## 📝 Structure des données

Les questions sont stockées dans une liste de dictionnaires :

```python
questions = [
    {
        "question": "Texte de la question",
        "choix": ["Choix 1", "Choix 2", "Choix 3", "Choix 4"],
        "reponse_correcte": 1  # Index de la bonne réponse (0-based)
    },
    # ...
]
```

## 🛠️ Personnalisation

Pour ajouter vos propres questions, modifiez la liste `questions` dans la fonction `lancer_quiz()` :

1. Ajoutez un nouveau dictionnaire avec les clés : `question`, `choix`, `reponse_correcte`
2. Assurez-vous que `reponse_correcte` correspond à l'index de la bonne réponse (commence à 0)

## 📋 Prérequis

- Python 3.6 ou supérieur
- Aucune bibliothèque externe requise

## 👨‍💻 Auteur

Projet BTP - Module de quiz cinéma

## 📄 Licence

Libre d'utilisation pour un usage éducatif
