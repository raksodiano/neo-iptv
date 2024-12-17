from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QSlider, QLabel


class ControlButtonsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout (vertical alignment)
        self.main_layout = QVBoxLayout(self)

        # Horizontal layout for buttons and volume control
        self.control_layout = QHBoxLayout()

        # Horizontal layout for the buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center buttons

        # Control buttons
        self.play_button = QPushButton(self)
        self.prev_button = QPushButton(self)
        self.next_button = QPushButton(self)

        # Add icons to the buttons
        self.prev_button.setIcon(QIcon.fromTheme("media-seek-backward"))  # Icon for Previous
        self.play_button.setIcon(QIcon.fromTheme("media-playback-start"))  # Icon for Play
        self.next_button.setIcon(QIcon.fromTheme("media-seek-forward"))  # Icon for Next

        # Add tooltips to buttons
        self.play_button.setToolTip("Play the channel")
        self.prev_button.setToolTip("Go to previous channel")
        self.next_button.setToolTip("Go to next channel")

        # Set icon size (optional)
        self.play_button.setIconSize(QSize(15, 15))
        self.prev_button.setIconSize(QSize(15, 15))
        self.next_button.setIconSize(QSize(15, 15))

        # Adjust the button size to a more suitable size
        self.play_button.setFixedSize(40, 40)
        self.prev_button.setFixedSize(40, 40)
        self.next_button.setFixedSize(40, 40)

        # Add buttons to the button layout
        self.button_layout.addWidget(self.prev_button)
        self.button_layout.addWidget(self.play_button)
        self.button_layout.addWidget(self.next_button)

        # Volume slider layout
        self.volume_layout = QHBoxLayout()
        self.volume_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Volume slider
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)  # Minimum volume
        self.volume_slider.setMaximum(100)  # Maximum volume
        self.volume_slider.setValue(90)  # Default volume
        self.volume_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.volume_slider.setTickInterval(10)
        self.volume_slider.setToolTip("Adjust volume")
        self.volume_slider.setFixedWidth(150)  # Adjust slider width

        # Volume label
        self.volume_label = QLabel(f"{self.volume_slider.value()}%")  # Initialize with the current slider value
        self.volume_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.volume_label.setFixedWidth(40)  # Optional: Set a fixed width for alignment

        # Add slider and label to the volume layout
        self.volume_layout.addWidget(self.volume_slider)
        self.volume_layout.addWidget(self.volume_label)

        # Spacer item to separate buttons and volume control
        self.control_layout.addLayout(self.button_layout)  # Add buttons in the center
        self.control_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.control_layout.addLayout(self.volume_layout)  # Add volume at the right

        # Add the control layout to the main layout
        self.main_layout.addLayout(self.control_layout)

        # Spacer item to push everything to the bottom
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Connect slider to update volume label
        self.volume_slider.valueChanged.connect(self.update_volume_label)

    def update_volume_label(self, value):
        """Update the volume label when the slider is moved."""
        self.volume_label.setText(f"{value}%")

    def connect_buttons(self, play_func, prev_func, next_func, volume_func):
        """Connect buttons and volume slider to their corresponding functions."""
        self.play_button.clicked.connect(play_func)
        self.prev_button.clicked.connect(prev_func)
        self.next_button.clicked.connect(next_func)
        self.volume_slider.valueChanged.connect(volume_func)
