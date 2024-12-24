from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class NetworkTab(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QVBoxLayout
        layout = QVBoxLayout()

        # Create a QLabel
        label = QLabel("Hello, this is a network label!", self)

        # Add the label to the layout
        layout.addWidget(label)

        # Set the layout for the widget
        self.setLayout(layout)
