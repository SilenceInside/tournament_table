# -*- coding: utf-8 -*-
import csv
import datetime
from operator import add, truediv

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QComboBox, QDesktopWidget,
                             QFileDialog, QLabel, QLCDNumber, QMainWindow,
                             QPushButton, QSlider, QSpinBox, QWidget,
                             QHBoxLayout, QVBoxLayout, QTableWidgetItem,
                             QAction, qApp, QSizePolicy)

from settings import Settings
from table_model import ParticipantTable, ResultTable

# from comb_algorithm import main
from algorithms.group_by_group import main
# from snake_with_lexical_alg import snake_plus_bruteforce as main
# from random_search import main
CHOICES = ['Brute force', 'Group by group', 'snake with brute force']


class MainWindow(QMainWindow):
    """Основное окно."""
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.settings = Settings()
        self.initUI()
        self.setupUI()

    def initUI(self):
        """Настраивает центральный виджет."""
        self.setFont(self.settings.font)
        self.resize(self.settings.size)
        self.setMinimumSize(self.settings.minimum_size)
        self.center()

        self.resize(self.settings.minimum_size)

        self.setWindowTitle(self.settings.window_title)
        self.setWindowIcon(self.settings.window_icon)
        self.init_menu()

    def center(self):
        """Перемещает окно в середину рабочего стола."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_menu(self):
        """Создает меню главного окна."""
        self.menubar = self.menuBar()

        self.file_menu = self.menubar.addMenu('Menu')

        action_exit = QAction('Exit', self)
        action_exit.setShortcut('Ctrl+Q')
        action_exit.triggered.connect(qApp.quit)

        action_load = QAction('Load', self)
        action_load.setShortcut('Ctrl+L')
        action_load.triggered.connect(self.load_csv)

        action_save = QAction('Save', self)
        action_save.setShortcut('Ctrl+S')
        action_save.triggered.connect(self.save_csv)

        self.file_menu.addAction(action_load)
        self.file_menu.addAction(action_save)
        self.file_menu.addAction(action_exit)

    def load_csv(self):
        """Загружает данные игроков из csv файла в таблицу."""
        file_name, _ = QFileDialog.getOpenFileName(None, "Load players list",
                                                   "", "Csv Files (*.csv);;All Files (*)")
        if file_name:
            for _ in range(self.table.rowCount()):
                self.table.removeRow(0)
            with open(file_name) as f:
                reader = csv.reader(f, delimiter=';', lineterminator='\n')
                for j, row in enumerate(reader):
                    self.table.insertRow(self.table.rowCount())
                    for i, element in enumerate(row):
                        item = QTableWidgetItem(element)
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.table.setItem(j, i, item)

    def save_csv(self):
        """Сохраняет данные игроков из таблицы в csv файл."""
        file_name, _ = QFileDialog.getSaveFileName(None, "Save players list", "",
                                                   "Csv Files (*.csv);; All Files (*)")
        if file_name:
            content = self.table.parse_for_csv()
            with open(file_name, 'w') as f:
                reader = csv.writer(f, delimiter=';', lineterminator='\n')
                reader.writerows(content)

    def setupUI(self):
        """Инициализирует макет главного окна."""
        self.init_players_table_widget()
        self.init_parameter_selection_widget()

        self.alpha_1 = 0.5
        self.alpha_2 = 0.5

        vbox = QVBoxLayout()
        vbox.addWidget(self.widget_1)
        vbox.addWidget(self.widget_2)

        self.central_widget.setLayout(vbox)

    def init_players_table_widget(self):
        """Строит таблицу участников с кнопками и надписью."""
        self.widget_1 = QWidget(self.central_widget)

        label = QLabel(self.settings.label_1_text, self.widget_1)
        label.setFont(self.settings.label_1_font)

        self.table = ParticipantTable(self.settings)
        self.table.setParent(self.widget_1)

        add_btn = QPushButton(self.settings.add_btn_text, self.widget_1)
        add_btn.clicked.connect(self.table.add_row)

        del_btn = QPushButton(self.settings.del_btn_text, self.widget_1)
        del_btn.clicked.connect(self.table.del_selected_row)

        hbox = QHBoxLayout()
        hbox.addWidget(label, alignment=QtCore.Qt.AlignRight)
        hbox.addWidget(add_btn, alignment=QtCore.Qt.AlignRight)
        hbox.addWidget(del_btn, alignment=QtCore.Qt.AlignRight)

        layout = QVBoxLayout()
        layout.addLayout(hbox)
        layout.addWidget(self.table)

        self.widget_1.setLayout(layout)

    def init_parameter_selection_widget(self):
        """Создает виджет выбора количества групп."""
        self.widget_2 = QWidget(self.central_widget)

        label = QLabel(self.settings.label_2_text, self.widget_2)

        self.spinbox = QSpinBox(self.widget_2)
        self.spinbox.setMinimum(2)
        self.spinbox.setMaximum(20)

        alg_label = QLabel(self.settings.label_alg_text, self.widget_2)
        self.alg_combobox = QComboBox(self.widget_2)
        for item in CHOICES:
            self.alg_combobox.addItem(item)

        self.sld = self.init_slider_widget()

        label1 = QLabel(self.settings.label_5_text, self.widget_2)
        label2 = QLabel(self.settings.label_6_text, self.widget_2)

        self.lcd_1 = self.init_lcd()
        self.lcd_2 = self.init_lcd()

        build_btn = QPushButton(self.settings.build_btn_text, self.widget_2)
        build_btn.clicked.connect(self.build_result_table)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.spinbox)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        layout_alg = QHBoxLayout()
        layout_alg.addWidget(alg_label)
        layout_alg.addWidget(self.alg_combobox)
        layout_alg.setAlignment(QtCore.Qt.AlignCenter)

        layout_sld = QHBoxLayout()
        layout_sld.addWidget(label1)
        layout_sld.addWidget(self.lcd_1)
        layout_sld.addWidget(self.sld)
        layout_sld.addWidget(self.lcd_2)
        layout_sld.addWidget(label2)
        layout_sld.setAlignment(QtCore.Qt.AlignCenter)

        layout_f = QVBoxLayout()
        layout_f.addLayout(layout)
        layout_f.addLayout(layout_alg)
        layout_f.addLayout(layout_sld)
        layout_f.addWidget(build_btn)
        self.widget_2.setLayout(layout_f)

    @staticmethod
    def init_lcd():
        """Создает лсд окно для коэффициентов альфа."""
        lcd = QLCDNumber()
        lcd.setSegmentStyle(2)
        lcd.setDigitCount(3)
        lcd.display(0.5)
        return lcd

    def init_slider_widget(self):
        """Создает слайдер для коэффициентов."""
        sld = QSlider()
        sld.setTickPosition(3)
        sld.setTickInterval(1)
        sld.setSingleStep(1)
        sld.setMinimum(0)
        sld.setMaximum(10)
        sld.setOrientation(QtCore.Qt.Horizontal)
        sld.setValue(5)
        sld.valueChanged.connect(self.display_alphas)
        return sld

    def display_alphas(self):
        """Меняет значения Альф на экране при дивжении слайдера."""
        self.alpha_1 = 1.0 - 0.1 * self.sld.value()
        self.alpha_2 = 1.0 - self.alpha_1
        self.lcd_1.display(self.alpha_1)
        self.lcd_2.display(self.alpha_2)

    def calculate_criterion(self, distributions):
        """Считает значение критериев для распределений."""
        rating_criterions = []
        assoc_criterions = []
        if self.alpha_1 == 0:
            for distr in distributions:
                assoc_criterions.append(self.calculate_assoc_criterion(distr))
            assoc_criterions = self.normalization_assoc_criterion(assoc_criterions)
            return assoc_criterions
        elif self.alpha_1 == 1:
            for distr in distributions:
                rating_criterions.append(self.calculate_rating_criterion(distr))
            rating_criterions = self.normalization_rating_criterion(rating_criterions)
            return rating_criterions
        else:
            for distr in distributions:
                assoc_criterions.append(self.calculate_assoc_criterion(distr))
                rating_criterions.append(self.calculate_rating_criterion(distr))
            assoc_criterions = self.normalization_assoc_criterion(assoc_criterions)
            rating_criterions = self.normalization_rating_criterion(rating_criterions)
            result = list(map(add, assoc_criterions, rating_criterions))
            result = self.normalization_by_both_crit(result)
            return result

    @staticmethod
    def normalization_by_both_crit(crit_list):
        """Нормализует на максимальный суммарный критерий."""
        norm = max(crit_list)
        print("Нормализация по 2м критериям\nнормировка на {}".format(norm))
        result = []
        for cr in crit_list:
            result.append(cr/norm)
        return result

    @staticmethod
    def normalization_assoc_criterion(assoc_criterion):
        """Нормирует все ассоциативные критерий на максимальный из полученных."""
        if len(assoc_criterion):
            m = max(assoc_criterion)
            print("Нормализация по критерию ассоциации\nнормировка на {}".format(m))

            return list([truediv(x, m) for x in assoc_criterion])
        else:
            return assoc_criterion

    @staticmethod
    def normalization_rating_criterion(rating_criterions):
        """Нормирует критерий рейтинга."""
        if len(rating_criterions):
            m = max(rating_criterions)
            print("Нормализация по критерию рейтинга\nнормировка на {}".format(m))
            print("Первый рейт критерий равен {}".format(rating_criterions[0]))

            return list([0 if x == 0 else truediv(x, m) for x in
                         rating_criterions])
        else:
            return rating_criterions

    def calculate_assoc_criterion(self, distr):
        """
        Считает значение критерия по ассоциациям.
        Число вхождений каждой ассоциации в каждой группе возводится в квадрат
        и суммируется с остальными.
        """
        assoc_set = set()
        for i in range(len(self.players_data)):
            assoc_set.add(self.players_data[i][2])
        assoc_set.discard('')

        assoc_criterion = 0

        for group in distr:
            cur_list = []
            # ассоциации в группе
            for el in group:
                cur_list.append(self.players_data[el-1][2])

            for assoc in assoc_set:
                result = cur_list.count(assoc)
                assoc_criterion += result ** 2

        return assoc_criterion

    def calculate_rating_criterion(self, distr):
        """Считает значение критерия по рейтингу."""
        list_of_average_rating_at_groups = []  # список средних рейтингов групп
        for group in distr:
            r = 0
            for player in group:
                r += self.players_data[player-1][1]
            list_of_average_rating_at_groups.append(r)

        average_rating = sum(list_of_average_rating_at_groups) / len(list_of_average_rating_at_groups)
        r_max = list_of_average_rating_at_groups[0]
        r_min = list_of_average_rating_at_groups[0]
        for r in list_of_average_rating_at_groups:
            if r > r_max:
                r_max = r
            elif r < r_min:
                r_min = r
        criterion = (r_max - r_min) / average_rating
        return criterion

    def build_result_table(self):
        """Действия при нажатии кнопки построить."""
        a = datetime.datetime.now()
        self.players_data = self.table.parse_table(self.settings)
        group_count = self.spinbox.value()
        # distributions = main(len(self.players_data), group_count)  # brute force
        # distributions = main(len(self.players_data), group_count, 2)  # snake
        distributions = main(len(self.players_data), group_count, 1, self.players_data)  # group ny group
        # distributions = main(len(self.players_data), group_count, deep=1, comb_range=5)
        criterion_list = self.calculate_criterion(distributions)
        self.result_window = ResultWindow(distributions, self.players_data, group_count,
                                          criterion_list)
        self.result_window.resize(460, 300)
        self.result_window.show()
        b = datetime.datetime.now()
        print(b-a, " время")
        print("критерий рейтинга {}".format(self.alpha_1))


class ResultWindow(QMainWindow):
    """Таблица результатов"""
    def __init__(self, distributions, player_data, group_count, criterion_list):
        super().__init__()
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
        self.resize(255, 255)
        self.position()

        self.init_result_data()

    def position(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_widget_3(self):
        """Создает виджет таблиц решений."""
        self.widget_3 = QWidget(self.central_widget)

        label = QLabel(self.settings.label_3_text, self.widget_3)
        label.setFont(self.settings.label_3_font)

        self.result_table = ResultTable()
        self.result_table.setParent(self.widget_3)

        layout = QVBoxLayout(self.widget_3)
        layout.addWidget(label, alignment=QtCore.Qt.AlignCenter)
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
