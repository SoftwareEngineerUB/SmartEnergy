import time
from threading import Thread
import json

from flask import Flask
from flask_mqtt import Mqtt

class FlaskClient:
    """The mqtt client associated with the flask webserver\n
        Its functionality will reside here (currently only a demo publisher function)"""

    @staticmethod
    def mqtt_publisher(mqtt_app: Mqtt):
        """demo method"""

        cnt = 0
        while True:

            mqtt_app.publish("python/mqtt/demo", f"published demo message {cnt}".encode())

            cnt += 1
            time.sleep(3)
    
    def __init__(self, app: Flask, config):
        
        self.config = config

        try:

            self.mqtt_app = Mqtt(app)
            self.mqtt_publisher_thread = Thread(target=FlaskClient.mqtt_publisher, daemon=True, args=(self.mqtt_app,))
            self.mqtt_publisher_thread.start()

        except Exception as err:
            raise Exception(f"could not start flask-mqtt publisher: {err}")
