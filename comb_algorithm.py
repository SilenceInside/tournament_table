# -*- coding: utf-8 -*-


def main(m, k):
    """
    Создает список всех возможных комбинаций размещения
    m элементов на k групп без повторений. В каждой группе
    находится m/k элементов.
    :return [   [(), (), ()],
                [(), (), ()],
                [(), (), ()]
            ]
    """

    n = int(m / k)
    # Генерация списка для решений и первого решения
    distribution_of_elements = [[x for x in range(1, m+1)]]

    current_index = m - 1
    while current_index != 0:
        if ((n + current_index) % n) == 0:
            current_index -= 1
        else:
            if is_biggest(distribution_of_elements[-1], current_index, n, m):
                current_index -= 1
            else:
                distribution_of_elements.append(generate_distribution(
                distribution_of_elements[-1], current_index, n, m))
                current_index = m - n - 1
    distribution = []
    for i in distribution_of_elements:
        distribution.append(group_separation(i, n, k))
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
    rest = distribution_of_elements[current_index : m+1]
    rest.sort()
    index_f = rest.index(r)
    result.append(rest[index_f+1])
    rest.pop(index_f + 1)
    if ((current_index + 1) % n) != 0:
        elementAfter_f = []
        for i in range(1, (n-(current_index % n))):
            elementAfter_f.append(rest.pop(index_f+1))
        result.extend(elementAfter_f)
    result.extend(rest)
    return result


def group_separation(elements_distribution, n, k):
    """Отделяет группы элементов."""
    result = []
    for i in range(k):
        result.append(tuple(elements_distribution[n*i:n*i+n]))
    return result
