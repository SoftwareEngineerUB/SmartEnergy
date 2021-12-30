from subprocess import Popen
from time import sleep

class Broker:

    START_DELAY = 0.5

    def __init__(self, config):
        
        try:
            self.broker_proc = Popen(["mosquitto", "-p", f"{config['broker_port']}"])
            sleep(Broker.START_DELAY)

        except Exception as err:
            raise Exception(f"could not initialize mqtt broker: {err}")
