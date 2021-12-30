from flask import Flask

from flask_mqtt import Mqtt
from flask_socketio import SocketIO

import time
from threading import Thread

# partially adapted from https://github.com/raresito/SmartBed-RESTApi-example

# NOTE: MQTT broker needs to be started separately
# instantiating Flask (HTTP) server, MQTT client (can both publish and subscribe)

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
)

# Setup connection to mqtt broker
app.config['MQTT_BROKER_URL'] = 'localhost'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

mqtt = Mqtt(app)
socketio = SocketIO(app)

@app.route('/')
def indexPage():

    return 'Hello World!'

# Start background thread that publishes mqtt messages
mqtt_publisher_thread = None
def init_mqtt_demo():

    mqtt_publisher_thread = Thread(target = mqtt_demo_publisher, daemon = True)
    mqtt_publisher_thread.start()

def mqtt_demo_publisher():

    _cnt = 0
    while True:
        
        mqtt.publish("python/mqtt/demo", f"published demo message {_cnt}".encode())

        _cnt += 1
        time.sleep(3)

if __name__ == '__main__':

    init_mqtt_demo()
    socketio.run(app, host='localhost', port=5555, use_reloader=False, debug=True)
