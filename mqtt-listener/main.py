from listener import MqttListener
from PySide6 import QtCore, QtWidgets, QtGui
import sys

UPDATE_TOPIC = "andrew/zoom"


def get_background_color(meeting, video_muted, audio_muted):
    if not meeting:
        return "black"
    elif video_muted and audio_muted:
        return "green"
    elif audio_muted:
        return "yellow"

    return "red"


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor("white"))

    label = QtWidgets.QLabel("<font color=red size=40>Hello World!</font>")
    label.setPalette(palette)
    label.setGeometry(0, 0, 300, 300)
    label.setAlignment(QtCore.Qt.AlignCenter)
    label.show()


    def message_callback(message):
        zoom = message["zoom"]
        meeting = message["meeting"]
        video_muted = message["video"] == "muted"
        audio_muted = message["audio"] == "muted"

        color = get_background_color(meeting, video_muted, audio_muted)
        palette.setColor(QtGui.QPalette.Window, color)

        text_color = "black"
        if color == "black":
            text = "offline"
            text_color = "white"
        elif color == "green":
            text = "in a meeting"
        elif color == "yellow":
            text = "video on - muted"
        else:
            text = "audio on - shhhh"
        label.setText(f"<font color='{text_color}' size=40>{text}</font>")
        label.setPalette(palette)


    listener = MqttListener(UPDATE_TOPIC, message_callback)
    listener.connect()

    sys.exit(app.exec())
