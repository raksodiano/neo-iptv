from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QScrollArea, QLabel
from logic.video_control import VideoControl
from config.channels import ChannelManager


class PlaylistWidget(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)

        self.main_window = main_window

        # Create an instance of VideoControl
        self.video_control = VideoControl()

        # Access the Singleton instance of ChannelManager to get the channels
        self.channels = ChannelManager().channels

        # Vertical layout for the widget
        self.layout = QVBoxLayout(self)

        # QLabel to display the number of channels at the top
        self.channel_count_label = QLabel(self)
        self.channel_count_label.setStyleSheet("color: white; font-size: 14px; padding: 5px;")
        self.layout.addWidget(self.channel_count_label)  # Add it at the top

        # Empty playlist (no items initially)
        self.playlist_widget = QListWidget(self)
        # self.playlist_widget.setStyleSheet("QListWidget { border: none; }")  # No borders

        # Set the background color of the widget to black
        self.setStyleSheet("background-color: black;")

        # Ensure the playlist is empty
        self.playlist_widget.clear()

        # Add the playlist widget to the layout
        self.layout.addWidget(self.playlist_widget)

        # Add a scroll area to the list widget
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.playlist_widget)
        self.scroll_area.setWidgetResizable(True)  # Make the widget resizeable within the scroll area

        # Add the scroll area to the layout instead of the widget directly
        self.layout.addWidget(self.scroll_area)

        # Set the layout of the widget
        self.setLayout(self.layout)

        # Populate the playlist with channel data
        self.populate_playlist()

        # Connect item click event to a method
        self.playlist_widget.itemClicked.connect(self.on_item_clicked)

    def populate_playlist(self):
        """Populate the playlist with channel data."""
        # Ensure the playlist is empty before adding new items
        self.playlist_widget.clear()

        # Add each channel to the playlist widget
        for channel in self.channels:
            self.playlist_widget.addItem(channel['name'])

        # Update the channel count label with the number of channels
        self.update_channel_count()

    def update_channel_count(self):
        """Update the label with the count of channels."""
        channel_count = len(self.channels)  # Get the number of channels
        self.channel_count_label.setText(f"Channels Loaded: {channel_count}")

    def on_item_clicked(self, item):
        """Handle the click event on a playlist item."""
        channel_name = item.text()

        # Find the channel's URL based on its name
        selected_channel = next(
            (channel for channel in self.channels if channel['name'] == channel_name), None
        )

        if selected_channel:
            print(f"Channel {channel_name} clicked! ID: {selected_channel['name']}")

            if self.main_window:
                self.main_window.play_channel(selected_channel)
        else:
            print(f"Error: Channel '{channel_name}' not found.")
