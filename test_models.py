import unittest
from datetime import datetime
from models import db, User, Mood, Movie
from flask import Flask


class TestModels(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['TESTING'] = True
        
        db.init_app(cls.app)
        with cls.app.app_context():
            db.create_all()
    
    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.session.query(User).delete()
        db.session.query(Mood).delete()
        db.session.query(Movie).delete()
        db.session.commit()
        
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        self.app_context.pop()
    
    def test_mood_creation(self):
        """Teste la création d'une humeur"""
        mood = Mood(user_id=self.user.id, mood_type='happy')
        db.session.add(mood)
        db.session.commit()
        
        self.assertIsNotNone(mood.id)
        self.assertEqual(mood.mood_type, 'happy')
    
    def test_mood_timestamp(self):
        """Teste que le timestamp de création est défini"""
        mood = Mood(user_id=self.user.id, mood_type='sad')
        db.session.add(mood)
        db.session.commit()
        
        self.assertIsInstance(mood.created_at, datetime)
    
    def test_mood_user_relationship(self):
        """Teste la relation Mood -> User"""
        mood = Mood(user_id=self.user.id, mood_type='excited')
        db.session.add(mood)
        db.session.commit()
        
        retrieved_mood = Mood.query.get(mood.id)
        self.assertEqual(retrieved_mood.user.username, 'testuser')
    
    def test_user_moods_relationship(self):
        """Teste la relation User -> Moods"""
        db.session.add(Mood(user_id=self.user.id, mood_type='happy'))
        db.session.add(Mood(user_id=self.user.id, mood_type='sad'))
        db.session.commit()
        
        retrieved_user = User.query.get(self.user.id)
        self.assertEqual(len(retrieved_user.moods), 2)
    
    def test_movie_creation(self):
        """Teste la création d'un film"""
        mood = Mood(user_id=self.user.id, mood_type='happy')
        db.session.add(mood)
        db.session.commit()
        
        movie = Movie(mood_id=mood.id, title='The Matrix', genre='Sci-Fi', rating=8.7)
        db.session.add(movie)
        db.session.commit()
        
        self.assertIsNotNone(movie.id)
        self.assertEqual(movie.title, 'The Matrix')
        self.assertEqual(movie.rating, 8.7)
    
    def test_movie_optional_fields(self):
        """Teste que description et genre sont optionnels"""
        mood = Mood(user_id=self.user.id, mood_type='happy')
        db.session.add(mood)
        db.session.commit()
        
        movie = Movie(mood_id=mood.id, title='Interstellar')
        db.session.add(movie)
        db.session.commit()
        
        self.assertIsNone(movie.description)
        self.assertIsNone(movie.genre)
    
    def test_movie_mood_relationship(self):
        """Teste la relation Movie -> Mood"""
        mood = Mood(user_id=self.user.id, mood_type='happy')
        db.session.add(mood)
        db.session.commit()
        
        movie = Movie(mood_id=mood.id, title='Inception')
        db.session.add(movie)
        db.session.commit()
        
        retrieved_movie = Movie.query.get(movie.id)
        self.assertEqual(retrieved_movie.mood.mood_type, 'happy')
    
    def test_mood_movies_relationship(self):
        """Teste la relation Mood -> Movies"""
        mood = Mood(user_id=self.user.id, mood_type='happy')
        db.session.add(mood)
        db.session.commit()
        
        db.session.add(Movie(mood_id=mood.id, title='Movie 1'))
        db.session.add(Movie(mood_id=mood.id, title='Movie 2'))
        db.session.commit()
        
        retrieved_mood = Mood.query.get(mood.id)
        self.assertEqual(len(retrieved_mood.movies), 2)
    
    def test_cascade_delete_mood(self):
        """Teste que les films sont supprimés quand l'humeur est supprimée"""
        mood = Mood(user_id=self.user.id, mood_type='happy')
        db.session.add(mood)
        db.session.commit()
        
        db.session.add(Movie(mood_id=mood.id, title='Movie 1'))
        db.session.add(Movie(mood_id=mood.id, title='Movie 2'))
        db.session.commit()
        
        self.assertEqual(Movie.query.count(), 2)
        
        db.session.delete(mood)
        db.session.commit()
        
        self.assertEqual(Movie.query.count(), 0)


if __name__ == '__main__':
    unittest.main()
