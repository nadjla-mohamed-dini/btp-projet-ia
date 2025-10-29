# -*- coding: utf-8 -*-
import unittest
from models import db, User
from flask import Flask


class TestUserPasswordHashing(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Configure l'application Flask et la base de données de test"""
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['TESTING'] = True
        
        db.init_app(cls.app)
        with cls.app.app_context():
            db.create_all()
    
    def setUp(self):
        """Crée un contexte d'application pour chaque test"""
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Nettoie après chaque test"""
        db.session.remove()
        self.app_context.pop()
    
    def test_password_is_hashed(self):
        """Vérifie que le mot de passe est bien haché"""
        user = User(username='testuser', email='test@example.com')
        password = 'mon_mot_de_passe_secret'
        user.set_password(password)
        
        # Le mot de passe stocké ne doit pas être égal au mot de passe en clair
        self.assertNotEqual(user.password, password)
        self.assertTrue(len(user.password) > len(password))
    
    def test_password_hash_format(self):
        """Vérifie que le hash a un format valide"""
        user = User(username='testuser2', email='test2@example.com')
        user.set_password('password123')
        
        # Le hash doit être un format valide de werkzeug (scrypt ou pbkdf2)
        self.assertTrue(
            user.password.startswith('scrypt:') or 
            user.password.startswith('pbkdf2:sha256:')
        )
    
    def test_correct_password_verification(self):
        """Vérifie que check_password retourne True avec le bon mot de passe"""
        user = User(username='testuser3', email='test3@example.com')
        password = 'mon_mot_de_passe'
        user.set_password(password)
        
        # Le bon mot de passe doit être validé
        self.assertTrue(user.check_password(password))
    
    def test_incorrect_password_verification(self):
        """Vérifie que check_password retourne False avec un mauvais mot de passe"""
        user = User(username='testuser4', email='test4@example.com')
        user.set_password('mon_mot_de_passe')
        
        # Un mauvais mot de passe doit être rejeté
        self.assertFalse(user.check_password('mauvais_mot_de_passe'))
    
    def test_empty_password_check(self):
        """Vérifie le comportement avec un mot de passe vide"""
        user = User(username='testuser5', email='test5@example.com')
        user.set_password('')
        
        # Doit pouvoir vérifier même avec un mot de passe vide
        self.assertTrue(user.check_password(''))
        self.assertFalse(user.check_password('something'))
    
    def test_case_sensitive_password(self):
        """Vérifie que les mots de passe sont sensibles à la casse"""
        user = User(username='testuser6', email='test6@example.com')
        user.set_password('MonMotDePasse')
        
        # Doit distinguer les majuscules/minuscules
        self.assertTrue(user.check_password('MonMotDePasse'))
        self.assertFalse(user.check_password('monmotdepasse'))
    
    def test_special_characters_in_password(self):
        """Vérifie que les caractères spéciaux sont supportés"""
        user = User(username='testuser7', email='test7@example.com')
        password = 'P@ssw0rd!#$%&*'
        user.set_password(password)
        
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.check_password('P@ssw0rd!#$%&'))


if __name__ == '__main__':
    unittest.main()
