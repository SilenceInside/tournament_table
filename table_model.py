from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget


class ParticipantTable(QTableWidget):
    """Таблица для списка участников."""
    def __init__(self, settings):
        super().__init__()
        self.setRowCount(settings.row_count)
        self.setColumnCount(settings.col_count)
        self.set_columns_width(settings)
        self.setHorizontalHeaderLabels(settings.horizontal_labels)
        self.horizontalHeader().setStretchLastSection(True)
        self.fill_table()

    def set_columns_width(self, settings):
        """Задает ширину первых 3 колонок."""
        for i, width in enumerate(settings.min_col_width):
            self.setColumnWidth(i, width)

    def fill_table(self):
        """Заполняет инициализированные строки пробелами."""
        for n in range(self.columnCount()):
            for m in range(self.rowCount()):
                item = QTableWidgetItem(" ")
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(m, n, item)

    def add_row(self):
        """Добавляет пустую строку в конце таблицы."""
        self.insertRow(self.rowCount())
        for i in range(self.columnCount()):
            item = QTableWidgetItem("")
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(self.rowCount()-1, i, item)

    def add_player(self, player):
        """Добавляет участника в таблицу."""
        self.add_row()
        index_for_row = self.rowCount() - 1
        for i, atr in enumerate(player):
            item = QTableWidgetItem(str(atr))
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(index_for_row, i+1, item)

    def del_selected_row(self):
        """Удаляет строки выделенного диапазона."""
        selected_items = self.selectedItems()
        # Условие, чтобы не закрылось приложение, когда ничего не выбрано
        if not selected_items:
            return 0
        upper_row = selected_items[0].row()
        bottom_row = selected_items[-1].row()
        for _ in range(upper_row, bottom_row + 1):
            self.removeRow(upper_row)

    def parse_table(self, settings):
        """Парсит данные из таблицы."""
        data = []
        col_nums = [settings.horizontal_labels.index('Name'),
                    settings.horizontal_labels.index('Rating'),
                    settings.horizontal_labels.index('Association')]

        for i in range(self.rowCount()):
            current_player = list()
            current_player.append(self.get_name(i, col_nums[0]))
            current_player.append(int(self.get_rating(i, col_nums[1])))
            current_player.append(self.get_association(i, col_nums[2]))
            data.append(current_player)

        return data

    def get_name(self, i, j):
        """Возвращает ФИО."""
        return self.item(i, j).text()

    def get_rating(self, i, j):
        """Возвращает Рейтинг."""
        return self.item(i, j).text()

    def get_association(self, i, j):
        """Возвращает Ассоциацию."""
        return self.item(i, j).text()

    def parse_for_csv(self):
        """Полностью парсит таблицу для записи в файл."""
        content = []
        for r in range(self.rowCount()):
            row = []
            for c in range(self.columnCount()):
                row.append(self.item(r, c).text())
            content.append(row)
        return content


class ResultTable(QTableWidget):
    """Таблица результатов."""
    def __init__(self):
        super().__init__()

    def display_groups(self, distr, players_list):
        """Выводит группы в таблицу."""
        self.clear()
        self.setRowCount(len(distr[0])+1)
        self.setColumnCount(len(distr))
        self.init_header(len(distr))
        self.insert_players(distr, players_list)

    def init_header(self, num):
        """Создает заголовки с номером для каждой группы."""
        headers = ("Group {}".format(i+1) for i in range(num))
        self.setHorizontalHeaderLabels(headers)

    def insert_players(self, distr, players_list):
        """Вставляет фамилии участников в таблицу."""
        for g, group in enumerate(distr):
            sum_rating = 0
            for p, player in enumerate(group):
                itm = "{name}, {association}".format(name=players_list[player-1][0], association=players_list[player-1][2])
                item = QTableWidgetItem(itm)
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(p, g, item)
                sum_rating += players_list[player-1][1]
            item = QTableWidgetItem(str(sum_rating))
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(p+1, g, item)
