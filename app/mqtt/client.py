from random import randint

from paho.mqtt import client as mqtt_client


class Client:
    """Typical mqtt client (can both publish and subscribe!)\n
        It lightly wraps paho-mqtt client, and thus any change on the client is currently done by accessing the self.client attribute"""

    def __init__(self, config, name):
        self.config = config

        self.name = name
        self.id = f"{name}_{randint(0, 0xffffffff)}"

        self.client = mqtt_client.Client(self.id)
