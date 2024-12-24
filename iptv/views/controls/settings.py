import asyncio
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from iptv.views.dialogs.setting import SettingsDialog


def show_settings_dialog(self):
    """ Opens the 'Settings' dialog when the button is clicked """
    settings_dialog = SettingsDialog()
    settings_dialog.exec()


class Settings(QWidget):
    """ QWidget with a button that opens the Settings dialog """

    def __init__(self):
        super().__init__()

        # Main layout for the QWidget
        layout = QVBoxLayout()

        # Create a button with an icon that opens the Settings dialog
        self.gear_button = QPushButton()
        self.gear_button.setIcon(QIcon.fromTheme("preferences-system"))
        self.gear_button.setToolTip("Click to open settings menu")
        self.gear_button.clicked.connect(show_settings_dialog)

        # Add the button to the layout
        layout.addWidget(self.gear_button)

        self.setLayout(layout)
        self.setWindowTitle("Main Widget")
