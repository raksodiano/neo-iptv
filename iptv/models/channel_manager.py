from .database.channel import Channel


class ChannelManager:
    _instance = None
    _channels = None
    _current_channel = None

    @classmethod
    def get_instance(cls):
        """ Get the singleton instance of the ChannelManager """
        if cls._instance is None:
            cls._instance = ChannelManager()
        return cls._instance

    @property
    def channels(self):
        """ Get the loaded channels, or load them if not loaded yet """
        if self._channels is None:
            print("Loading channels from database...")
            self._channels = Channel.get_all_channels()
        return self._channels

    def refresh(self):
        """ Force the instance to reload all data from the database """
        self._channels = None
        self._current_channel = None
        self.channels  # This will reload the channels

    @property
    def current_channel(self):
        """ Get the current channel object """
        if not self._channels:
            print("No channels loaded")
            return None
        if self._current_channel is None:
            self._current_channel = self._channels[0]
        return self._current_channel

    def set_current_channel(self, channel_url):
        """ Set the current channel by passing the channel's URL """
        channel = next((ch for ch in self._channels if ch.url == channel_url), None)

        if channel:
            self._current_channel = channel
        else:
            self._current_channel = None

    def _get_channel_by_offset(self, offset):
        """ Get a channel by its offset from the current channel (next/previous) """
        if not self._channels or not self._current_channel:
            return None

        # Find the index of the current channel using its id
        current_channel_id = self._current_channel.id
        current_position = next(
            (index for index, channel in enumerate(self._channels) if channel.id == current_channel_id), None)

        if current_position is None:
            print("Current channel not found in the channel list")
            return None

        # Calculate the new position
        new_position = (current_position + offset) % len(self._channels)

        # Return the channel at the new position
        return self._channels[new_position]

    def get_next_channel(self):
        """ Get the next channel in the list, or the first channel if at the end """
        self._current_channel = self._get_channel_by_offset(1)
        return self._current_channel

    def get_previous_channel(self):
        """ Get the previous channel in the list, or the last channel if at the start """
        self._current_channel = self._get_channel_by_offset(-1)
        return self._current_channel

    def get_first_channel(self):
        """ Get the first channel in the list and set it as the current channel """
        if not self._channels:
            print("No channels available")
            return None
        self._current_channel = self._channels[0]
        return self._current_channel
