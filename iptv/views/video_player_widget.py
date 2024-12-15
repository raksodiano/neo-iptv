from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QColor
import vlc


class VideoPlayerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: black;")  # Set black background

        # Create VLC instance and player
        self.vlc_instance = vlc.Instance('--vout=drm')  # Use drm output for better integration
        self.media_player = self.vlc_instance.media_player_new()

        # Timer to refresh widget and update the paintEvent
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_video)
        self.update_timer.start(100)  # Update every 100 ms (~10 FPS)

        # Flag to track whether video is playing
        self.is_playing = False

    def set_media_player(self, media_player):
        """Sets the VLC media player for video rendering in this widget"""
        self.media_player = media_player
        self.media_player.set_xwindow(int(self.winId()))  # Associate VLC player with this widget

    def play_media(self, media_url):
        """Play video or IPTV stream"""
        media = self.vlc_instance.media_new(media_url)
        self.media_player.set_media(media)
        self.media_player.play()
        self.is_playing = True

    def stop_media(self):
        """Stop video playback"""
        self.media_player.stop()
        self.is_playing = False

    def update_video(self):
        """Update the widget and render video"""
        if self.is_playing:
            self.update()  # Trigger the paintEvent to redraw the widget

    def paintEvent(self, event):
        """Custom paint event to show content while video is loading"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.is_playing:
            # If video is playing, just ensure the widget is updated with the video
            super().paintEvent(event)
        else:
            # If video is not yet playing, show a loading message
            painter.setPen(QColor(255, 255, 255))  # Set text color to white
            painter.setFont(self.font())
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Video is loading...")

    def resizeEvent(self, event):
        """Ensure video is resized with the widget"""
        super().resizeEvent(event)
        if self.is_playing:
            self.media_player.set_xwindow(int(self.winId()))  # Reassociate the window if resizing
