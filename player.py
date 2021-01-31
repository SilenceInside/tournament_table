# -*- coding: utf-8 -*-


class Player:
    """Модель игрока."""

    def __init__(self, name, rating, association='', birthday='',
                 couch='', other=''):
        self.name = str(name)
        self.rating = str(rating)
        self.association = str(association)
        self.birthday = str(birthday)
        self.couch = str(couch)
        self.other = str(other)

    def __str__(self):
        if not self.association:
            return self.name + ' with rating ' + self.rating
        else:
            return (self.name + ' with rating ' + self.rating +
                    ' from ' + self.association)

    def get_attrs(self):
        """Возвращает список всех аргументов для таблицы."""
        return [self.name, self.rating, self.association,
                self.birthday, self.couch, self.other]
