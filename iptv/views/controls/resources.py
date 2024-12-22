from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListView
from PyQt6.QtCore import QStringListModel


class Resources(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Resources list (example with resource names)
        self.resources_list = QListView(self)
        self.resources_model = QStringListModel(["Image 1", "Image 2", "Video 1", "Audio 1"])
        self.resources_list.setModel(self.resources_model)
        layout.addWidget(self.resources_list)

        # Additional information label
        self.info_label = QLabel("Resources Info Here", self)
        layout.addWidget(self.info_label)

        self.setLayout(layout)
