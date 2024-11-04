import time
import random



def run_dms_simulator(delay, callback, stop_event, settings, publish_event,pin):
    while True:
        if len(pin)>0:
            callback(pin[0], settings, publish_event)
            pin=[]

            time.sleep(1)

            if stop_event.is_set():
                break
