import time
import random
from itertools import cycle


def run_ds_simulator(delay, callback, stop_event, settings,publish_event,alarm,lock):
    for o in cycle([True, False]):
        if o:
            if not alarm.active:
                if delay>5:
                    with lock:
                        time.sleep(5)
                        alarm.turnOnOff(True,settings["name"],"Door opened for more than 5 seconds")
                        time.sleep(delay-5)
                        alarm.turnOnOff(False,settings["name"],"Door closed")
            else:
                alarm.turnOnOff(True,settings["name"],"Door opened")
                time.sleep(delay)

        else:
            time.sleep(delay)
        callback(o, settings,publish_event)

        if stop_event.is_set():
            break
