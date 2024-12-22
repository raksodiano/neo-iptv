import logging
import re

import requests
from PyQt6.QtCore import QThread, pyqtSignal
from ipytv import playlist

from iptv.models.database.channel import Channel

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DownloadM3U(QThread):
    finished = pyqtSignal(object)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        """ This function will be executed in a separate thread. """
        try:
            logger.debug(f"Starting download from URL: {self.url}")

            # Download the content of the M3U URL
            response = requests.get(self.url, timeout=30)  # Added timeout to prevent hanging
            response.raise_for_status()  # This will raise an error if the download fails
            logger.debug(f"Successfully downloaded M3U content from {self.url}")

            # Load the M3U content from the downloaded URL
            m3u_playlist = playlist.loadf(response.text)  # Using loadf to load the M3U content
            logger.debug(f"Loaded M3U playlist with {len(m3u_playlist)} entries")

            valid_channels = []
            invalid_channels = []

            for entry in m3u_playlist:
                # Access the attributes of the IPTVChannel object directly
                channel_url = entry.url
                if self.is_valid_iptv_stream(channel_url):
                    valid_channels.append(channel_url)
                    Channel.insert_channel(entry)
                    logger.debug(f"Valid channel found: {channel_url}")
                else:
                    invalid_channels.append(channel_url)
                    logger.debug(f"Invalid channel found: {channel_url}")

            # Emit the result to be processed in the main UI
            self.finished.emit((valid_channels, invalid_channels))
            logger.info(
                f"Finished processing. Valid channels: {len(valid_channels)}, Invalid channels: {len(invalid_channels)}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error while downloading M3U URL: {e}")
            self.finished.emit(None)  # Emit None if there was an error

        except Exception as e:
            logger.error(f"Unexpected error during M3U processing: {e}")
            self.finished.emit(None)

    def is_valid_iptv_stream(self, uri):
        """ Verifies if the URI is a valid IPTV stream. """
        # Basic validation to ensure the URI is an HTTP(s) stream
        if re.match(r'^(http|https)://', uri):
            if uri.endswith('.m3u8') or uri.endswith('.ts') or re.search(r'rtmp://', uri):
                return True
        return False

    def add_channels_to_db(channels):
        """ Add valid channels to the database. """
        session = Session()

        try:
            for channel_url in channels:
                existing_channel = session.query(Channel).filter_by(url=channel_url).first()
                if existing_channel:
                    print(f"Channel {channel_url} already exists in the database.")
                else:
                    channel = Channel(url=channel_url)
                    session.add(channel)

            session.commit()
            print(f"Successfully added {len(channels)} channels to the database.")
        except Exception as e:
            session.rollback()
            print(f"Error adding channels to the database: {e}")
        finally:
            session.close()
