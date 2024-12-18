from iptv.utils.helpers import load_channels


class ChannelManager:
    """Singleton class to manage channels"""

    _instance = None
    _channels = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._channels = cls.load_channels()
        return cls._instance

    @staticmethod
    def load_channels():
        """Load channels from the file"""
        channels = load_channels()
        if channels:
            print(f"Loaded {len(channels)} channels.")
            return channels
        else:
            print("Failed to load channels.")
            return []

    @property
    def channels(self):
        """Getter for channels"""
        return self._channels
