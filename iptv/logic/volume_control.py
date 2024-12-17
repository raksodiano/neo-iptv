class VolumeControl:
    def __init__(self, video_control):
        # Default volume level
        self.video_control = video_control
        self.volume = 90

    def set_volume(self, value):
        """Set the volume in both the internal volume state and the VLC player."""
        self.volume = value
        self.video_control.set_volume(value)

    def get_volume(self):
        """Get the current volume level."""
        return self.volume
