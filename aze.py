from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'feelflix.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute('''CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            favorite_quote TEXT,
            favorite_actor TEXT,
            favorite_director TEXT,
            favorite_movie TEXT,
            favorite_series TEXT
        )''')
        
        c.execute('''CREATE TABLE movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            mood TEXT NOT NULL,
            description TEXT,
            rating REAL,
            image_url TEXT
        )''')
        
        c.execute('''CREATE TABLE quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT
        )''')
        
        c.execute('''CREATE TABLE quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            FOREIGN KEY(quiz_id) REFERENCES quizzes(id)
        )''')
        
        c.execute('''CREATE TABLE playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        
        conn.commit()
        conn.close()
        print("✓ Base de données créée")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        conn = get_db_connection()
        conn.execute('''INSERT INTO users (username, email) VALUES (?, ?)''',
                    (data.get('username'), data.get('email')))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Utilisateur créé'})
    except sqlite3.IntegrityError:
        return jsonify({'status': 'error', 'message': 'Utilisateur existe déjà'}), 400

@app.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    return jsonify({'status': 'error'}), 404

@app.route('/api/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''UPDATE users SET 
        favorite_quote = ?, 
        favorite_actor = ?, 
        favorite_director = ?, 
        favorite_movie = ?,
        favorite_series = ? 
        WHERE id = ?''',
        (data.get('favorite_quote'), data.get('favorite_actor'), 
         data.get('favorite_director'), data.get('favorite_movie'),
         data.get('favorite_series'), user_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/api/movies')
def get_movies():
    mood = request.args.get('mood')
    conn = get_db_connection()
    if mood:
        movies = conn.execute('SELECT * FROM movies WHERE mood = ?', (mood,)).fetchall()
    else:
        movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return jsonify([dict(movie) for movie in movies])

if __name__ == '__main__':
    init_db()
    print("🎬 Feelflix démarre sur http://localhost:5000")
    app.run(debug=True, port=5000)
