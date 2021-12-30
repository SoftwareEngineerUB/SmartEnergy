from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO

from app.models.db import db

# Instantiate Flask app
from app.mqtt.mqtt_hub import init_mqtt

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(SECRET_KEY='dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'

# Index page
@app.route('/')
def indexPage():
    return 'Hello World!'

# Initiate server
def initiateServer():
    # Migrate database
    migrate = Migrate(app, db)

    # Initiate database
    db.init_app(app)
    db.create_all(app=app)
    migrate.init_app(app, db)

    # Initiate mqtt
    mqtt = init_mqtt(app)

    # Initiate socket IO app - flask
    socketio = SocketIO(app)
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)
