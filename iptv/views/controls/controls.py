from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from .navigation import Navigation
from .settings import Settings
from .toggle_buttones import ToggleButtons
from .volume import Volume


class Controls(QWidget):
    def __init__(self):
        super().__init__()

        # Create the main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a container for both navigation and volume control elements
        self.frame = QWidget(self)
        layout.addWidget(self.frame)

        # Create a horizontal layout for navigation and volume
        frame_layout = QHBoxLayout(self.frame)
        frame_layout.setContentsMargins(15, 0, 15, 0)

        # Instantiate the Navigation and Volume controls and add them to the layout
        self.setting = Settings()
        self.toggle_buttons = ToggleButtons()
        self.navigation = Navigation()
        self.volume = Volume()

        # Create a spacer
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Add navigation and volume controls to the horizontal layout (side by side)
        frame_layout.addWidget(self.navigation)
        frame_layout.addWidget(self.toggle_buttons)
        frame_layout.addItem(spacer)
        frame_layout.addWidget(self.volume)
        frame_layout.addWidget(self.setting)

        # Set the layout for the parent widget (Controls)
        self.setLayout(layout)

        # Adjust layout to ensure everything scales correctly
        self.frame.setLayout(frame_layout)
