import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import paho.mqtt.client as mqtt

STATE_FILE_PATH = os.path.expanduser("~/Desktop")
STATE_FILE = os.path.join(STATE_FILE_PATH, "zoom-state.txt")

UPDATE_TOPIC = "andrew/zoom"

CHECK_INTERVAL_SECS = 5


class ObservedFile(FileSystemEventHandler):
    def __init__(self, filename, change_callback):
        self.filename = filename
        self.change_callback = change_callback
        self.observer = Observer()
        self.observer.schedule(self, os.path.dirname(filename), recursive=True)
        self.observer.start()
        self.on_modified()

    def on_modified(self, event=None):
        if event is not None and event.is_directory:
            return
        if event is None or event.src_path == self.filename:
            with open(self.filename) as f:
                contents = f.read().strip()
                self.change_callback(contents)

    def stop(self):
        self.observer.stop()
        self.observer.join(5)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe(UPDATE_TOPIC)


def on_message(client, userdata, msg):
    pass


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("10.115.18.5", 1883, 60)
    client.loop_start()

    digest = None


    def cb(contents: str):
        client.publish(UPDATE_TOPIC, contents)


    observed = ObservedFile(STATE_FILE, cb)
    try:
        while True:
            time.sleep(1)
    finally:
        observed.stop()
