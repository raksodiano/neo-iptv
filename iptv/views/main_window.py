from PyQt6.QtCore import QTimer, QEvent
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QFileDialog, QSizePolicy
from logic.video_control import VideoControl

from .control_buttons_widget import ControlButtonsWidget
from .video_player_widget import VideoPlayerWidget


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
        self.hide_buttons_timer = QTimer(self)
        self.hide_buttons_timer.timeout.connect(self.hide_buttons)
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

        # Layout for the main window
        layout = QVBoxLayout(self.central_widget)

        # Video display widget (imported from video_player_widget.py)
        self.video_widget = VideoPlayerWidget(self)
        layout.addWidget(self.video_widget)

        # Control buttons widget (imported from control_buttons_widget.py)
        self.control_buttons_widget = ControlButtonsWidget(self)
        layout.addWidget(self.control_buttons_widget)

        # Status label initialization
        self.status_label = QLabel(self)
        self.status_label.setText("Ready to play video.")
        layout.addWidget(self.status_label)  # Add it to the layout

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
        self.central_widget.setMouseTracking(True)
        self.central_widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseMove:
            # Get position of the mouse relative to the window
            mouse_pos = event.pos()
            screen_height = self.height()
            threshold = screen_height * 0.8  # Bottom 20% of the screen
            if mouse_pos.y() > threshold:
                # Show buttons if the mouse is in the bottom 20% of the screen
                if not self.buttons_visible:
                    self.buttons_visible = True
                    self.control_buttons_widget.setVisible(True)
                    self.hide_buttons_timer.start(10000)  # Start the timer for 10 seconds
            else:
                if self.buttons_visible:
                    self.buttons_visible = False
                    self.control_buttons_widget.setVisible(False)
                    self.hide_buttons_timer.stop()  # Stop the timer when the mouse is not in the bottom area
        return super().eventFilter(obj, event)

    def hide_buttons(self):
        # Hide the buttons if the timer expires (after 10 seconds)
        self.buttons_visible = False
        self.control_buttons_widget.setVisible(False)

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
