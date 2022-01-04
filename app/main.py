from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO

from .commands import mock_blueprint
from app.models.db import db

# Instantiate Flask app

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(SECRET_KEY='dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
app.register_blueprint(mock_blueprint)


# Index page
@app.route('/')
def index_page():
    return 'Hello World!'


# Initiate server
def initiate_server():
    # Migrate database
    migrate = Migrate(app, db)

    # Initiate database
    db.init_app(app)
    db.create_all(app=app)
    migrate.init_app(app, db)

    # Initiate mqtt
    # mqtt = init_mqtt(app)

    # Initiate socket IO app - flask
    socketio = SocketIO(app)
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)
