# -*- coding: utf-8 -*-
import csv

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QDesktopWidget,
                             QFileDialog, QLabel, QMainWindow,
                             QPushButton, QWidget,
                             QHBoxLayout, QVBoxLayout, QTableWidgetItem,
                             QAction, qApp)

from settings import Settings
from widgets.tables import ParticipantTable
from widgets.algorithm_manager import AlgorithmManagerWidget


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

        file_menu = self.menubar.addMenu('Menu')

        action_exit = QAction('Exit', self)
        action_exit.setShortcut('Ctrl+Q')
        action_exit.triggered.connect(qApp.quit)

        action_load = QAction('Load', self)
        action_load.setShortcut('Ctrl+L')
        action_load.triggered.connect(self.load_csv)

        action_save = QAction('Save', self)
        action_save.setShortcut('Ctrl+S')
        action_save.triggered.connect(self.save_csv)

        file_menu.addAction(action_load)
        file_menu.addAction(action_save)
        file_menu.addAction(action_exit)

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
        hbox.addWidget(label, alignment=QtCore.Qt.AlignCenter)

        hbox_2 = QHBoxLayout()
        hbox_2.addWidget(add_btn, alignment=QtCore.Qt.AlignRight)
        hbox_2.addWidget(del_btn, alignment=QtCore.Qt.AlignRight)

        layout = QVBoxLayout()
        layout.addLayout(hbox)
        layout.addWidget(self.table)
        layout.addLayout(hbox_2)

        self.widget_1.setLayout(layout)

    def init_parameter_selection_widget(self):
        """Создает виджет выбора количества групп."""
        self.widget_2 = AlgorithmManagerWidget(self)

    @property
    def players_count(self):
        self.players_data = self.table.parse_table(self.settings)
        return len(self.players_data)
