import locale
import os
import sys

from PyQt6.QtWidgets import QApplication
from iptv.models.channel_manager import ChannelManager
from iptv.models.database.channel import Channel
from iptv.views.main_window import MainWindow

os.environ["LC_NUMERIC"] = "C"
locale.setlocale(locale.LC_NUMERIC, 'C')
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


def initialize_channels():
    channel_manager = ChannelManager.get_instance()
    channels = channel_manager.get_channels()
    print(f"Loaded {len(channels)} channels.")
    return channels


def main():
    # Create the database
    Channel.create_table()
    initialize_channels()

    # Create the application
    app = QApplication(sys.argv)

    # Create the main window
    window = MainWindow()
    window.show()

    # Run the application's event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
