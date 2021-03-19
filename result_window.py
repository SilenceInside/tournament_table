from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QDesktopWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, \
    QHBoxLayout

from settings import Settings
from widgets.tables import ResultTable


class ResultWindow(QMainWindow):
    """Таблица результатов"""
    def __init__(self, distributions, player_data, group_count, criterion_list, parent=None):
        super().__init__(parent)
        self.distributions = distributions
        self.player_data = player_data
        self.group_count = group_count
        self.criterion_list = criterion_list

        self.settings = Settings()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.setWindowTitle(self.settings.result_window_title)
        self.setWindowIcon(self.settings.window_icon)

        self.setupUI()

        self.center()
        self.init_result_data()

    def center(self):
        """Перемещает окно в середину рабочего стола."""
        rect = self.frameGeometry()
        center_position = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(center_position)
        self.move(rect.x(), rect.y())

    def init_widget_3(self):
        """Создает виджет таблиц решений."""
        self.widget_3 = QWidget(self.central_widget)

        self.result_table = ResultTable()
        self.result_table.setParent(self.widget_3)

        layout = QVBoxLayout(self.widget_3)
        layout.addWidget(self.result_table)
        self.widget_3.setLayout(layout)

    def init_widget_4(self):
        """Виджет выбора решения."""
        self.widget_4 = QWidget(self.central_widget)

        label = QLabel(self.settings.label_4_text, self.widget_4)

        self.choice_box = QComboBox(self.widget_4)
        for criterion in self.criterion_list:
            crit = '{0:f}'.format(criterion)
            self.choice_box.addItem(crit)

        show_btn = QPushButton(self.settings.show_btn_text, self.widget_4)
        show_btn.clicked.connect(self.show_chosen_result)

        hbox = QHBoxLayout(self.widget_4)
        hbox.addWidget(label)
        hbox.addWidget(self.choice_box)
        hbox.addWidget(show_btn)
        hbox.setAlignment(QtCore.Qt.AlignCenter)

        self.widget_4.setLayout(hbox)

    def setupUI(self):
        self.init_widget_3()
        self.init_widget_4()

        vbox = QVBoxLayout()
        vbox.addWidget(self.widget_3)
        vbox.addWidget(self.widget_4)
        self.central_widget.setLayout(vbox)

    def init_result_data(self):
        best_crit = self.criterion_list.index(min(self.criterion_list))
        self.choice_box.setCurrentIndex(best_crit)
        self.show_result(self.distributions[best_crit])

    def show_result(self, distr):
        """Заполняет таблицу результатов."""
        self.result_table.display_groups(distr, self.player_data)

    def show_chosen_result(self):
        """Заполняет таблицу результатов выбранным решением."""
        cur_index = self.choice_box.currentIndex()
        self.show_result(self.distributions[cur_index])
