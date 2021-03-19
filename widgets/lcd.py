from PyQt5.QtWidgets import QLCDNumber


class LCD(QLCDNumber):
    def __init__(self, *args, value=0.5, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSegmentStyle(2)
        self.setDigitCount(3)
        self.display(value)

