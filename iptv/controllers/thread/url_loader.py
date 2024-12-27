import random
import time
from concurrent.futures import ThreadPoolExecutor

from PyQt6.QtCore import QThread, pyqtSignal
from ipytv import playlist

from iptv.controllers.helpers import process_channel_entry


class URLLoaderThread(QThread):
    """
    Thread class to handle loading channels from a URL in the background.
    Emits progress updates during the process.
    """
    progress_signal = pyqtSignal(int)
    completed_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        """
        Loads the playlist from the provided URL and processes the channels in batches.
        """
        try:
            # Load the playlist from the URL using ipytv
            pl = playlist.loadu(self.url)

            if not pl.get_channels():
                raise ValueError("The URL is invalid or cannot be parsed.")

            # Extract the channel data from the playlist
            channels = [{"name": entry.name, "url": entry.url} for entry in pl.get_channels()]
            total_channels = len(channels)
            batch_size = 100
            max_workers = min(batch_size, total_channels)

            # Process channels in batches
            for i in range(0, total_channels, batch_size):
                batch = channels[i:i + batch_size]
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    list(executor.map(process_channel_entry, batch))

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
