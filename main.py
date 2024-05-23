from rutor import *
from gui import MainWindow, QApplication
import sys
import qdarkstyle
import os

def main():
    os.environ['QT_API'] = 'pyqt5'
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = MainWindow()
    window.show()
    app.exec()

if __name__=='__main__':
    main()
