from mimetypes import init
import time
from threading import Thread, Condition, Lock
import json

from flask import Flask
from flask_mqtt import Mqtt

from app.models import Data, Device, User
from app.models.db import db

class ScheduleState:
    """Class for representing scheduler internal state"""

    def __init__(self):
        
        self.queue = []
        """FIFO queue that accumulates requests from every module of this app\n
            it is usually populated by ScheduleHandlers or, for example, anomaly detection routines"""

        self.info = {}
        """Dictionary to represent current state"""

        self.queue_lock = Lock()
        self.info_lock = Lock()

class ScheduleHandlers:
    """Collection of all (default) schedule-related handlers\n
        Rules for implementing a handler:\n
        1. every handler must receive as first argument the current state\n
        thats pretty much it :)"""

    @staticmethod
    def alarm(current_state: ScheduleState, 
                seconds, repeats, channel, 
                condition=lambda _: True, 
                content_generator=lambda _: "uninitialized content for alarm"):

        if repeats is None:
            repeats = 1

        rep = 0
        while rep < repeats:

            time.sleep(seconds)

            if condition(current_state) is True:
                current_state.queue.append((ScheduleState.PUBLISH, channel, content_generator(current_state)))
            
            if repeats is not None:
                rep += 1

call = {"alarm": ScheduleHandlers.alarm}
"""Identifier -> Function map"""

class FlaskClient:
    """The mqtt client associated with the flask webserver\n
        It manages the current state of the devices and their scheduling"""

    PUBLISH = "publish"
    EXEC_SYNC = "execs"
    EXEC_BACKGROUND = "execb"

    def scheduler_loop(self, state: ScheduleState):

        is_empty = Condition()
        
        while True:
            
            # NOT busy waiting
            while len(state.queue) == 0:
                is_empty.wait()

            while len(state.queue) > 0:

                r = state.queue.pop(0)

                if r[0] == FlaskClient.PUBLISH:
                    self.mqtt.publish(r[1], r[2])

                elif r[0] == FlaskClient.EXEC_SYNC:
                    call[r[1]](current_state=state, **r[2])

                elif r[1] == FlaskClient.EXEC_BACKGROUND:
                    thr = Thread(target=call[r[1]], daemon=True, args=(state,), kwargs=r[2]) 
                    thr.start()

    def start_scheduler(self):
        """Parses each device settings for each user, calls required handlers\n
            and then starts the (infinite) publisher loop, for each different user"""
        
        with self.app.app_context():
            for user in db.session.query(User).all():

                # for each user in db
                
                initial_state = ScheduleState()
                self.per_user_scheds[user] = Thread(target=self.scheduler_loop, daemon=True, args=(initial_state,))
                
                # check settings
                for device in db.session.query(Device).filter_by(user_id=user.id):
                    if "handlers" in device.settings.keys():

                        for key, val in device.settings["handlers"]:
                            initial_state.info[key] = val
                
                # start scheduler loop
                self.per_user_scheds[user].start()

    def __init__(self, app: Flask, config):

        self.config = config

        try:

            self.app = app
            self.mqtt = Mqtt(app)

            self.per_user_scheds = {}

            self.global_sched_thr = Thread(target=self.start_scheduler, daemon=True)
            self.global_sched_thr.start()

        except Exception as err:
           raise Exception(f"error while executing scheduler-related code: {err}")
