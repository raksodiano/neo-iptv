import sys

from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QDialog,
    QLabel,
    QHBoxLayout,
    QTextEdit,
    QFileDialog
)


class StreamToTextEdit(QObject):
    """ Redirects print() output to a QTextEdit widget """

    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def write(self, text):
        """ Writes the text to the QTextEdit if it's still valid """
        if self.text_edit and not self.text_edit.isDeleted():
            cursor = self.text_edit.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)  # Move cursor to the end
            cursor.insertText(text)  # Insert the text at the cursor position
            self.text_edit.setTextCursor(cursor)  # Update the text cursor
            self.text_edit.ensureCursorVisible()  # Ensure the cursor is visible

    def flush(self):
        """ Required method for print() compatibility """
        pass


class DownloadM3UThread(QThread):
    """ Thread for downloading and processing the M3U channels """

    new_message = pyqtSignal(str)  # Signal to send messages to QTextEdit

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        """ This runs when the thread starts """
        try:
            self.new_message.emit(f"Starting download from URL: {self.url}\n")
            # Simulate download and channel processing
            # The real download would happen here using `DownloadM3U`
            self.new_message.emit(f"Processing M3U from URL: {self.url}\n")
            # Simulate valid and invalid channels for demonstration
            valid_channels = ["Channel 1", "Channel 2"]
            invalid_channels = ["Channel X"]
            self.new_message.emit(f"Valid channels: {len(valid_channels)}\n")
            self.new_message.emit(f"Invalid channels: {len(invalid_channels)}\n")

            # Emit results (simulated)
            self.new_message.emit("Download finished.\n")
        except Exception as e:
            self.new_message.emit(f"Error: {str(e)}\n")


class LoadChannelsDialog(QDialog):
    """ Dialog for loading IPTV channels """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Load Channels")
        self.setFixedSize(400, 350)

        # Layout for the dialog
        layout = QVBoxLayout()

        # Add a label
        label = QLabel("Select an M3U file or URL to load channels.", self)
        layout.addWidget(label)

        # Add buttons
        self.file_button = QPushButton("Select M3U File", self)
        self.url_button = QPushButton("Enter M3U URL", self)

        # Connect buttons to corresponding actions
        self.file_button.clicked.connect(self.load_m3u_file)
        self.url_button.clicked.connect(self.show_url_input)

        # Add buttons to layout
        layout.addWidget(self.file_button)
        layout.addWidget(self.url_button)

        # QTextEdit to show terminal output
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)  # Make it read-only so users can't edit it
        layout.addWidget(self.text_area)

        self.setLayout(layout)

        # Redirect print() to QTextEdit
        sys.stdout = StreamToTextEdit(self.text_area)

    def show_url_input(self):
        """ Show the input field and 'Load' button for the M3U URL """
        # Hide the buttons
        self.file_button.setVisible(False)
        self.url_button.setVisible(False)

        # Create the URL input and load button
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter M3U URL")
        self.url_input.setClearButtonEnabled(True)

        self.load_button = QPushButton("Load", self)
        self.load_button.clicked.connect(self.load_url)

        # Layout for the new components
        url_layout = QHBoxLayout()
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.load_button)

        # Add the new layout to the dialog layout
        layout = self.layout()
        layout.addLayout(url_layout)

    def load_url(self):
        """ Handle the URL loading action """
        url = self.url_input.text().strip()
        if url:
            self.on_url_entered()

        self.accept()

    def on_url_entered(self):
        """ Processes the entered URL and loads the M3U data in a separate thread. """
        url = self.url_input.text().strip()
        if url:
            print(f"Starting download from URL: {url}")
            self.download_thread = DownloadM3UThread(url)
            self.download_thread.new_message.connect(self.append_message)
            self.download_thread.start()

        self.url_input.setVisible(False)

    def append_message(self, message):
        """ This function is called each time the thread sends a message """
        print(message)

    def load_m3u_file(self):
        """ Opens a dialog to load an M3U file and process it. """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select M3U File",
            "",
            "M3U Files (*.m3u);;All Files (*)",
            options=QFileDialog.Option.ReadOnly
        )

        if file_path:
            self.process_m3u_file(file_path)
