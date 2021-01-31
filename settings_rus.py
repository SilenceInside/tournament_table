# Настройки для tt1.py
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QIcon


class Settings:
    def __init__(self) -> object:
        # Настройки центрального виджета
        self.font = QFont('SansSerif', 10)
        self.size = QSize(800, 600)
        self.minimum_size = QSize(800, 500)
        self.window_title = "Турнирная таблица"
        self.window_icon = QIcon('icon.png')

        # Настройки таблицы
        self.horizontal_labels = ['№', 'ФИО', 'Рейтинг', 'Дата рождения',
                                  'Ассоциация', 'Тренер', 'Примечание']
        self.col_count = len(self.horizontal_labels)
        self.row_count = 0
        self.min_col_width = [30, 130, 55]

        # Надписи
        self.label_1_font = QFont('SansSerif', 12)
        self.label_1_text = "Список участников"
        self.label_2_text = "Выберите количеств групп:"
        self.label_3_font = self.label_1_font
        self.label_3_text = "Распределение участников"
        self.label_4_text = "Выбрать вручную:"
        self.label_5_text = "Рейтинг"
        self.label_6_text = "Ассоциации"

        # Кнопки
        self.add_btn_text = "Добавить"
        self.del_btn_text = "Удалить"
        self.build_btn_text = "Построить таблицу"
        self.show_btn_text = "Показать"
