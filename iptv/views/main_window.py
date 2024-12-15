from PyQt6.QtCore import QTimer, QEvent
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSizePolicy
from logic.video_control import VideoControl

from .control_buttons_widget import ControlButtonsWidget
from .video_player_widget import VideoPlayerWidget
from .playlist_widget import PlaylistWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Neo IPTV")
        self.setGeometry(100, 100, 800, 600)  # Size of the window

        # Center the window on the screen
        self.center_window()

        # Initialize the VideoControl class to manage the video logic
        self.video_control = VideoControl()

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
        # self.video_widget.setFixedSize(640, 360)
        video_layout.addWidget(self.video_widget)

        # Control buttons widget (imported from control_buttons_widget.py)
        self.control_buttons_widget = ControlButtonsWidget(self)
        # self.control_buttons_widget.setFixedHeight(100)
        video_layout.addWidget(self.control_buttons_widget)

        # Playlist widget (imported from playlist_widget.py)
        self.playlist_widget = PlaylistWidget(self, self)
        # self.playlist_widget.setFixedWidth(int(self.width() * 0.5))
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
            self.play_next_channel
        )

        # Ensure the video widget takes up the maximum available space
        self.video_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Connect mouse movement events to detect mouse position
        # self.central_widget.setMouseTracking(True)
        # self.central_widget.installEventFilter(self)

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
            # if mouse_pos.x() > threshold_right:
            #     if not self.playlist_widget.isVisible():
            #         self.playlist_widget.setVisible(True)

            # Show the control buttons when the mouse is in the bottom 20% of the screen
            if mouse_pos.y() > threshold_bottom:
                if not self.control_buttons_widget.isVisible():
                    self.control_buttons_widget.setVisible(True)
                    self.hide_widgets_timer.start(15000)  # Restart the timer when it is shown
            else:
                if self.control_buttons_widget.isVisible():
                    self.control_buttons_widget.setVisible(False)
                    self.hide_widgets_timer.stop()  # Stop the timer if the mouse leaves the area

            # If the mouse is not in the area for the PlaylistWidget, hide it
            # if mouse_pos.x() < threshold_right:
            #     if self.playlist_widget.isVisible():
            #         self.playlist_widget.setVisible(False)

        return super().eventFilter(obj, event)

    # def resizeEvent(self, event):
    #     """Called when the window is resized"""
    #     new_width = event.size().width()  # Get the new width of the window
    #     new_height = event.size().height()  # Get the new height of the window
    #
    #     # Set the playlist width to 30% of the window width (fixed)
    #     playlist_width = int(new_width * 0.3)  # 30% for the playlist widget
    #     self.playlist_widget.setFixedWidth(playlist_width)  # Set playlist widget width
    #
    #     # Adjust the video layout width to take up the remaining space
    #     video_layout_width = new_width - playlist_width  # Remaining width for the video widget
    #
    #     # Ensure the video widget does not exceed the total width of the window
    #     if video_layout_width > new_width:  # If the calculated width is larger than the window width
    #         video_layout_width = new_width  # Limit the width to the window width
    #
    #     # Ensure that the video widget width is non-negative
    #     if video_layout_width > 0:
    #         self.video_widget.setFixedWidth(video_layout_width)  # Set video widget width
    #     else:
    #         self.video_widget.setFixedWidth(0)  # Prevent setting a negative width
    #
    #     # Set the video widget height to the full height of the window
    #     self.video_widget.setFixedHeight(new_height)  # Keep the full height for the video widget

    def hide_widgets(self):
        # Hide the buttons if the timer expires (after 10 seconds)
        self.buttons_visible = False
        self.control_buttons_widget.setVisible(False)
        # self.playlist_widget.setVisible(False)

    def play_channel(self, channel_url):
        """Get the IPTV channel from the list and play it"""
        if self.video_control.iptv_channels:
            self.status_label.setText(f"Playing IPTV Channel: {channel_url}")
            self.video_control.play_iptv_channel(channel_url, self.video_widget)

    def play_iptv_channel(self):
        """Get the IPTV channel from the list and play it"""
        if self.video_control.iptv_channels:
            # Play the first channel in the list (index 0)
            first_channel_url = self.video_control.iptv_channels[0]
            self.status_label.setText(f"Playing IPTV Channel: {first_channel_url}")
            self.video_control.play_iptv_channel(first_channel_url, self.video_widget)

    def play_previous_channel(self):
        # Use the VideoControl class to play the previous IPTV channel
        previous_channel = self.video_control.play_previous_channel(self.video_widget)
        if previous_channel:
            self.status_label.setText(f"Playing: {previous_channel}")

    def play_next_channel(self):
        # Use the VideoControl class to play the next IPTV channel
        next_channel = self.video_control.play_next_channel(self.video_widget)
        if next_channel:
            self.status_label.setText(f"Playing: {next_channel}")
