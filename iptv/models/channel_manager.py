from .database.channel import Channel


class ChannelManager:
    _instance = None
    _channels = None
    _current_channel = None  # Variable para almacenar el canal actual

    @classmethod
    def get_instance(cls):
        """ Get the singleton instance of the ChannelManager """
        if cls._instance is None:
            cls._instance = ChannelManager()
        return cls._instance

    def load_channels(self):
        """ Load channels from the database into the singleton instance """
        if self._channels is None:
            print("Loading channels from database...")
            self._channels = Channel.get_all_channels()
        return self._channels

    def get_channels(self):
        """ Get the loaded channels, or load them if not loaded yet """
        return self._channels if self._channels else self.load_channels()

    def get_current_channel(self):
        """ Get the current channel object """
        if self._channels and len(self._channels) > 0:
            if self._current_channel is None:
                self._current_channel = self._channels[0]
            return self._current_channel
        else:
            print("No channels loaded")
            return None

    def set_current_channel(self, channel):
        """ Set the current channel by passing the channel object """
        if channel in self._channels:
            self._current_channel = channel
        else:
            self._current_channel = None

    def get_next_channel(self):
        """ Get the next channel in the list, or the first channel if at the end """
        if self._channels and self._current_channel:
            current_channel = self._current_channel
            current_position = self._channels.index(current_channel)
            next_position = (current_position + 1) % len(self._channels)
            self._current_channel = self._channels[next_position]
            return self._current_channel
        return None

    def get_previous_channel(self):
        """ Get the previous channel in the list, or the last channel if at the start """
        if self._channels and self._current_channel:
            current_channel = self._current_channel
            current_position = self._channels.index(current_channel)
            prev_position = (current_position - 1) % len(self._channels)
            self._current_channel = self._channels[prev_position]
            return self._current_channel
        return None

    def get_first_channel(self):
        """ Get the first channel in the list and set it as the current channel """
        if not self._channels:
            print("No channels available")
            return None

        if self._current_channel is None:
            self._current_channel = self._channels[0]

        return self._current_channel
