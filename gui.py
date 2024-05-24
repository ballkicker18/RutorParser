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
    QLineEdit,
    QDialog
)
from rutor import *
import webbrowser

class TorrentDialog(QDialog):
    def __init__(self, torrent: Torrent):
        super().__init__()
        self.setWindowTitle(torrent.name)
        layout = QVBoxLayout()
        self.torrent = torrent

        self.name_label = QLabel(torrent.name)
        self.date_label = QLabel(f'Дата: {torrent.date.day}.{torrent.date.month}.{torrent.date.year}')
        self.size_label = QLabel(f"Размер: {torrent.size}")
        self.peers_label = QLabel(f"Пиры:\tUp: {torrent.get_up_peers()}; Down: {torrent.get_down_peers()}")

        layout.addWidget(self.name_label)
        layout.addWidget(self.date_label)
        layout.addWidget(self.size_label)
        layout.addWidget(self.peers_label)

        self.torrent_download_button = QPushButton('Скачать торрент')
        self.torrent_download_button.clicked.connect(self.download_torrent)
        layout.addWidget(self.torrent_download_button)
        
        self.setLayout(layout)
    
    def download_torrent(self):
        webbrowser.open(self.torrent.get_torrent_link())

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

        button = QPushButton('Поиск')
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
                self.torrents_list.addItem(QListWidgetItem(f'{torrent.name}'))
        else:
            pass

    def search_return_pressed(self):
        self.search_and_add()

    def torrent_clicked(self, item):
        for torrent in self.torrents:
            if item.text() == torrent.name:
                logger.debug('Starting dialog')
                torrentdialog = TorrentDialog(torrent)
                torrentdialog.exec()

    def search_button_clicked(self):
        self.search_and_add()
