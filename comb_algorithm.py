# -*- coding: utf-8 -*-
from typing import List, Tuple


def main(m: int, k: int, items_list: List[int] = None) -> List[List[Tuple[int]]]:
    """
    Создает список всех возможных комбинаций размещения
    m элементов на k групп без повторений. В каждой группе
    находится m/k элементов.
    :param m: количество элементов
    :param k: количество групп, на которое нужно разделить m
    :param items_list: список чисел, которые будут использоваться вместо
    значений по-умолчанию от 1 до m
    :return [   [(), (), ()],
                [(), (), ()],
                [(), (), ()]
            ]
    """

    n = int(m / k) # количество элементов в каждой группе
    # Генерация списка для решений и первого решения
    if items_list and len(items_list) == m:
        first_distribution = sorted(list(items_list))
    else:
        first_distribution = [x for x in range(1, m+1)]

    distributions_list = [first_distribution]

    current_index = m - 1
    while current_index != 0:
        if (n + current_index) % n == 0:
            current_index -= 1
        else:
            if is_biggest(distributions_list[-1], current_index, n, m):
                current_index -= 1
            else:
                distributions_list.append(generate_distribution(
                    distributions_list[-1], current_index, n, m))
                current_index = m - n - 1
    distribution = []
    for i in distributions_list:
        distribution.append(group_separation(i, n, k))
    return distribution


def is_biggest(items_distribution: List[int],
               current_index: int,
               n: int,
               m: int = 0) -> bool:
    """
    Проверяет является элемент с индексом current_index наибольшим
    из последующих элементов.
    :param items_distribution: список натуральных чисел
    :param current_index: индекс проверяемого элемента в в items_distribution
    :param n: количество элементов в одной группе
    :param m: количество элементов в списке
    """

    group_number = (current_index // n) + 1
    last_part = items_distribution[(group_number * n)::]
    compared_element = items_distribution[current_index]
    for i in last_part:
        if compared_element < i:
            return False
    return True


def generate_distribution(items_distribution: List[int],
                          current_index: int,
                          n: int,
                          m: int) -> List[int]:
    """
    Генерирует новое распределение элементов.
    Оно строится на основе передаваемого распределения и индекса элемента,
    который необходимо изменить.
    :param items_distribution: распределение элементов
    :param current_index: индекс элемента в items_distribution, с которого
    строится новое распределение
    :param n: количество элементов в одной группе
    :param m: количество элементов в списке
    """
    item_for_change = items_distribution[current_index]
    # элементы до current_index сохраняют порядок
    result = items_distribution[0:current_index]
    rest = items_distribution[current_index: m + 1]
    rest.sort()

    # на место элемента current_index и до тех пор пока не заполним текущую
    # группу вставляем следующие за ним в порядке возрастания элементы из rest
    rest_current_index = rest.index(item_for_change)

    for _ in range(n - current_index % n):
        result.append(rest.pop(rest_current_index + 1))

    # оставшиеся элементы дописываем в конец
    result.extend(rest)
    return result


def group_separation(items_distribution: List[int], n: int, k: int) -> List[Tuple[int]]:
    """
    Отделяет группы элементов по n элемементов на k групп.
    :param items_distribution: Список элементов
    :param n: количество элементов в одной группе
    :param k: количество групп
    :return: items_distribution разделенный на k кортежей
    """
    result = []
    for i in range(k):
        result.append(tuple(items_distribution[n * i:n * i + n]))
    return result
