from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout

from .controls.controls import Controls
from .list.playlist import Playlist
from .video.player import Player
from iptv.event_bus import event_bus


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Neo IPTV")

        event_bus.playlist_toggle.connect(self.toggle_playlist)
        event_bus.fullscreen_toggle.connect(self.toggle_fullscreen)

        # Create instances
        self.video_player = Player()
        self.controls = Controls()
        self.playlist = Playlist()

        # Center the window on the screen
        self.center_window()

        # Setup the interface (UI)
        self.setup_ui()

    def center_window(self):
        # Resize window
        self.resize(800, 600)

        # Get the screen's available geometry (size)
        screen_geometry = self.screen().availableGeometry()

        # Calculate the center position based on the screen size and window size
        center_x = (screen_geometry.width() - self.width()) // 2
        center_y = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center of the screen
        self.move(center_x, center_y)

    def setup_ui(self):
        # Create a central widget
        window = QWidget(self)
        self.setCentralWidget(window)

        # Main layout for the window
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        video_player_layout = QVBoxLayout()
        video_player_layout.setContentsMargins(0, 0, 0, 15)

        # Add the video player and controls to the video player layout
        video_player_layout.addWidget(self.video_player, stretch=1)
        video_player_layout.addWidget(self.controls)

        # Add the video player layout and playlist to the main layout
        main_layout.addLayout(video_player_layout, stretch=85)
        main_layout.addWidget(self.playlist)

        # Set the main layout for the window
        window.setLayout(main_layout)

    def toggle_fullscreen(self):
        """ Toggle the fullscreen mode of the window. """
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def toggle_playlist(self):
        """ Emit the event to toggle the visibility of the playlist. """
        self.playlist.setVisible(not self.playlist.isVisible())
        self.layout().update()
