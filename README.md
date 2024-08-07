# zoom-lamp

This project provides scipts to push the state of the Zoom client on MacOS to MQTT.  There is also a sample MQTT listener to show the different states.

## Running it

### Initialize the environment

To install dependencies, run `poetry install`.  In the terminals where you will execute python scripts, first run `poetry shell`.

### Sending Zoom state to MQTT

1. If you don't already have an MQTT server, start one using `mqtt-server/run.sh`.  This will start an MQTT server locally running on port 1883.
2. Start the zoom state exporter using something like: `watch -n 5 zoom-status/zoomer.js`.  This script uses JavaScript for Automation (JXA) to read the menus (and thus state) of the Zoom application.  State is written to a text file.
3. Start the Python script to publish the state to MQTT using:  `poetry run python zoom-status/mqtt-send.py`.  State is published to the `home/zoom` topic.

### Running the app to show the state

Run `mqtt-listener/main.py`.  This is a Qt/PySide application that listens to the MQTT topic for zoom state and updates itself accordlingly to show that state.
