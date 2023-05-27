import threading
import time
from random import randrange
from uuid import uuid4
from producer import proceed_to_deliver

DELIVERY_INTERVAL_SEC = 10
temperature_range = 50
device_event: threading.Event = None

def reset_range(new_range):
    global temperature_range
    temperature_range = new_range

def generator_job():
    global device_event
    while device_event.is_set():
        time.sleep(DELIVERY_INTERVAL_SEC)
        req_id = uuid4().__str__()
        temperature = randrange(temperature_range)
        details = {
            'deliver_to': 'plc_analog',
            'operation': 'push_temperature_value',
            'temperature': temperature,
            'id': req_id
        }
        proceed_to_deliver(req_id, details)
        details['id'] = uuid4().__str__()
        details['deliver_to'] = 'scada_out'
        proceed_to_deliver(details['id'], details)

def start_generator():
    global device_event
    device_event = threading.Event()
    device_event.set()
    threading.Thread(target=lambda: generator_job()).start()

if __name__ == '__main__':
    start_generator()