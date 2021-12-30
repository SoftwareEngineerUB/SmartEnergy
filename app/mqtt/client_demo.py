from paho.mqtt import client as mqtt_client

from random import randint

# NOTE: MQTT broker needs to be started separately
# instantiating just a MQTT client (can both publish and subscribe)

BROKER_ADDR = ('localhost', 1883)  # default (mosquitto) mqtt broker port used
TOPIC = "python/mqtt/demo"

CLIENT_ID = f"client_{randint(0, 10000)}"


def connect():
    def _on_connect(client, userdata, flags, rc):

        if rc == 0:
            print(f"connection established: status {rc}")
        else:
            print(f"connection failed: {rc}")

    client = mqtt_client.Client(CLIENT_ID)
    client.on_connect = _on_connect
    client.connect(*BROKER_ADDR)

    return client


def listen_for_messages(client: mqtt_client.Client, topic=TOPIC):
    def _on_message(client, userdata, message: mqtt_client.MQTTMessage):
        print(f"message from topic [{topic}] received: {message.payload.decode()}")

    client.on_message = _on_message
    client.subscribe(topic=topic)

    try:
        client.loop_forever()

    except KeyboardInterrupt:

        print("\nclient unsubscribed")
        client.unsubscribe(topic=topic)


if __name__ == "__main__":
    client = connect()
    listen_for_messages(client)
