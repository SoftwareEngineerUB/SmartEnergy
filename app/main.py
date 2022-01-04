from flask import Flask
from flask_socketio import SocketIO

# Instantiate Flask app
from app.mqtt.mqtt_hub import initiateMqtt
from app.util.database import Database

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(SECRET_KEY='dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'


# Index page
@app.route('/')
def index_page():
    return 'Hello World!'


# Initiate server
def initiateFlask():
    # Migrate database
    Database.initiateDatabase(app)

    # Initiate mqtt
    # initiateMqtt(app)

    # Initiate socket IO app - flask
    socketio = SocketIO(app)
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)
