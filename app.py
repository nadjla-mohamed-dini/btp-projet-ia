from flask import Flask, jsonify, render_template
from models import db
from config import get_config
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(get_config())
db.init_app(app)


@app.route('/')
def home():
    return jsonify({"message": "Bienvenue sur Feelflix - Application Flask avec PostgreSQL"})


@app.route('/mood')
def mood():
    return render_template('mood.html')


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
