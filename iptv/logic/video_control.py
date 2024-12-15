import vlc


class VideoControl:
    def __init__(self):
        # Initialize VLC
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()

        # List to store videos
        self.video_list = []
        self.current_video_index = -1  # To track the current video

        # IPTV channel list (can be manually added)
        self.iptv_channels = [
            "https://stmv1.srvif.com/animetv/animetv/playlist.m3u8",
            "https://d1j2u714xk898n.cloudfront.net/v1/master/9d062541f2ff39b5c0f48b743c6411d25f62fc25/STIRR-MuxIP-24HourFreeMovies/145.m3u8",
            "http://sochinskayatrk.ru/hdtv/hls/43Channel_hd/playlist.m3u8"
        ]
        self.current_channel_index = -1

    def play_video(self, video_path, video_widget):
        """Play selected video"""
        if video_path:
            self.video_list.append(video_path)
            self.current_video_index = len(self.video_list) - 1
            media = self.vlc_instance.media_new(video_path)
            self.media_player.set_media(media)

            # Pass the media player to the VideoPlayerWidget for rendering
            video_widget.set_media_player(self.media_player)

            self.media_player.play()
            return video_path  # Return video path for status update

    def play_previous_channel(self, video_widget):
        """Play the previous IPTV channel"""
        if self.current_channel_index > 0:
            self.current_channel_index -= 1
            previous_channel_url = self.iptv_channels[self.current_channel_index]
            return self.play_iptv_channel(previous_channel_url, video_widget)
        return None

    def play_next_channel(self, video_widget):
        """Play the next IPTV channel"""
        if self.current_channel_index < len(self.iptv_channels) - 1:
            self.current_channel_index += 1
            next_channel_url = self.iptv_channels[self.current_channel_index]
            return self.play_iptv_channel(next_channel_url, video_widget)
        return None

    def play_previous_video(self, video_widget):
        """Play previous video"""
        if len(self.video_list) > 1 and self.current_video_index > 0:
            self.current_video_index -= 1
            previous_video = self.video_list[self.current_video_index]
            media = self.vlc_instance.media_new(previous_video)
            self.media_player.set_media(media)

            # Pass the media player to the VideoPlayerWidget for rendering
            video_widget.set_media_player(self.media_player)

            self.media_player.play()
            return previous_video

    def play_next_video(self, video_widget):
        """Play next video"""
        if len(self.video_list) > 1 and self.current_video_index < len(self.video_list) - 1:
            self.current_video_index += 1
            next_video = self.video_list[self.current_video_index]
            media = self.vlc_instance.media_new(next_video)
            self.media_player.set_media(media)

            # Pass the media player to the VideoPlayerWidget for rendering
            video_widget.set_media_player(self.media_player)

            self.media_player.play()
            return next_video

    def load_iptv_channels(self):
        """Load IPTV channels (example with static list)"""
        print("IPTV Channels Loaded:", self.iptv_channels)

    def play_iptv_channel(self, channel_url, video_widget):
        """Play IPTV channel"""
        if channel_url:
            media = self.vlc_instance.media_new(channel_url)
            self.media_player.set_media(media)

            # Pass the media player to the VideoPlayerWidget for rendering
            video_widget.set_media_player(self.media_player)

            self.media_player.play()
            return channel_url
