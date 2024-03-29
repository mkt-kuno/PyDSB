import sys
import time
import datetime
import utils
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QFont, QPalette, QColor
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QTabWidget, QGridLayout, QFrame
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hello World')
        self.resize(640,480)
        
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        
        tab_widget = QTabWidget()
        tab_widget.addTab(MainTab(), 'Main')
        tab_widget.addTab(VersionTab(), 'Version')
        self.setCentralWidget(tab_widget)

class AnalogInChannelBox(QGroupBox):
    def __init__(self, config:utils.DChannel) -> None:
        super().__init__()
        self.setTitle(config.id)

        self._grid = QGridLayout(self)
        self.setLayout(self._grid)

        self._grid.addWidget(QLabel(config.raw.label), 0, 0, Qt.AlignLeft)
        self._grid.addWidget(QLabel(config.phy.label), 1, 0, Qt.AlignLeft)
        self._grid.addWidget(QLabel(config.raw.unit), 0, 2, Qt.AlignRight)
        self._grid.addWidget(QLabel(config.phy.unit), 1, 2, Qt.AlignRight)
        
        self._raw_format = config.raw.format
        self._raw = QLabel()
        self.set_raw_value(0.0)
        self._raw.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._raw.setPalette(QPalette(QColor(255,255,255)))
        self._raw.setAutoFillBackground(True)
        self._grid.addWidget(self._raw, 0, 1, Qt.AlignRight)

        self._phy_format = config.phy.format
        self._phy = QLabel()
        self.set_phy_value(0.0)
        self._phy.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._phy.setPalette(QPalette(QColor(255,255,255)))
        self._phy.setAutoFillBackground(True)
        self._grid.addWidget(self._phy, 1, 1, Qt.AlignRight)
    
    def set_raw_value(self, value: float):
        self._raw.setText(self._raw_format.format(value))
    
    def set_phy_value(self, value: float):
        self._phy.setText(self._phy_format.format(value))

class MainTab(QWidget):
    def __init__(self):
        super().__init__()

        box = QVBoxLayout(self)
        self.setLayout(box)
        
        # @test
        import Model
        config = Model.Model().test_get_channel_list()

        wid = QWidget()
        grid = QGridLayout()
        for row in range(3):
            for col in range(6):
                grid.addWidget(AnalogInChannelBox(config), row, col)
        wid.setLayout(grid)
        box.addWidget(wid)

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