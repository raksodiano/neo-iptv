from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListView,
    QAbstractItemView,
    QLabel
)

from iptv.event_bus import event_bus
from iptv.models.channel_manager import ChannelManager


class Playlist(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border: none;")

        # Label to show the count of channels
        self.channel_count_label = QLabel("Channels count: 0", self)
        layout.addWidget(self.channel_count_label)

        # Create the list view and model
        self.playlist = QListView(self)
        self.playlist.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        # Create the item model
        self.playlist_model = QStandardItemModel()
        self.playlist.setModel(self.playlist_model)

        # Initialize the playlist with current channels
        self.load_channels()

        # Connect the selection signal of the list to a slot
        self.playlist.selectionModel().selectionChanged.connect(self.on_channel_selected)

        # Connect to the EventBus signal for channel updates
        event_bus.channels_updated.connect(self.on_channels_updated)

        # Add the list view to the layout
        layout.addWidget(self.playlist)

        self.setLayout(layout)

    def load_channels(self):
        """ Load channels from the ChannelManager and update the playlist """
        # Clear the model
        self.playlist_model.clear()

        # Get channels from the ChannelManager
        channels = ChannelManager.get_instance().channels

        print(f"Channels Playlist: {len(channels)}")

        # Update the label with the count of channels
        self.update_channel_count_label(len(channels))

        # Add the channels to the model
        for channel in channels:
            item = QStandardItem(channel.name)  # Use the channel's name
            item.setData(channel.url, Qt.ItemDataRole.UserRole)  # Store the URL as additional data
            self.playlist_model.appendRow(item)

    def update_channel_count_label(self, count):
        """ Update the label to display the count of channels """
        self.channel_count_label.setText(f"Channels count: {count}")

    def on_channel_selected(self):
        """ Handle the selection of a channel from the playlist and emit its URL """
        selected_index = self.playlist.selectedIndexes()
        if selected_index:
            selected_item = selected_index[0]
            url = selected_item.data(Qt.ItemDataRole.UserRole)
            event_bus.channel_url_changed.emit(url)

    def on_channels_updated(self):
        """ Handle the channels_updated signal from the EventBus """
        print("Channels updated signal received.")
        ChannelManager.get_instance().refresh()
        self.load_channels()
