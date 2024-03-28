import sys
import time
import datetime
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QTabWidget, QWidget, QVBoxLayout, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hello World')
        self.resize(640,480)
        
        tab_widget = QTabWidget()
        tab_widget.addTab(MainTab(), 'Main')
        tab_widget.addTab(VersionTab(), 'Version')
        self.setCentralWidget(tab_widget)

class MainTab(QWidget):
    def __init__(self):
        super().__init__()
        box = QVBoxLayout(self)
        self.setLayout(box)

        label = QLabel('This is Main Tab')
        box.addWidget(label)
        self.test = QLabel(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))
        box.addWidget(self.test)

        self.update_timer = QTimer()
        self.update_timer.setInterval(33)
        self.update_timer.timeout.connect(self.update_test_label)
        self.update_timer.start(33)

    def update_test_label(self):
        self.test.setText(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))

class VersionTab(QWidget):
    def __init__(self):
        super().__init__()
        box = QVBoxLayout(self)
        self.setLayout(box)
        
        label = QLabel('Version 1.0')
        btn = QPushButton('Test')
        box.addWidget(label)
        box.addWidget(btn)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()