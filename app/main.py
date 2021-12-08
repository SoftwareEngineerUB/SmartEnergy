from flask import Flask
from flask_migrate import Migrate

from app.models.db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'

migrate = Migrate(app, db)

db.init_app(app)
migrate.init_app(app, db)


@app.route('/')
def index_page():
    return "Hello world"
