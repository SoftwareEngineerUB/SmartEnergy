from random import randint

from paho.mqtt import client as mqtt_client

class Client:
    """MQTT client serving as a device mqtt endpoint\n
        It lightly wraps paho-mqtt client (raw client referenced with self.client attribute)"""

    def __init__(self, config, name):
        self.config = config

        self.name = name
        self.id = f"{name}_{randint(0, 0xffffffff)}"

        self.client = mqtt_client.Client(self.id)
