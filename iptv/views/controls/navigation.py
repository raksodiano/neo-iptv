from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

from iptv.event_bus import event_bus
from iptv.models.channel_manager import ChannelManager


class Navigation(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Navigation buttons (Back and Next)
        self.back_button = QPushButton()
        self.next_button = QPushButton()

        # Add icons to the buttons
        self.back_button.setIcon(QIcon.fromTheme("media-seek-backward"))
        self.next_button.setIcon(QIcon.fromTheme("media-seek-forward"))

        # Add tooltips to buttons
        self.back_button.setToolTip("Go to previous channel")
        self.next_button.setToolTip("Go to next channel")

        # Connect buttons to their respective functions
        self.back_button.clicked.connect(self.go_to_previous_channel)
        self.next_button.clicked.connect(self.go_to_next_channel)

        layout.addWidget(self.back_button)
        layout.addWidget(self.next_button)

        self.setLayout(layout)

    def go_to_previous_channel(self):
        """ Navigate to the previous channel """
        previous_channel = ChannelManager.get_instance().get_previous_channel()
        if previous_channel:
            event_bus.channel_url_changed.emit(previous_channel.url)

    def go_to_next_channel(self):
        """ Navigate to the next channel """
        next_channel = ChannelManager.get_instance().get_next_channel()
        if next_channel:
            event_bus.channel_url_changed.emit(next_channel.url)
