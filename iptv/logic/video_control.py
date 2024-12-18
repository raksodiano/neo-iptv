import mpv
from iptv.config.channels import ChannelManager
from iptv.utils.helpers import get_channel_index_by_url


class VideoControl:
    def __init__(self):
        # Inicializar MPV
        self.mpv_player = mpv.MPV()

        self.current_channel = None
        self.channels = ChannelManager().channels

    def play_iptv_channel(self, channel, video_widget):
        """Play IPTV channel"""
        if channel:
            print(channel)
            self.current_channel = channel

            # Cargar la URL del canal en MPV
            self.mpv_player.play(channel['url'])

            # Pasar el reproductor de MPV al widget de video para la renderización
            video_widget.set_media_player(self.mpv_player)

            return channel

    def play_previous_channel(self, video_widget):
        """Play the previous IPTV channel"""
        if self.current_channel is not None:
            current_index = get_channel_index_by_url(self.channels, self.current_channel['url'])

            if current_index > 0:
                previous_channel = self.channels[current_index - 1]
                self.current_channel = previous_channel
                return self.play_iptv_channel(previous_channel, video_widget)
        return None

    def play_next_channel(self, video_widget):
        """Play the next IPTV channel"""
        if self.current_channel is not None:
            current_index = get_channel_index_by_url(self.channels, self.current_channel['url'])

            if current_index < len(self.channels) - 1:
                next_channel = self.channels[current_index + 1]
                self.current_channel = next_channel
                return self.play_iptv_channel(next_channel, video_widget)
        return None

    def set_volume(self, volume):
        """Set the volume of the MPV player."""
        self.mpv_player.volume = volume
        print(f"Volume set to {volume}%")
