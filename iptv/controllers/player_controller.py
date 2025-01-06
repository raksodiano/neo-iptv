import requests
from PyQt6.QtCore import QThread, pyqtSignal

from iptv.config.logger import logger
from iptv.event_bus import event_bus
from iptv.models.channel_manager import ChannelManager


def is_valid_url(url):
    """ Validate if the URL is accessible. """
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


class PlayerController(QThread):
    playback_started = pyqtSignal()
    playback_error = pyqtSignal(str)
    playback_status_changed = pyqtSignal(str)
    channel_url_changed = pyqtSignal(str)

    def __init__(self, player, url):
        super().__init__()
        self.player = player
        self.url = url

        event_bus.channel_url_changed.connect(self.update_video_url)
        event_bus.volume_changed.connect(self.update_volume)
        event_bus.mute_toggled.connect(self.toggle_mute)

        self.channel_url_changed.connect(self.update_video_url)

    def run(self):
        """ Play the video in the background. """
        try:
            if is_valid_url(self.url):
                # Start playback in the background
                self.player.play(self.url)
                self.player.observe_property('playback-status', self.on_playback_status_change)
                self.playback_started.emit()
            else:
                self.playback_error.emit("Invalid URL")
        except Exception as e:
            logger.error(f"Error: {e}")
            self.playback_error.emit(f"Error: {str(e)}")

    def stop_video(self):
        """ Stop the current video playback. """
        try:
            self.player.stop()
            self.playback_status_changed.emit("stopped")
        except Exception as e:
            logger.error(f"Error: {e}")
            self.playback_error.emit(f"Error: {str(e)}")

    def on_playback_status_change(self, name, value):
        """ Called when playback status changes (playing, paused). """
        self.playback_status_changed.emit(value)

    def update_video_url(self, new_url: str):
        """ Handle a change in video URL."""
        if is_valid_url(new_url):
            logger.info(f"New Channel: {new_url}")
            ChannelManager.get_instance().set_current_channel(new_url)
            self.url = new_url
            self.player.play(new_url)
            self.playback_status_changed.emit("playing")
        else:
            logger.info(f"Channel URL is not valid or accessible: {new_url}")

    def update_volume(self, volume: int):
        """ Handle a change in volume."""
        self.player.volume = volume

    def toggle_mute(self, muted: bool):
        """ Handle mute toggle."""
        self.player.mute = muted
