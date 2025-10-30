# -*- coding: utf-8 -*-
from flask import Flask
from flask_migrate import Migrate
from models import db
from app import app  # Assure-toi que app.py expose bien "app"

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
