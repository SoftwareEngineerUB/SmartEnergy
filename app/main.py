from flask import Flask

# Instantiate Flask app
from app.meter.route import app_meter
from app.mqtt.mqtt_hub import initiateMqtt, MqttHub
from app.util.database import Database


# Initiate server
def initiateFlask():
    # Initiate app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Register blueprints
    app.register_blueprint(app_meter)
    # Initiate database
    Database.initiateDatabase(app)

    # Initiate mqtt
    initiateMqtt(app)

    # Initiate mqtt scheduler
    MqttHub.handle.initialize_scheduler()

    return app
