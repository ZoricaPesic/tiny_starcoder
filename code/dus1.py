import time
import random


def generate_values(initial_distance=0):
    current_distance = 10
    decreasing = True

    while True:
        yield current_distance

        if decreasing:
            current_distance -= 1
            if current_distance < 0:
                decreasing = False
                current_distance = 0
        else:
            current_distance += 1
            if current_distance > 10:
                decreasing = True
                current_distance = 10


def run_dus_simulator(delay, callback, stop_event, settings,publish_event):
    for d in generate_values():
        time.sleep(delay)
        callback(d, settings,publish_event)
        if stop_event.is_set():
            break
