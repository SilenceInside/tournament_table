# -*- coding: utf-8 -*-
from itertools import product
import math


def comb_by_number(m: int, k: int, n: int, num: int) -> list:
    """
    Вычисляет распределение с номером num.

    :param m: количество элементов
    :param k: количество групп
    :param n: m / k
    :param num: номер распределения
    :return: распределения с заданным номером num
    """
    distribution = [i for i in range(1, m + 1)]  # начальное распределение

    def count_combinations(j):

        result = 1
        for i in range(1, k - j + 1):
            result *= math.factorial(n * i - 1) / math.factorial(n - 1) / math.factorial(n * (i - 1))
        return result

    def shift_distribution(j, y, distribution):
        """

        :param j: номер группы
        :param y: количество сдвигов
        :param distribution: распределение, которое нужно сдвинуть
        :return: новое распределение
        """
        first_part = distribution[:((j - 1) * n)]  # распределение до группы j
        group_j = distribution[((j - 1) * n): j * n]  # группа j
        rest_part = distribution[j * n:]  # остаток для перебора
        rest_part.sort()

        for _ in range(y):
            for a, b in product(group_j[::-1], rest_part):
                if a < b:
                    # меняем местами эти элементы
                    copy_group_j = group_j[:]
                    copy_rest_part = rest_part[:]
                    copy_group_j[group_j.index(a)] = b
                    copy_rest_part[rest_part.index(b)] = a

                    rest = copy_group_j[(group_j.index(a) + 1):] + copy_rest_part
                    rest.sort()
                    for i in range(1, len(group_j) - group_j.index(a)):
                        for kr in range(len(rest)):
                            if rest[kr] > a:
                                copy_group_j[group_j.index(a) + i] = rest.pop(kr)
                                break

                    # переписываем новые данные
                    rest_part = rest
                    group_j = copy_group_j
                    break

        return first_part + group_j + rest_part

    def finish_distribution(distribution, k, n):
        result = []
        for i in range(k):
            result.append(tuple(distribution[i * n: (i + 1) * n]))
        return result

    x = num - 1
    for j in range(1, k):
        comb_count = count_combinations(j)
        y = math.floor(x / comb_count)  # целая часть от деления
        x = x % comb_count  # остаток от деления
        if y == 0: continue
        distribution = shift_distribution(j, y, distribution)
        if x == 0: break

    distribution = finish_distribution(distribution, k, n)
    return distribution


def calculate_defined_area(m: int, k: int, number: int,
                           total_comb: int, comb_range: int=0):
    """
    Расчитывает комбинации с номера number-range до number+range
    :param m: количество элементов
    :param k: количество групп для разбиения всех элементов
    :param number: номер комбинации
    :param total_comb: общее число комбинаций
    :param comb_range: радиус поиска вокруг номера комбинации
    :return: список комбинаций
    """
    start = number - comb_range
    end = number + comb_range
    if (number - comb_range) < 0:
        start = 1
    if (number + comb_range) > total_comb:
        end = total_comb

    n = int(m / k)
    return tuple(comb_by_number(m, k, n, _) for _ in range(start, end + 1))


def main(m: int, k: int, deep: int=1, comb_range: int=0) -> tuple:
    """
    Расчитывает номера комбинаций, области вокруг которых нужно прссмотреть
    :param m: количество элементов
    :param k: количество групп для разбиения всех элементов
    :param deep: номер группы, изменения которой необходимо отслеживать
    :param comb_range: радиус вычисляемых номеров от N-comb_range до N+comb_range
    :return: кортеж всех интересующих точек
    """
    result = ()

    def count_combinations(j: int=1) -> int:
        """
        Вычисляет количество комбинаций между сменой элементов в группе j.
        Если j=0, тогда вычисляется полное число комбинаций.
        """
        n = int(m / k)
        res = 1
        for i in range(1, k - j + 1):
            res *= (math.factorial(n * i - 1) / math.factorial(n - 1) /
                    math.factorial(n * (i - 1)))
        return int(res)

    #  Цикл для выбранных номеров комбинаций
    total_comb_count = count_combinations(0)
    #  j - номер группы для которой берутся итерации
    start_comb_number = count_combinations(deep)
    for num in range(start_comb_number, total_comb_count + 1, start_comb_number):
        #  comb_range - радиус области от текущего номера
        result += calculate_defined_area(m, k, num, total_comb_count,
                                         comb_range=comb_range)

    return result
