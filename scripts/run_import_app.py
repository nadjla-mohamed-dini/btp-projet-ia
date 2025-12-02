from app import app
print('App imported OK')
print('Config:', app.config.get('SQLALCHEMY_DATABASE_URI'))
