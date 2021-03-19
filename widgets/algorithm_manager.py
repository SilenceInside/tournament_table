from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSpinBox, QLabel,\
    QComboBox, QWidget, QPushButton

from .lcd import LCD
from .slider import Slider
from settings import Settings
from algorithms import comb_algorithm, snake_with_lexical_alg, \
    group_by_group, random_search
from result_window import ResultWindow
from criterion_calculator import CriteriaCalculator


class AlgorithmManagerWidget(QWidget):
    CHOICES = ['Brute force', 'Snake', 'Snake with brute force',
               'Group by group', 'Random search']

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = Settings()

        # group count widget
        label = QLabel(self.settings.label_2_text, self)
        self.group_count_spinbox = QSpinBox(self)
        self.group_count_spinbox.setRange(2, 20)

        group_count_layout = QHBoxLayout()
        group_count_layout.addWidget(label)
        group_count_layout.addWidget(self.group_count_spinbox)
        group_count_layout.setAlignment(QtCore.Qt.AlignCenter)

        # algorithm choice widget
        alg_label = QLabel(self.settings.label_alg_text, self)
        self.algorithm_combobox = QComboBox(self)
        self.algorithm_combobox.addItems(self.CHOICES)
        self.algorithm_combobox.currentIndexChanged.connect(
            self.change_view_options)

        algorithm_choice_layout = QHBoxLayout()
        algorithm_choice_layout.addWidget(alg_label)
        algorithm_choice_layout.addWidget(self.algorithm_combobox)
        algorithm_choice_layout.setAlignment(QtCore.Qt.AlignCenter)

        # premade group options
        label_premade_group_count = QLabel(
            self.settings.label_premade_group_count)
        self.premade_group_count = QSpinBox(self)
        self.premade_group_count.setRange(1, 10)
        self.premade_group_count.setValue(1)
        premade_group_layout = QHBoxLayout()
        premade_group_layout.addWidget(label_premade_group_count)
        premade_group_layout.addWidget(self.premade_group_count)
        premade_group_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.premade_widget = QWidget(self)
        self.premade_widget.setLayout(premade_group_layout)

        # snake brute force options
        label_snake_brute_force = QLabel(
            self.settings.label_snake_brute_force)
        self.snake_items_count = QSpinBox(self)
        self.snake_items_count.setRange(1, 10)
        self.snake_items_count.setValue(1)
        snake_brute_force_layout = QHBoxLayout()
        snake_brute_force_layout.addWidget(label_snake_brute_force)
        snake_brute_force_layout.addWidget(self.snake_items_count)
        snake_brute_force_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.snake_brute_force_widget = QWidget(self)
        self.snake_brute_force_widget.setLayout(snake_brute_force_layout)

        # random search options
        label_random_1 = QLabel(self.settings.label_random_search_1)
        self.random_search_deep = QSpinBox(self)
        self.random_search_deep.setRange(1, 10)
        self.random_search_deep.setValue(1)

        label_random_2 = QLabel(self.settings.label_random_search_2)
        self.random_search_range = QSpinBox(self)
        self.random_search_range.setRange(1, 10)
        self.random_search_range.setValue(2)

        random_search_layout = QHBoxLayout()
        random_search_layout.addWidget(label_random_1)
        random_search_layout.addWidget(self.random_search_deep)
        random_search_layout.addWidget(label_random_2)
        random_search_layout.addWidget(self.random_search_range)
        random_search_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.random_searh_widget = QWidget(self)
        self.random_searh_widget.setLayout(random_search_layout)

        # slider
        self.slider = Slider()
        self.slider.valueChanged.connect(self.change_lcd_values)
        label1 = QLabel(self.settings.label_5_text)
        label2 = QLabel(self.settings.label_6_text)
        self.lcd_1 = LCD()
        self.lcd_2 = LCD()

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(label1)
        slider_layout.addWidget(self.lcd_1)
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.lcd_2)
        slider_layout.addWidget(label2)

        # build button
        build_btn = QPushButton(self.settings.build_btn_text, self)
        build_btn.clicked.connect(self.show_result)

        # general layout
        vertical_layout = QVBoxLayout(self)
        vertical_layout.addLayout(group_count_layout)
        vertical_layout.addLayout(algorithm_choice_layout)
        vertical_layout.addWidget(self.premade_widget)
        vertical_layout.addWidget(self.snake_brute_force_widget)
        vertical_layout.addWidget(self.random_searh_widget)
        vertical_layout.addLayout(slider_layout)
        vertical_layout.addWidget(build_btn)

        self.hide_all_options()

    def change_lcd_values(self):
        """Меняет значения на LCD при движении слайдера."""
        self.lcd_1.display(1.0 - 0.1 * self.slider.value())
        self.lcd_2.display(1.0 - self.lcd_1.value())

    def hide_all_options(self):
        self.premade_widget.hide()
        self.snake_brute_force_widget.hide()
        self.random_searh_widget.hide()

    def change_view_options(self):
        algorithm_index = self.algorithm_combobox.currentIndex()

        self.hide_all_options()
        if algorithm_index == 2:
            self.snake_brute_force_widget.show()
        elif algorithm_index == 3:
            self.premade_widget.show()
        elif algorithm_index == 4:
            self.random_searh_widget.show()

    @property
    def group_count(self):
        return self.group_count_spinbox.value()

    @property
    def players_count(self):
        return self.parent().parent().players_count

    def calculate_distribution(self):
        algorithm_index = self.algorithm_combobox.currentIndex()

        if algorithm_index == 0:
            return comb_algorithm.main(self.players_count, self.group_count)

        elif algorithm_index == 1:
            num = int(self.players_count / self.group_count)
            return snake_with_lexical_alg.snake_plus_bruteforce(
                self.players_count, self.group_count, num)

        elif algorithm_index == 2:
            num = self.snake_items_count.value()
            if num > int(self.players_count / self.group_count):
                num = int(self.players_count / self.group_count)
            return snake_with_lexical_alg.snake_plus_bruteforce(
                self.players_count, self.group_count, num)

        elif algorithm_index == 3:
            return group_by_group.main(self.players_count,
                                self.group_count,
                                self.premade_group_count.value(),
                                self.get_players_data())
        else:
            return random_search.main(self.players_count,
                               self.group_count,
                               deep=self.random_search_deep.value(),
                               comb_range=self.random_search_range.value())

    def show_result(self):
        result_distributions = self.calculate_distribution()
        players_data = self.get_players_data()
        criteria_list = CriteriaCalculator.calculate(
            distributions=result_distributions,
            players_data=players_data,
            rating_coef=self.lcd_1.value(),
            assoc_coef=self.lcd_2.value()
        )
        result = ResultWindow(result_distributions,
                              players_data,
                              self.group_count,
                              criteria_list,
                              self.parent())
        result.show()
        result.center()

    def get_players_data(self):
        return self.parent().parent().table.parse_table(self.settings)
