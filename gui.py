from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QWidget,
    QPushButton,
    QListWidgetItem,
    QLineEdit,
    QDialog,
    QTextEdit,
    QScrollArea
)
from rutor import *
import webbrowser
import tempfile

class TorrentInfoDialog(QDialog):
    def __init__(self, info: str, image_dir: tempfile.TemporaryDirectory):
        super().__init__()
        self.setWindowTitle("Torrent Info")
        self.info = info
        self.image_dir = image_dir
        layout = QVBoxLayout()
        logger.debug(self.info)
        image_path = f'{self.image_dir}/torrent_image.jpg'
        self.image_label = QLabel()
        image_pixmap = QPixmap(image_path)
        scaled_pixmap = image_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        layout.addWidget(self.image_label)

        info_label = QTextEdit()
        info_label.setPlainText(info)
        info_label.setReadOnly(True)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(info_label)

        layout.addWidget(scroll_area)

        self.setLayout(layout)

class TorrentDialog(QDialog):
    def __init__(self, torrent: Torrent, rutor: Rutor):
        super().__init__()
        self.setWindowTitle(torrent.name)
        layout = QVBoxLayout()
        self.torrent = torrent
        self.rutor = rutor

        self.name_label = QLabel(torrent.name)
        self.date_label = QLabel(f'Дата: {torrent.date.day}.{torrent.date.month}.{torrent.date.year}')
        self.size_label = QLabel(f"Размер: {torrent.size}")
        self.peers_label = QLabel(f"Пиры:\tUp: {torrent.get_up_peers()}; Down: {torrent.get_down_peers()}")

        layout.addWidget(self.name_label)
        layout.addWidget(self.date_label)
        layout.addWidget(self.size_label)
        layout.addWidget(self.peers_label)
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()
        
        self.more_info_button = QPushButton('Узнать больше')
        self.more_info_button.clicked.connect(self.more_info)
        buttons_layout.addWidget(self.more_info_button)

        self.torrent_download_button = QPushButton('Скачать торрент')
        self.torrent_download_button.clicked.connect(self.download_torrent)
        buttons_layout.addWidget(self.torrent_download_button)

        buttons_widget.setLayout(buttons_layout)

        layout.addWidget(buttons_widget)
        
        self.setLayout(layout)
    
    def more_info(self):
        with tempfile.TemporaryDirectory() as tempdir:
            info = self.rutor.check_torrent_page(self.torrent, tempdir)
            info_dialog = TorrentInfoDialog(info, tempdir)
            info_dialog.exec()

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
                torrentdialog = TorrentDialog(torrent, self.rutor)
                torrentdialog.exec()

    def search_button_clicked(self):
        self.search_and_add()
