# -*- coding: utf-8 -*-
"""
Алгоритм разбиения элементов по группам равной величины комбинированным методом (змейка + полный перебор).
Сначала заданное число элементов в группах заполняется методом змейки. Затем их оставшихся элементов формируются
все возможные комбинации. Далее решения объединяются.
"""


def snake_plus_bruteforce(m, k, num=0):
    """
    Возвращает список распределений элементов по группам змейка+полный перебор.

    :param m: количество всех элементов
    :param k: количество групп
    :param num: количество элементов в каждой группе, которые надо распределить
    змейкой
    """
    if num == 0:
        return main(m, k)

    if num > 0 and num < m/k:
        number = num * k + 1  # num * k элементов распределяются змейкой
        result_list = main(m - number + 1, k, start_num=number)
        for distribution in result_list:
            for i in range(k):
                for j in range(num, 0, -1):
                    #  дописываем в начало каждой группы элементы методом змейки
                    element = j * k - i * (-1)**j + (1 - k) * (j % 2)
                    distribution[i].insert(0, element)
        return result_list


def main(m, k, start_num=1):
    """
    Создает список всех возможных разбиений m элементов на k групп.

    В каждой группе находится m/k элементов.
    :param num: первое число в списке
    :return [   [[], [], []],
                [[], [], []],
                [[], [], []]
            ]
    """
    n = int(m / k)
    # Генерация списка для решений и первого решения
    distribution_of_elements = [[x for x in range(start_num, m + start_num)]]

    current_index = m - 1
    while current_index + 1:
        if is_biggest(distribution_of_elements[-1], current_index, n, m):
            current_index -= 1
        else:
            distribution_of_elements.append(generate_distribution(
                distribution_of_elements[-1], current_index, n, m))
            current_index = m - n - 1

    distribution = [group_separation(i, n, k)
                    for i in distribution_of_elements]
    return distribution


def is_biggest(distribution_of_elements, current_index, n, m):
    """
    Проверяет является элемент с индексом current_index наибольшим
    из последующих элементов.
    """
    group_number = (current_index // n) + 1
    last_part = distribution_of_elements[(group_number * n): (m + 1)]
    new_R = distribution_of_elements[current_index]
    for i in last_part:
        if new_R < i:
            return False
    return True


def generate_distribution(distribution_of_elements, current_index, n, m):
    """Генерирует новое распределение элементов."""
    r = distribution_of_elements[current_index]
    result = distribution_of_elements[0:current_index]
    rest = distribution_of_elements[current_index: m + 1]
    rest.sort()

    index_f = rest.index(r)
    result.append(rest.pop(index_f + 1))

    if ((current_index + 1) % n):

        elementAfter_f = []
        for i in range(1, (n - (current_index % n))):
            elementAfter_f.append(rest.pop(index_f + 1))
        result.extend(elementAfter_f)

    result.extend(rest)
    return result


def group_separation(elements_distribution, n, k):
    """Отделяет группы элементов."""
    result = []
    for i in range(k):
        result.append(list(elements_distribution[n * i:n * i + n]))
    return result


if __name__ == '__main__':
    for s in snake_plus_bruteforce(16, 4, 2):
        print(s)
