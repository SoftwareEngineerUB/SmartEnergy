from flask import Flask
from flask_socketio import SocketIO

# Instantiate Flask app
from app.meter.route import app_meter
from app.mqtt.mqtt_hub import initiateMqtt
from app.util.database import Database


# Initiate server
def initiateFlask():
    # Initiate app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'

    # Register blueprints
    app.register_blueprint(app_meter)

    # Initiate database
    Database.initiateDatabase(app)

    # Initiate mqtt
    initiateMqtt(app)

    # Initiate socket IO app - flask
    socketio = SocketIO(app)
    socketio.run(app, host='localhost', port=5000, use_reloader=True, debug=True)
