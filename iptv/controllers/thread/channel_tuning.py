import random
import time
from concurrent.futures import ThreadPoolExecutor

from PyQt6.QtCore import QThread, pyqtSignal

from iptv.config.logger import logger
from iptv.controllers.helpers import is_url_responsive
from iptv.models.database.channel import Channel


def check_channel(channel):
    """
    Checks if a channel is responsive and updates its status in the database.
    """
    Channel.update_channel(channel.id, {"tuned": is_url_responsive(channel)})

    return channel


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
                list(executor.map(check_channel, batch))

            # Emit progress update after each batch
            progress = int((i + batch_size) / total_channels * 100)  # Calculate progress
            self.progress_updated.emit(progress)

            logger.info(f"Processed {i + len(batch)} out of {total_channels} channels ({progress}%)")

            # Simulate some delay between batches (for demonstration)
            time.sleep(random.uniform(0.1, 0.5))  # Random delay between 100ms and 500ms

        # Emit finished signal after all batches are processed
        self.tuning_finished.emit()
