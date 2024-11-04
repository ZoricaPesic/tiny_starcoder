import time

def run_db_simulator(delay, db_callback, stop_event, settings, publish_event, alarm, clock,lock):
    turned_on=alarm.turned_on
    clock_on=clock.is_on
    while True:
        if not turned_on==alarm.turned_on:

            with lock:
                turned_on = alarm.turned_on
            if turned_on:
                db_callback(True,settings,publish_event)
            elif not turned_on:
                db_callback(False, settings, publish_event)
        if not clock_on==clock.is_on:
            with lock:
                clock_on = clock.is_on
            if clock.is_on and settings["name"]=="BB":
                db_callback(True, settings, publish_event)
            elif settings["name"]=="BB" and not clock.is_on:
                db_callback(False, settings, publish_event)

        time.sleep(0.1)

        if stop_event.is_set():
            break

