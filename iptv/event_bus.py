from PyQt6.QtCore import QObject, pyqtSignal


class EventBus(QObject):
    """EventBus to manage global signals."""

    channel_url_changed = pyqtSignal(str)
    volume_changed = pyqtSignal(int)
    mute_toggled = pyqtSignal(bool)
    playlist_toggle = pyqtSignal()
    fullscreen_toggle = pyqtSignal()

    def __init__(self):
        super().__init__()

    def emit_channel_url(self, url):
        """Emit a signal when the channel URL changes."""
        self.channel_url_changed.emit(url)

    def emit_volume(self, volume):
        """Emit a signal when the volume changes."""
        self.volume_changed.emit(volume)

    def emit_mute(self, muted):
        """Emit a signal when mute state changes."""
        self.mute_toggled.emit(muted)

    def emit_playlist_toggle(self):
        """Emit a signal to toggle playlist visibility."""
        self.playlist_toggle.emit()

    def emit_fullscreen_toggle(self):
        """Emit a signal to toggle fullscreen mode."""
        self.fullscreen_toggle.emit()


# Global EventBus instance
event_bus = EventBus()
