import sys

from PyQt5.QtWidgets import QApplication
from main_window import MainWindow


app = QApplication(sys.argv)

ui = MainWindow()
ui.show()

sys.exit(app.exec_())
