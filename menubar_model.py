"""Создание менюбара"""

from PyQt5.QtWidgets import QMainWindow, QMenu


class MenuBar(QMainWindow):
    """Класс для менюбара."""
    def __init__(self):
        super().__init__()
        self.setGeometry()
