from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QWidget,
    QPushButton,
    QListWidgetItem,
    QLineEdit
)
from rutor import *
import webbrowser

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Rutor Parser")
        layout = QVBoxLayout()

        self.torrents_list = QListWidget()
        self.torrents_list.itemDoubleClicked.connect(self.torrent_clicked)
        layout.addWidget(self.torrents_list)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введи название торрента")
        self.search_input.returnPressed.connect(self.search_return_pressed)
        layout.addWidget(self.search_input)

        button = QPushButton('Search')
        button.clicked.connect(self.search_button_clicked)
        layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.rutor = Rutor()

    def search_and_add(self):
        text = self.search_input.text()
        if len(text) > 3:
            self.torrents = self.rutor.search(text)
            self.torrents_list.clear()
            for torrent in self.torrents:
                self.torrents_list.addItem(QListWidgetItem(torrent.name))
        else:
            pass

    def search_return_pressed(self):
        self.search_and_add()

    def torrent_clicked(self, item):
        for torrent in self.torrents:
            if item.text() == torrent.name:
                webbrowser.open(torrent.get_torrent_link())

    def search_button_clicked(self):
        self.search_and_add()
