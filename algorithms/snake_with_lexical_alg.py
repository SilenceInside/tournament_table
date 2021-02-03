# -*- coding: utf-8 -*-
"""
Алгоритм разбиения элементов по группам равной величины комбинированным методом (змейка + полный перебор).
Сначала заданное число элементов в группах заполняется методом змейки. Затем их оставшихся элементов формируются
все возможные комбинации. Далее решения объединяются.

snake_plus_bruteforce(12, 3, 2)
[
    [(1, 6, 7, 8), (2, 5, 9, 10), (3, 4, 11, 12)]
    [(1, 6, 7, 8), (2, 5, 9, 11), (3, 4, 10, 12)]
    [(1, 6, 7, 8), (2, 5, 9, 12), (3, 4, 10, 11)]
    [(1, 6, 7, 9), (2, 5, 8, 10), (3, 4, 11, 12)]
    [(1, 6, 7, 9), (2, 5, 8, 11), (3, 4, 10, 12)]
    [(1, 6, 7, 9), (2, 5, 8, 12), (3, 4, 10, 11)]
    [(1, 6, 7, 10), (2, 5, 8, 9), (3, 4, 11, 12)]
    [(1, 6, 7, 10), (2, 5, 8, 11), (3, 4, 9, 12)]
    [(1, 6, 7, 10), (2, 5, 8, 12), (3, 4, 9, 11)]
    [(1, 6, 7, 11), (2, 5, 8, 9), (3, 4, 10, 12)]
    [(1, 6, 7, 11), (2, 5, 8, 10), (3, 4, 9, 12)]
    [(1, 6, 7, 11), (2, 5, 8, 12), (3, 4, 9, 10)]
    [(1, 6, 7, 12), (2, 5, 8, 9), (3, 4, 10, 11)]
    [(1, 6, 7, 12), (2, 5, 8, 10), (3, 4, 9, 11)]
    [(1, 6, 7, 12), (2, 5, 8, 11), (3, 4, 9, 10)]
]

snake_plus_bruteforce(12, 3, 5)
[
    [(1, 6, 7, 12), (2, 5, 8, 11), (3, 4, 9, 10)]
]
"""
from typing import List, Tuple
from .comb_algorithm import main as comb_alg


def snake_plus_bruteforce(m: int, k: int, num: int = 0) -> List[List[Tuple[int]]]:
    """
    Возвращает список распределений элементов по группам змейка+полный перебор.

    :param m: количество всех элементов
    :param k: количество групп
    :param num: количество элементов в каждой группе, которые надо распределить
    змейкой. num < k
    """
    if num <= 0:
        return comb_alg(m, k)

    if 0 < num < m/k:
        # num * k элементов распределяются змейкой
        number = num * k + 1  # первый элемент, после распределения змейкой
        items_for_brute_force = list(range(number, m + 1))
        result_list = comb_alg(m - num * k, k, items_for_brute_force)
        for distribution in result_list:
            for i in range(k):
                for j in range(num, 0, -1):
                    #  дописываем в начало каждой группы элементы методом змейки
                    element = j * k - i * (-1)**j + (1 - k) * (j % 2)
                    temp = list(distribution[i])
                    temp.insert(0, element)
                    distribution[i] = tuple(temp)
        return result_list
    else:
        result = [[] for _ in range(k)]
        for i in range(k):
            for j in range(int(m/k), 0, -1):
                #  дописываем в начало каждой группы элементы методом змейки
                element = j * k - i * (-1) ** j + (1 - k) * (j % 2)
                temp = result[i]
                temp.insert(0, element)
            result[i] = tuple(temp)
        return [result]


if __name__ == '__main__':
    for s in snake_plus_bruteforce(12, 3, 5):
        print(s)
