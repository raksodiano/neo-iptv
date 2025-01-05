from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

from iptv.event_bus import event_bus


class ToggleButtons(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Buttons for controlling the video player (Show/Hide Playlist and Toggle Fullscreen)
        self.toggle_playlist_button = QPushButton()
        self.fullscreen_button = QPushButton()

        # Add icons to the buttons
        self.toggle_playlist_button.setIcon(QIcon.fromTheme("folder-open"))
        self.fullscreen_button.setIcon(QIcon.fromTheme("view-fullscreen"))

        # Add tooltips to buttons
        self.toggle_playlist_button.setToolTip("Show/Hide Playlist")
        self.fullscreen_button.setToolTip("Toggle Fullscreen")

        # Connect buttons to respective functions
        self.toggle_playlist_button.clicked.connect(self.toggle_playlist)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        layout.addWidget(self.toggle_playlist_button)
        layout.addWidget(self.fullscreen_button)

        self.setLayout(layout)

    def toggle_playlist(self):
        """ Emit the event to toggle the visibility of the playlist. """
        event_bus.emit_playlist_toggle()

        # Toggle the icon of the playlist button
        current_icon = "folder-open" if self.toggle_playlist_button.icon().name() == "folder-new" else "folder-new"
        self.toggle_playlist_button.setIcon(QIcon.fromTheme(current_icon))

    def toggle_fullscreen(self):
        """ Toggle the fullscreen mode of the player. """
        event_bus.emit_fullscreen_toggle()

        current_icon = "view-restore" if self.fullscreen_button.icon().name() == "view-fullscreen" else "view-fullscreen"
        self.fullscreen_button.setIcon(QIcon.fromTheme(current_icon))
