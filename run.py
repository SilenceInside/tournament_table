import sys

from PyQt5.QtWidgets import QApplication
from tt import MainWindow, ResultWindow


app = QApplication(sys.argv)

ui = MainWindow()
ui.show()

sys.exit(app.exec_())
