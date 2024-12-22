import re

from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMenu, QFileDialog, QMessageBox, QLineEdit
from iptv.controllers.download_m3u import DownloadM3U
from iptv.models.database.channel import Channel
from ipytv import playlist

from iptv.controllers.helpers import filter_responsive_channels


class Settings(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QVBoxLayout()

        # Create a button to settings menu
        self.gear_button = QPushButton()
        self.gear_button.setIcon(QIcon.fromTheme("preferences-system"))
        self.gear_button.setToolTip("Click to open settings menu")

        # Create a menu for the button
        self.menu = QMenu(self)

        # Add actions (settings options) to the menu
        self.load_channels_new = QAction("Load M3U File", self)
        self.load_url_action = QAction("Load M3U URL", self)
        self.tune_in = QAction("Tune in", self)

        self.load_channels_new.triggered.connect(self.load_m3u_file)
        self.load_url_action.triggered.connect(self.load_m3u_url)
        self.tune_in.triggered.connect(self.tune)

        self.menu.addAction(self.load_channels_new)
        self.menu.addAction(self.load_url_action)
        self.menu.addAction(self.tune_in)

        # Connect the button to show the menu when clicked
        self.gear_button.clicked.connect(self.show_menu)

        # Add the button to the layout
        layout.addWidget(self.gear_button)

        self.setLayout(layout)

        # URL input for direct URL entry
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter M3U URL")
        self.url_input.setVisible(False)  # Initially hide the URL input
        layout.addWidget(self.url_input)

    def show_menu(self):
        """ Show the settings menu when the gear button is clicked """
        self.menu.exec(self.gear_button.mapToGlobal(self.gear_button.rect().bottomLeft()))

    def load_m3u_file(self):
        """ Opens a dialog to load an M3U file and process it. """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select M3U File",
            "",
            "M3U Files (*.m3u);;All Files (*)",
            options=QFileDialog.Option.ReadOnly
        )

        if file_path:
            self.process_m3u_file(file_path)

    def load_m3u_url(self):
        """ Shows an input field to load an M3U URL and process it. """
        self.url_input.setVisible(True)  # Show the URL input field
        self.url_input.returnPressed.connect(self.on_url_entered)

    def on_url_entered(self):
        """ Processes the entered URL and loads the M3U data in a separate thread. """
        url = self.url_input.text().strip()
        if url:
            # Start the download and process in a separate thread
            self.download_thread = DownloadM3U(url)
            self.download_thread.finished.connect(self.on_download_finished)
            self.download_thread.start()

        self.url_input.setVisible(False)  # Hide the input after processing

    def on_download_finished(self, result):
        """ Called when the thread finishes downloading and processing the M3U URL. """
        if result:
            valid_channels, invalid_channels = result
            # Display the results
            if valid_channels:
                QMessageBox.information(self, "Success", f"Loaded {len(valid_channels)} valid IPTV streams.")
            if invalid_channels:
                print(f"Invalid channels found: {len(invalid_channels)}")
        else:
            QMessageBox.critical(self, "Error", "There was a problem processing the M3U URL.")

    def process_m3u_file(self, file_path):
        """ Processes the loaded M3U file using ipytv and validates if it's a valid IPTV playlist. """
        try:
            # Try loading the M3U file using ipytv
            m3u_playlist = playlist.loadf(file_path)  # Using loadf to load the M3U file

            # Check if the file contains a valid IPTV playlist
            valid_channels = []
            invalid_channels = []

            for entry in m3u_playlist:
                # Access the attributes of the IPTVChannel object directly
                channel_url = entry.url
                if self.is_valid_iptv_stream(channel_url):
                    valid_channels.append(channel_url)
                    Channel.insert_channel(entry)
                    print(f"Valid channel URI: {channel_url}")
                else:
                    invalid_channels.append(channel_url)
                    print(f"Invalid channel URI: {channel_url}")

            # Show a summary of valid channels
            if valid_channels:
                QMessageBox.information(self, "Success", f"Loaded {len(valid_channels)} valid IPTV streams.")

            if invalid_channels:
                print(f"Invalid channels found: {len(invalid_channels)}")

        except Exception as e:
            QMessageBox.critical(self, "General Error", f"An error occurred while loading the file: {e}")
            print(f"Error loading file: {e}")

    def is_valid_iptv_stream(self, uri):
        """ Verifies if the URI is a valid IPTV stream. """
        if re.match(r'^(http|https)://', uri):
            if uri.endswith('.m3u8') or uri.endswith('.ts') or re.search(r'rtmp://', uri):
                return True
        return False

    def tune(self):
        """ Tune in channels """
        channels = Channel.get_all_channels_without_filters()
        filter_responsive_channels(channels)
