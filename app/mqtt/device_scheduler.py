import time
from random import randint
from threading import Thread, Condition, Lock

from flask import Flask
from flask_mqtt import Mqtt

from app.models import Device, User
from app.models.db import db

class ScheduleState:
    """Class for representing scheduler internal state"""

    PUBLISH = "publish"
    EXEC_SYNC = "execs"
    EXEC_BACKGROUND = "execb"

    def __init__(self):
        
        self.queue = []
        """FIFO queue that accumulates requests from every module of this app\n
            it is usually populated by ScheduleHandlers or, for example, anomaly detection routines"""

        self.info = {}
        """Dictionary to represent current state"""

        self.info_lock = Lock()

        self.wakeup = Condition()
        """Variable that, when notified, wakes up the scheduler"""

    def notify(self):
        """Notify wakeup condition"""

        self.wakeup.acquire(True)
        self.wakeup.notify()
        self.wakeup.release()

    def assign_publish(self, channel, content):

        if type(content) == str:
            content = content.encode()

        self.queue.append((ScheduleState.PUBLISH, channel, content))

    def assign_exec_sync(self, to_call, kwargs):

        if type(to_call) != str:
            to_call = to_call.__name__

        self.queue.append((ScheduleState.EXEC_SYNC, to_call, kwargs))

    def assign_exec_background(self, to_call, kwargs):

        if type(to_call) != str:
            to_call = to_call.__name__

        self.queue.append((ScheduleState.EXEC_BACKGROUND, to_call, kwargs))

class ScheduleHandlers:
    """Collection of all (default) schedule-related handlers\n
        Rules for implementing a handler:\n
        1. every handler must receive as first argument the current state\n
        2. for multithreading safety, lock before using info from (the) state object\n
        """

    def global_shutdown(current_state: ScheduleState):

        current_state.assign_publish("global", "<<SHUTDOWN>>")
        current_state.notify()

    def alarm(current_state: ScheduleState, 
                seconds, repeats, channel, 
                condition="always_true", 
                content_generator="default_content"):

        if repeats == -1:
            repeats = 1

        rep = 0
        while rep < repeats:

            time.sleep(seconds)

            if ScheduleHandlers.call[condition](current_state) is True:
                current_state.assign_publish(channel, ScheduleHandlers.call[content_generator](current_state))

            current_state.notify()
            
            if repeats == -1:
                rep += 1

    call = {
            "alarm": alarm,
            "always_true": lambda _: True, 
            "default_content": lambda _: b"uninitialized content",
            "random_notifier": lambda _: f"random message {randint(0, 10000)}"
            }
    """Function dispatcher"""

class DeviceScheduler:
    """The mqtt client associated with the flask webserver\n
        It manages the current state of the devices and their scheduling"""

    def scheduler_loop(self, state: ScheduleState):
        
        while True:
            
            # NOT busy waiting
            while len(state.queue) == 0:

                state.wakeup.acquire(True)  # only because the wait() call needs the current thread to have the lock
                state.wakeup.wait()

            while len(state.queue) > 0:

                r = state.queue.pop(0)

                if r[0] == ScheduleState.PUBLISH:
                    self.mqtt.publish(r[1], r[2])

                elif r[0] == ScheduleState.EXEC_SYNC:
                    ScheduleHandlers.call[r[1]](current_state=state, **r[2])

                elif r[0] == ScheduleState.EXEC_BACKGROUND:
                    thr = Thread(target=ScheduleHandlers.call[r[1]], daemon=True, args=(state,), kwargs=r[2]) 
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

                    settings = device.settings
                    if "handlers" in settings.keys():

                        for fct, kwargs in settings["handlers"].items():
                            initial_state.assign_exec_background(fct, kwargs)

                    # TODO add initial info in initial_state from every device
                
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
