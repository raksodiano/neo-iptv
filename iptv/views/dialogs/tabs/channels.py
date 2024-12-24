from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QHBoxLayout,
    QProgressBar
)

from iptv.controllers.helpers import filter_responsive_channels
from iptv.controllers.thread.channel_tuning import ChannelTuningThread
from iptv.models.database.channel import Channel


class ChannelTab(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout (with margin adjustments)
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Label at the top
        self.label = QLabel("Manage your IPTV Channels", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.label)

        # Layout for buttons (horizontal alignment)
        button_layout = QVBoxLayout()

        # Buttons to load channels from file and URL
        self.load_file_button = QPushButton("Load Channels from File", self)
        self.load_url_button = QPushButton("Load Channels from URL", self)
        self.tune_button = QPushButton("Tune Channels", self)

        # Connect buttons to their respective methods
        self.load_file_button.clicked.connect(self.load_channels_from_file)
        self.load_url_button.clicked.connect(self.load_channels_from_url)
        self.tune_button.clicked.connect(self.start_tuning)

        # Add buttons to the layout
        button_layout.addWidget(self.load_file_button)
        button_layout.addWidget(self.load_url_button)
        button_layout.addWidget(self.tune_button)

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        # Waiting label (initially hidden)
        self.wait_label = QLabel("", self)
        self.wait_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wait_label.setVisible(False)
        layout.addWidget(self.wait_label)

        # Progress bar (initially hidden)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Message label (initially hidden)
        self.message_label = QLabel("", self)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setVisible(False)
        layout.addWidget(self.message_label)

        # Add a spacer to ensure that the buttons are placed together and pushed towards the bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        # Set the layout for the widget
        self.setLayout(layout)

    def start_tuning(self):
        """
        This function is called when the 'Tune Channels' button is pressed.
        It triggers the tuning process in a separate thread to avoid UI blocking.
        """
        # Show waiting message and progress bar
        self.wait_label.setText("Please wait while tuning the channels...")
        self.wait_label.setVisible(True)

        # Hide the buttons while tuning
        self.load_file_button.setEnabled(False)
        self.load_url_button.setEnabled(False)
        self.tune_button.setEnabled(False)

        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)  # Reset progress to 0

        # Show waiting message
        self.message_label.setText("""
            The channels are being tuned, please wait. <br><br>
            
            This process will only hide the channels that are currently not responsive until they are tuned again. <br>
            It will not hide channels that are inaccessible due to other reasons. <br> 
            Please note that some channels may not be active 24/7 and could disappear during a tuning.
    
            To ensure the process completes successfully, avoid closing the settings window, as it may cancel the tuning.
            """)
        self.message_label.setVisible(True)

        # Create and start the tuning thread
        channels = Channel.get_all_channels_without_filters()
        self.tuning_thread = ChannelTuningThread(channels)

        # Connect signals for progress updates and when finished
        self.tuning_thread.progress_updated.connect(self.update_progress)
        self.tuning_thread.finished.connect(self.on_tuning_finished)

        # Start the tuning thread
        self.tuning_thread.start()

    def update_progress(self, progress):
        """
        This function updates the progress bar during the tuning process.
        :param progress: The current progress (between 0 and 100).
        """
        self.progress_bar.setValue(progress)

    def on_tuning_finished(self):
        """
        This function is called when the tuning process has finished.
        It updates the UI to reflect the completion of the tuning process.
        """
        self.wait_label.setText("Channels tuned successfully!")
        self.wait_label.setVisible(True)  # Show the success message

        # Hide the progress bar
        self.progress_bar.setVisible(False)

        # Re-enable buttons after the tuning process is finished
        self.load_file_button.setEnabled(True)
        self.load_url_button.setEnabled(True)
        self.tune_button.setEnabled(True)

    def load_channels_from_file(self):
        """ Placeholder for the method to load channels from a file """
        print("Loading channels from file...")

    def load_channels_from_url(self):
        """ Placeholder for the method to load channels from a URL """
        print("Loading channels from URL...")
