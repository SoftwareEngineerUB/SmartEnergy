import json

from flask import Flask

from app.mqtt.broker import Broker
from app.mqtt.device_scheduler import DeviceScheduler
from app.mqtt.client import Client

MQTT_CONFIG_PATH = "./app/mqtt/mqtt_config.json"


class MqttHub:
    """A class that contains most of mqtt-related initialization and runtime management\n
        NOTE: the code uses two mqtt modules: flask-mqtt and paho-mqtt;
                both of them can publish and subscribe;\
                flask-mqtt is associated with the flask webserver,\ 
                while the other clients are independent;\
                it remains to be seen whether the current architecture will change or not"""

    handle = None

    @staticmethod
    def load_config(path):
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def update_config(path, new_config):
        with open(path, "w+") as f:
            json.dump(new_config, f)

    def __init__(self, app: Flask, config_path):
        self.config_path = config_path
        self.config = MqttHub.load_config(config_path)

        # partially adapted from https://github.com/raresito/SmartBed-RESTApi-example
        app.config['MQTT_BROKER_URL'] = self.config["broker_addr"]
        app.config['MQTT_BROKER_PORT'] = self.config["broker_port"]  # default port for non-tls connection
        app.config['MQTT_USERNAME'] = self.config[
            "mqtt_username"]  # set the username here if you need authentication for the broker
        app.config['MQTT_PASSWORD'] = self.config[
            "mqtt_pass"]  # set the password here if the broker demands authentication
        app.config['MQTT_KEEPALIVE'] = self.config[
            "mqtt_keepalive"]  # set the time interval for sending a ping to the broker to 5 seconds
        app.config['MQTT_TLS_ENABLED'] = self.config["tls_enabled"]  # set TLS to disabled for testing purposes

        self.broker = Broker(self.config)
        self.scheduler = None  # later

        self.app = app

        self.clients = {}

    def create_client(self, name) -> Client:
        self.clients.update({name: Client(name)})
        return self.clients[name]

    def initialize_scheduler(self):
        self.scheduler = DeviceScheduler(self.app, self.config)


def initiateMqtt(app):
    MqttHub.handle = MqttHub(app, MQTT_CONFIG_PATH)
    return MqttHub.handle
