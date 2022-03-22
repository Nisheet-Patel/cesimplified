from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SECRET_KEY'] = "os.getenv('secret_key')"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.jinja_options['extensions'].append('jinja2.ext.loopcontrols')
    app.jinja_options['extensions'].append('jinja2.ext.do')

    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app