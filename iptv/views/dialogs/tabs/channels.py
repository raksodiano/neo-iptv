from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QProgressBar,
    QFileDialog,
    QMessageBox,
    QLineEdit,
    QHBoxLayout
)

from iptv.controllers.thread.channel_tuning import ChannelTuningThread
from iptv.controllers.thread.file_loader import FileLoaderThread
from iptv.event_bus import event_bus
from iptv.models.database.channel import Channel


class ChannelTab(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Label at the top
        self.label = QLabel("Manage your IPTV Channels", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.label)

        # Layout for buttons (vertical alignment)
        button_layout = QVBoxLayout()

        # Buttons to load channels from file and URL
        self.load_file_button = QPushButton("Load Channels from File", self)
        self.load_url_button = QPushButton("Load Channels from URL", self)
        self.tune_button = QPushButton("Tune Channels", self)

        # Connect buttons to their respective methods
        self.load_file_button.clicked.connect(self.load_channels_from_file)
        self.load_url_button.clicked.connect(self.toggle_url_input)
        self.tune_button.clicked.connect(self.start_tuning)

        # Add buttons to the layout
        button_layout.addWidget(self.load_file_button)
        button_layout.addWidget(self.load_url_button)
        button_layout.addWidget(self.tune_button)

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        # URL input section (hidden by default)
        self.url_input_layout = QHBoxLayout()
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter URL here...")
        self.url_input.setVisible(False)

        self.load_url_confirm_button = QPushButton("Load", self)
        self.load_url_confirm_button.setVisible(False)
        self.load_url_confirm_button.clicked.connect(self.load_channels_from_url)

        self.url_input_layout.addWidget(self.url_input)
        self.url_input_layout.addWidget(self.load_url_confirm_button)
        layout.addLayout(self.url_input_layout)

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

        # Add a spacer
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        # Set the layout for the widget
        self.setLayout(layout)

        self.file_loader_thread = None

    def toggle_url_input(self):
        """
        Toggles the visibility of the URL input and confirm button when 'Load Channels from URL' is clicked.
        """
        is_visible = not self.url_input.isVisible()
        self.url_input.setVisible(is_visible)
        self.load_url_confirm_button.setVisible(is_visible)

    def start_tuning(self):
        """
        This function is called when the 'Tune Channels' button is pressed.
        It triggers the tuning process in a separate thread to avoid UI blocking.
        """
        confirm = QMessageBox.question(
            self,
            "Confirm Load",
            f"Do you want to tune the channels? This will take some time.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        # Show waiting message and progress bar
        self.wait_label.setText("Please wait while tuning the channels...")
        self.wait_label.setVisible(True)

        # Hide the buttons while tuning
        self.load_file_button.setEnabled(False)
        self.load_url_button.setEnabled(False)
        self.tune_button.setEnabled(False)

        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # Show waiting message
        self.message_label.setText("""
            The channels are being tuned, please wait. <br><br>

            This process will only hide the channels that are currently not responsive until they are tuned again. <br>
            It will not hide channels that are inaccessible due to other reasons. <br> 
            Please note that some channels may not be active 24/7 and could disappear during a tuning. <br><br> 

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
        self.wait_label.setVisible(True)

        self.message_label.setText("")
        self.message_label.setVisible(False)

        # Hide the progress bar
        self.progress_bar.setVisible(False)

        # Re-enable buttons after the tuning process is finished
        self.load_file_button.setEnabled(True)
        self.load_url_button.setEnabled(True)
        self.tune_button.setEnabled(True)

        # Emit the channels_updated signal
        event_bus.emit_channels_updated()

    def load_channels_from_file(self):
        """
        Opens a file dialog to select an M3U or M3U8 file, and starts the loading process.
        """

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select M3U/M3U8 File",
            "",
            "Playlist Files (*.m3u *.m3u8);;All Files (*)"
        )

        if not file_path:
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Load",
            f"Do you want to load channels from '{file_path}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        self.file_loader_thread = FileLoaderThread(file_path)
        self.file_loader_thread.progress_signal.connect(self.update_progress)
        self.file_loader_thread.completed_signal.connect(self.on_file_loading_complete)
        self.file_loader_thread.error_signal.connect(self.on_file_loading_error)

        self.wait_label.setText("Loading channels from file...")
        self.wait_label.setVisible(True)

        self.load_file_button.setEnabled(False)
        self.load_url_button.setEnabled(False)
        self.tune_button.setEnabled(False)

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.file_loader_thread.start()

    def on_file_loading_complete(self):
        """
        Handles actions after the file has been successfully loaded.
        """

        QMessageBox.information(self, "Success", "Channels loaded successfully!")
        self.wait_label.setText("Channels loaded successfully!")
        self.wait_label.setVisible(True)

        self.load_file_button.setEnabled(True)
        self.load_url_button.setEnabled(True)
        self.tune_button.setEnabled(True)

        self.progress_bar.setVisible(False)

        event_bus.emit_channels_updated()

    def on_file_loading_error(self, error_message):
        """
        Handles errors that occur during the file loading process.
        """
        QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")

        self.load_file_button.setEnabled(True)
        self.load_url_button.setEnabled(True)
        self.tune_button.setEnabled(True)

        self.progress_bar.setVisible(False)

    def load_channels_from_url(self):
        """
        Handles the loading of channels from the entered URL.
        """
        url = self.url_input.text().strip()

        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a valid URL.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Load",
            f"Do you want to load channels from the URL: '{url}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        # Logic to handle URL-based loading can be implemented here.
        QMessageBox.information(self, "URL Loading", f"Channels are being loaded from: {url}")
