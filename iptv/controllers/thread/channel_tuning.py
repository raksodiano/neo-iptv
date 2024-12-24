from PyQt6.QtCore import QThread, pyqtSignal
from concurrent.futures import ThreadPoolExecutor
import time
import random

from iptv.controllers.helpers import is_url_responsive
from iptv.models.database.channel import Channel


class ChannelTuningThread(QThread):
    """
    Thread class to handle the channel tuning process in background.
    Emits progress updates during the process.
    """
    progress_updated = pyqtSignal(int)  # Signal to update progress
    tuning_finished = pyqtSignal()  # Signal when the tuning process is finished

    def __init__(self, channels):
        super().__init__()
        self.channels = channels

    def run(self):
        """
        This method runs in a separate thread.
        It processes the channels in batches and updates their 'tuned' status.
        """
        total_channels = len(self.channels)
        batch_size = 100  # Process channels in batches of 100
        max_workers = min(batch_size, len(self.channels))  # Limiting the max workers

        # Process channels in batches
        for i in range(0, total_channels, batch_size):
            batch = self.channels[i:i + batch_size]
            # Using ThreadPoolExecutor to process the batch in parallel
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                results = list(executor.map(self.check_channel, batch))

            # Emit progress update after each batch
            progress = int((i + batch_size) / total_channels * 100)  # Calculate progress
            self.progress_updated.emit(progress)

            # Simulate some delay between batches (for demonstration)
            time.sleep(random.uniform(0.1, 0.5))  # Random delay between 100ms and 500ms

        # Emit finished signal after all batches are processed
        self.tuning_finished.emit()

    def check_channel(self, channel):
        """
        Checks if a channel is responsive and updates its status in the database.
        """
        if not is_url_responsive(channel, 3):
            print(f"Offline channel: {channel.name}")
            Channel.update_channel(channel.id, {"tuned": False})
        else:
            print(f"Online channel: {channel.name}")
            Channel.update_channel(channel.id, {"tuned": True})
        return channel
