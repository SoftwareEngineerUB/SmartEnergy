import time
from threading import Thread

from flask_mqtt import Mqtt


def init_mqtt(app):
    # Initiate MQTT
    mqtt = Mqtt(app)
    mqtt_publisher_thread = Thread(target=mqtt_publisher, daemon=True, args=(mqtt,))
    mqtt_publisher_thread.start()


def mqtt_publisher(mqtt):
    _cnt = 0
    while True:
        mqtt.publish("python/mqtt/demo", f"published demo message {_cnt}".encode())
        _cnt += 1
        time.sleep(3)
