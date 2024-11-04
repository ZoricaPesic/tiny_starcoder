import random
import time


def generate_values():
    while True:
        motion = random.choice([True, False])
        yield motion


def run_dpir_simulator(delay, callback, stop_event, settings,publish_event,alarm):
    for m in generate_values():
        time.sleep(delay)
        callback(m, settings,publish_event,alarm)
        if stop_event.is_set():
            break
