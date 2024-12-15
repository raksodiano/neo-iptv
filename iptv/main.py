import sys
import os
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow

# Ensure that the root project directory is in the PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


def main():
    # Create the application
    app = QApplication(sys.argv)

    # Create the main window and show it
    window = MainWindow()
    window.show()

    # Run the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
