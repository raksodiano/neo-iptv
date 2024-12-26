import random
import time
from concurrent.futures import ThreadPoolExecutor

from PyQt6.QtCore import QThread, pyqtSignal
from ipytv import playlist

from iptv.models.database.channel import Channel


def process_channel_entry(entry_data):
    """
    Processes a single channel's data from the playlist entry and inserts it into the database.
    """
    channel_name = entry_data["name"]
    channel_url = entry_data["url"]

    # Avoid adding duplicate channels
    if Channel.get_channel_by_url(channel_url):
        return f"Channel '{channel_name}' already exists."

    # Insert the new channel into the database
    Channel.insert_channel({
        "name": channel_name,
        "url": channel_url,
        "tuned": False
    })

    return f"Channel '{channel_name}' added successfully."


class FileLoaderThread(QThread):
    """
    Thread class to handle loading channels from a file in the background.
    Emits progress updates during the process.
    """
    progress_signal = pyqtSignal(int)  # Signal to update progress
    completed_signal = pyqtSignal()  # Signal when the loading process is finished
    error_signal = pyqtSignal(str)  # Signal for errors during the process

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        """
        Reads the file and processes the channels in batches.
        """
        try:
            # Load the playlist file using ipytv
            pl = playlist.loadf(self.file_path)

            if not pl.get_channels():
                raise ValueError("The file is invalid or cannot be parsed.")

            # Extract the channel data from the playlist
            channels = [{"name": entry.name, "url": entry.url} for entry in pl.get_channels()]
            total_channels = len(channels)
            batch_size = 100
            max_workers = min(batch_size, total_channels)

            # Process channels in batches
            for i in range(0, total_channels, batch_size):
                batch = channels[i:i + batch_size]
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    results = list(executor.map(process_channel_entry, batch))

                # Emit progress update after each batch
                progress = int((i + len(batch)) / total_channels * 100)
                self.progress_signal.emit(progress)

                # Simulate some delay between batches
                time.sleep(random.uniform(0.1, 0.3))

            # Emit completion signal after all batches are processed
            self.completed_signal.emit()

        except Exception as e:
            # Emit an error signal if an exception occurs
            self.error_signal.emit(str(e))
