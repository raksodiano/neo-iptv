from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QSlider, QPushButton, QHBoxLayout, QSizePolicy
from iptv.event_bus import event_bus


class Volume(QWidget):
    def __init__(self):
        super().__init__()

        self.last_volume = None

        # Main layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Mute button
        self.mute_button = QPushButton()
        self.mute_button.setIcon(QIcon.fromTheme("audio-volume-high"))
        self.mute_button.setToolTip("Mute")
        self.mute_button.clicked.connect(self.toggle_mute)

        layout.addWidget(self.mute_button)

        # Volume slider
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)  # Default volume is 100

        self.volume_slider.valueChanged.connect(self.change_volume)

        layout.addWidget(self.volume_slider)

        self.setLayout(layout)

    def change_volume(self, value):
        """ Emit signal when volume changes. """
        if value != 0:
            self.last_volume = value

        event_bus.emit_volume(value)

    def toggle_mute(self):
        """ Emit signal when mute button is clicked. """
        if self.volume_slider.value() == 0:
            self.volume_slider.setValue(self.last_volume if self.last_volume else 100)
            event_bus.emit_mute(False)
        else:
            # Mute: Set volume to 0
            self.volume_slider.setValue(0)
            event_bus.emit_mute(True)

            # Update mute button icon
        muted = self.volume_slider.value() == 0
        self.mute_button.setIcon(
            QIcon.fromTheme("audio-volume-muted" if muted else "audio-volume-high")
        )
