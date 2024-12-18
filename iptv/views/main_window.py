from PyQt6.QtCore import QTimer, QEvent
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSizePolicy
from iptv.logic.video_control import VideoControl
from iptv.logic.volume_control import VolumeControl

from iptv.views.control_buttons_widget import ControlButtonsWidget
from iptv.views.video_player_widget import VideoPlayerWidget
from iptv.views.playlist_widget import PlaylistWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Neo IPTV")

        # Center the window on the screen
        self.center_window()

        # Initialize the Control class to manage the logic
        self.video_control = VideoControl()
        self.volume_control = VolumeControl(self.video_control)

        # Set up UI components
        self.setup_ui()

        # Initialize timer to hide buttons after 10 seconds
        self.hide_widgets_timer = QTimer(self)
        self.hide_widgets_timer.timeout.connect(self.hide_widgets)
        self.buttons_visible = True

        # Initial state of buttons
        self.control_buttons_widget.setVisible(self.buttons_visible)

    def center_window(self):
        # Get the screen's available geometry (size)
        screen_geometry = self.screen().availableGeometry()

        # Calculate the center position based on the screen size and window size
        center_x = (screen_geometry.width() - self.width()) // 2
        center_y = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center of the screen
        self.move(center_x, center_y)

    def setup_ui(self):
        # Central widget container
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Get the screen's available geometry
        screen_geometry = self.screen().availableGeometry()

        print(screen_geometry)

        # Set the initial window size to a reasonable fraction of the screen size, for example, 80% of the screen
        initial_width = int(screen_geometry.width() * 0.8)
        initial_height = int(screen_geometry.height() * 0.8)

        # Ensure the window is not larger than the available screen size
        self.setGeometry(100, 100, initial_width, initial_height)

        layout = QHBoxLayout(self.central_widget)

        video_layout = QVBoxLayout()
        self.video_widget = VideoPlayerWidget(self)
        video_layout.addWidget(self.video_widget)

        # Control buttons widget
        self.control_buttons_widget = ControlButtonsWidget(self)
        self.control_buttons_widget.setFixedHeight(80)
        video_layout.addWidget(self.control_buttons_widget)

        # Playlist widget
        self.playlist_widget = PlaylistWidget(self, self)
        self.playlist_widget.setFixedWidth(400)

        # Add the video layout to the main layout
        layout.addLayout(video_layout)
        layout.addWidget(self.playlist_widget)

        # Status label initialization
        self.status_label = QLabel(self)
        self.status_label.setText("Ready to play video.")
        video_layout.addWidget(self.status_label)  # Add it to the layout

        # Explicitly assign layout to the central widget
        self.central_widget.setLayout(layout)

        # Connect buttons to their respective methods
        self.control_buttons_widget.connect_buttons(
            self.play_iptv_channel,
            self.play_previous_channel,
            self.play_next_channel,
            self.adjust_volume
        )

        # Ensure the video widget takes up the maximum available space
        self.video_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Connect mouse movement events to detect mouse position
        self.central_widget.setMouseTracking(True)
        self.central_widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseMove:
            # Get position of the mouse relative to the window
            mouse_pos = event.pos()
            screen_width = self.width()
            screen_height = self.height()

            # Define the threshold for each specific area
            threshold_bottom = screen_height * 0.8  # Bottom 20% of the window
            threshold_right = screen_width * 0.6  # 70% of the window width (for PlaylistWidget)

            # Show the PlaylistWidget when the mouse is in the right 30% of the screen
            if mouse_pos.x() > threshold_right:
                if not self.playlist_widget.isVisible():
                    self.playlist_widget.setVisible(True)

            # Show the controls buttons when the mouse is in the bottom 20% of the screen
            if mouse_pos.y() > threshold_bottom:
                if not self.control_buttons_widget.isVisible():
                    self.control_buttons_widget.setVisible(True)
                    self.hide_widgets_timer.start(15000)  # Restart the timer when it is shown
            else:
                if self.control_buttons_widget.isVisible():
                    self.control_buttons_widget.setVisible(False)
                    self.hide_widgets_timer.stop()  # Stop the timer if the mouse leaves the area

            # If the mouse is not in the area for the PlaylistWidget, hide it
            if mouse_pos.x() < threshold_right:
                if self.playlist_widget.isVisible():
                    self.playlist_widget.setVisible(False)

        return super().eventFilter(obj, event)

    def hide_widgets(self):
        # Hide the buttons
        self.buttons_visible = False
        self.control_buttons_widget.setVisible(False)
        self.playlist_widget.setVisible(False)

    def play_channel(self, channel):
        """Get the IPTV channel from the list and play it"""
        if self.video_control.channels:
            self.status_label.setText(f"Channel: {channel['name']}")
            self.video_control.play_iptv_channel(channel, self.video_widget)

    def play_iptv_channel(self):
        """Get the IPTV channel from the list and play it"""
        if self.video_control.channels:
            channel = self.video_control.channels[0]
            self.status_label.setText(f"Channel: {channel['name']}")
            self.video_control.play_iptv_channel(channel, self.video_widget)

    def play_previous_channel(self):
        # Use the VideoControl class to play the previous IPTV channel
        previous_channel = self.video_control.play_previous_channel(self.video_widget)
        if previous_channel:
            self.status_label.setText(f"Channel: {previous_channel['name']}")

    def play_next_channel(self):
        # Use the VideoControl class to play the next IPTV channel
        next_channel = self.video_control.play_next_channel(self.video_widget)
        if next_channel:
            self.status_label.setText(f"Channel: {next_channel['name']}")

    def adjust_volume(self, value):
        """Adjust the volume using the VolumeControl."""
        self.volume_control.set_volume(value)
        self.control_buttons_widget.update_volume_label(value)
