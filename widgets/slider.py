from PyQt5 import QtCore
from PyQt5.QtWidgets import QSlider


class Slider(QSlider):
    def __init__(self, *args, value=5, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTickPosition(3)
        self.setTickInterval(1)
        self.setSingleStep(1)
        self.setRange(0, 10)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setValue(value)
