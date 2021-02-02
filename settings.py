from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QIcon


class Settings:
    def __init__(self) -> object:
        # Настройки центрального виджета
        self.font = QFont('SansSerif', 10)
        self.size = QSize(800, 600)
        self.minimum_size = QSize(800, 600)
        self.window_title = "Tournament table"
        self.window_icon = QIcon('icon.png')
        self.result_window_title = "Result"

        # Настройки таблицы
        self.horizontal_labels = ['№', 'Name', 'Rating', 'Birthday',
                                  'Association', 'Coach', 'Comment']
        self.col_count = len(self.horizontal_labels)
        self.row_count = 0
        self.min_col_width = [30, 130, 55]

        # Надписи
        self.label_1_font = QFont('SansSerif', 12)
        self.label_1_text = "List of participants"
        self.label_2_text = "Select the number of groups:"
        self.label_3_font = self.label_1_font
        self.label_3_text = "Distribution of participants"
        self.label_4_text = "Select:"
        self.label_5_text = "Rating"
        self.label_6_text = "Association"

        # Кнопки
        self.add_btn_text = "Add"
        self.del_btn_text = "Remove"
        self.build_btn_text = "Build a table"
        self.show_btn_text = "Show"
