import json
import paho.mqtt.client as mqtt
import time


class MqttListener:
    def __init__(self, topic, message_callback):
        self.topic = topic
        self.message_callback = message_callback

    def connect(self):
        client = mqtt.Client()

        def on_connect(client, userdata, flags, rc):
            print("Connected with result code " + str(rc))

            client.subscribe(self.topic)

        def on_message(client, userdata, msg):
            if msg.topic == self.topic and len(msg.payload.strip()) > 0:
                update = json.loads(msg.payload)
                self.message_callback(update)

        client.on_connect = on_connect
        client.on_message = on_message
        client.connect("localhost", 1883, 60)

        client.loop_start()
        self.client = client

    def disconnect(self):
        self.client.disconnect()
        self.client = None


if __name__ == "__main__":
    def message_handler(message):
        print(message)


    listener = MqttListener("home/zoom", message_handler)
    listener.connect()
    while True:
        time.sleep(1)
