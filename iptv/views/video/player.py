from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox
from iptv.controllers.player_controller import PlayerController
from mpv import MPV

from iptv.models.channel_manager import ChannelManager


def log_output(level, prefix, message):
    """ Handle logs from MPV. """
    print(f"[{level}] {message}")


class Player(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        self.controller = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a QLabel for displaying video
        self.loading_label = QLabel("Channel content will be displayed here", self)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loading_label)

        # Initialize the MPV player
        self.player = MPV(
            wid=str(int(self.winId())),
            log_handler=log_output,
        )

        # Set the layout for the widget
        self.setLayout(layout)

        channel = ChannelManager.get_instance().current_channel

        # Start the video with the given URL
        if channel is None:
            print("No channels available or the channels are not loaded correctly.")
        else:
            self.start_video(channel.url)

    def start_video(self, url):
        """ Start the video in a separate thread using the controller. """
        self.controller = PlayerController(self.player, url)

        # Connect signals to corresponding methods
        self.controller.playback_started.connect(self.hide_loading_label)
        self.controller.playback_error.connect(self.show_error_message)
        self.controller.playback_status_changed.connect(self.on_playback_status_change)

        self.controller.start()  # Start the background thread for playback

    def on_playback_status_change(self, status):
        """ Hide or show the loading label based on playback status. """
        if status == "playing":
            QTimer.singleShot(0, self.hide_loading_label)
        elif status == "paused" or status == "stopped":
            QTimer.singleShot(0, self.show_loading_label)

    def hide_loading_label(self):
        """ Hide the loading label. """
        self.loading_label.setVisible(False)

    def show_loading_label(self):
        """ Show the loading label. """
        self.loading_label.setVisible(True)

    def show_error_message(self, message):
        """ Show an error message box in case of issues. """
        error_dialog = QMessageBox(self)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.exec()
