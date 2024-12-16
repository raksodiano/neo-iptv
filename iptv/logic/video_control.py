import vlc
from config.channels import ChannelManager
from utils.helpers import get_channel_index_by_url


class VideoControl:
    def __init__(self):
        # Initialize VLC
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()

        self.current_channel = None

        self.channels = ChannelManager().channels

    def play_iptv_channel(self, channel, video_widget):
        """Play IPTV channel"""
        if channel:
            print(channel)
            self.current_channel = channel
            media = self.vlc_instance.media_new(channel['url'])
            self.media_player.set_media(media)

            # Pass the media player to the VideoPlayerWidget for rendering
            video_widget.set_media_player(self.media_player)

            self.media_player.play()
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
