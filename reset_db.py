from app import app, db, Movie, Mood

def reset_movies():
    with app.app_context():
        Movie.query.delete()
        db.session.commit()
        print("Tous les films ont été supprimés ✅")

def reset_moods():
    with app.app_context():
        Mood.query.delete()
        db.session.commit()

        moods = ["triste", "drôle", "heureux", "amoureux", "énervé", "peur"]
        for m in moods:
            mood = Mood(user_id=1, mood_type=m)
            db.session.add(mood)
        db.session.commit()
        print("Moods recréés ✅")

if __name__ == "__main__":
    reset_movies()
    reset_moods()
    print("Base de données réinitialisée avec succès ! 🎉")