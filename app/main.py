from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO

from app.models.db import db

# Instantiate Flask app
from app.mqtt.server_demo import init_mqtt

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(SECRET_KEY='dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'

# partially adapted from https://github.com/raresito/SmartBed-RESTApi-example
# Setup connection to mqtt broker
# NOTE: MQTT broker needs to be started separately
# instantiating Flask (HTTP) server, MQTT client (can both publish and subscribe)
app.config['MQTT_BROKER_URL'] = 'localhost'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes


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
    # init_mqtt(app)

    # Initiate socket IO app - flask
    socketio = SocketIO(app)
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)
