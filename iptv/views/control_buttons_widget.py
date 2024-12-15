from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy


class ControlButtonsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout (vertical alignment)
        self.main_layout = QVBoxLayout(self)

        # Spacer item to push buttons to the bottom
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.main_layout.addItem(self.spacer)

        # Horizontal layout for the buttons
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center buttons in the layout

        # Control buttons
        self.play_button = QPushButton(self)
        self.prev_button = QPushButton(self)
        self.next_button = QPushButton(self)

        # Add icons to the buttons
        self.prev_button.setIcon(QIcon.fromTheme("media-seek-backward"))  # Icon for Previous
        self.play_button.setIcon(QIcon.fromTheme("media-playback-start"))  # Icon for Play
        self.next_button.setIcon(QIcon.fromTheme("media-seek-forward"))  # Icon for Next

        # Add tooltips to buttons
        self.play_button.setToolTip("Play the video")  # Tooltip for play button
        self.prev_button.setToolTip("Go to previous video")  # Tooltip for previous button
        self.next_button.setToolTip("Go to next video")

        # Set icon size (optional)
        self.play_button.setIconSize(QSize(30, 30))  # Smaller icons
        self.prev_button.setIconSize(QSize(30, 30))  # Smaller icons
        self.next_button.setIconSize(QSize(30, 30))  # Smaller icons

        # Adjust the button size to a more suitable size
        self.play_button.setFixedSize(60, 60)  # Smaller button size
        self.prev_button.setFixedSize(60, 60)  # Smaller button size
        self.next_button.setFixedSize(60, 60)  # Smaller button size

        # Add buttons to the horizontal layout
        self.layout.addWidget(self.prev_button)
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.next_button)

        # Add the horizontal layout to the main layout
        self.main_layout.addLayout(self.layout)

    def connect_buttons(self, play_func, prev_func, next_func):
        # Connect buttons to their corresponding functions
        self.play_button.clicked.connect(play_func)
        self.prev_button.clicked.connect(prev_func)
        self.next_button.clicked.connect(next_func)
