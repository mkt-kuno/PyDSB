import sys
from PySide6.QtCore import Qt
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