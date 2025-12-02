from app import app
from models import db

with app.app_context():
    engine = db.get_engine(app)
    print('Driver:', engine.name)
    print('URL:', str(engine.url))
