from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTabWidget

from iptv.views.dialogs.tabs.advance import AdvanceTab
from iptv.views.dialogs.tabs.channels import ChannelTab
from iptv.views.dialogs.tabs.image import ImageTab
from iptv.views.dialogs.tabs.network import NetworkTab
from iptv.views.dialogs.tabs.sound import SoundTab


class SettingsDialog(QDialog):
    """ Dialog for the application settings with tabs """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setFixedSize(700, 400)

        # Create the main layout for the dialog
        main_layout = QVBoxLayout()

        # Create the QTabWidget to hold different settings sections
        self.tab_widget = QTabWidget(self)

        # Create tabs
        self.advance_tab = AdvanceTab()
        self.channel_tab = ChannelTab()
        self.image_tab = ImageTab()
        self.network_tab = NetworkTab()
        self.sound_tab = SoundTab()

        # Add tabs to the QTabWidget
        # self.tab_widget.addTab(self.advance_tab, "Settings")
        # self.tab_widget.addTab(self.image_tab, "Image")
        # self.tab_widget.addTab(self.sound_tab, "Sound")
        # self.tab_widget.addTab(self.network_tab, "Network")
        self.tab_widget.addTab(self.channel_tab, "Channels")

        # Add the QTabWidget to the main layout
        main_layout.addWidget(self.tab_widget)

        # Set the layout for the dialog
        self.setLayout(main_layout)
