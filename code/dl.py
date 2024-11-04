import time


def run_dl_simulator(delay, dl_callback, stop_event, settings, publish_event, light):
    while True:
        if light.turned_on:
            dl_callback(True,settings,publish_event)
            time.sleep(delay)
            dl_callback(False,settings,publish_event)
            light.turned_on=False

        time.sleep(1)

        if stop_event.is_set():
            break

