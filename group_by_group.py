# -*- coding: utf-8 -*-
"""
Алгоритм разбиения элементов по группам равной величины.

Сначала подбираются заданное число групп по двум критериям:
1. рейтинг группы должен быть как можно ближе к среднему значению
(т.е. сумма всех рейтингов деленная на количество групп)
2. количество элементов от каждой ассоциации в группе не должно быть
больше, чем число элементов от данной ассоциации деленное на количество
групп, округленное вверх
Затем из оставшихся элементов строятся все возможные комбинации методом
полного перебора.
"""
from itertools import combinations as comb
from math import ceil


def main(m, k, appr_gr_count, player_list):
    """
    Строит наиболее оптимальные распределения элементов по группам.

    Сначала расчитываются appr_gr_count первых групп, таким образом чтобы
    средний рейтинг в полученных группах был наиболее близок к оптимальному.
    Затем лексикографически из оставшихся элементов строятся все возможные
    комбинации и дописываются к ранее полученным.
    :param m: число всех элементов
    :param k: число групп
    :param appr_gr_count: количество групп для предварительного рассчета
    :param player_dict: словарь с информацией о элементах
    """
    player_dict = dict()
    for i in range(len(player_list)):
        player_dict[i+1] = {'name': player_list[i][0], 'rating': player_list[i][1], 'assoc': player_list[i][2]}

    def calc_average_group_rating():
        """Вычисляет средний рейтинг групп."""
        result = 0
        for v in player_dict.values():
            result += v['rating']
        return result / k

    average_group_rating = calc_average_group_rating()
    assoc_count = dict()
    for v in player_dict.values():
        association = v['assoc']
        if assoc_count.get(association, False):
            assoc_count[association] += 1
        else:
            assoc_count[association] = 1

    n = int(m / k)
    free_values = list(range(1, m + 1))
    premade_groups = []

    def is_new_group_better_rating(n_group, b_group):
        s_ng = sum((player_dict[key]['rating'] for key in n_group))
        s_bg = sum((player_dict[key]['rating'] for key in b_group))
        if abs(s_ng - average_group_rating) <= abs(s_bg - average_group_rating):
            return True
        else:
            return False

    def is_association_count_normal(group, threshold):
        current_assoc_dict = dict()
        for num in group:
            a = player_dict[num]['assoc']
            if current_assoc_dict.get(a, False):
                current_assoc_dict[a] += 1
            else:
                current_assoc_dict[a] = 1
        for k, v in current_assoc_dict.items():
            if threshold[k] < v:
                return False
        return True

    for _ in range(appr_gr_count):

        threshold_assoc = dict()  # лимит участников от ассоциации в одной группе
        for k, v in assoc_count.items():
            threshold_assoc[k] = ceil(v / n)
        comb_list = list(comb(free_values, n))

        # проверка, что во взятой группе нормально распределены ассоциации
        while True:
            current_group = comb_list.pop(0)
            if is_association_count_normal(current_group, threshold_assoc):
                best_group = current_group
                break

        # сравниваем группу на близость значения рейтинга группы к среднему
        # и проверяем распределение ассоциаций
        for gr in comb_list:
            if is_new_group_better_rating(gr, best_group) and is_association_count_normal(gr, threshold_assoc):
                best_group = gr
        best_group = list(best_group)
        #  убираем элементы группы из общего списка
        #  уменьшаем количество представителей ассоциации в списке
        for element in best_group:
            free_values.remove(element)
            assoc_count[player_dict[element]['assoc']] -= 1

        premade_groups.append(best_group)

    combinations = comb_alg(len(free_values), int(len(free_values) / n),
                            free_values)
    for combination in combinations:
        for premade_group in reversed(premade_groups):
            combination.insert(0, premade_group)

    return combinations


def comb_alg(m, k, list_of_numbers=None):
    """
    Создает список всех размещений m элементов на k групп без повторений.

    В каждой группе находится m/k элементов.
    :param m: число всех элементов
    :param k: число групп
    :param list_of_numbers: список элементов для перебора
    :return [   [[], [], [],
                [[], [], []],
                [[], [], []]
            ]
    """
    # Генерация списка для решений и первого решения
    if list_of_numbers:
        distribution_of_elements = [list_of_numbers]
    else:
        distribution_of_elements = [[x for x in range(1, m + 1)]]
    m = len(distribution_of_elements[0])
    n = int(m / k)
    current_index = m - 1
    while current_index:
        if ((n + current_index) % n) == 0:
            current_index -= 1
        else:
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
    """Проверяет является элемент с индексом current_index наибольшим."""
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


def calculate_criterion(obj):
    """Вычисляет значение критерия по рейтингу."""
    average_rating_at_groups = []
    for group in obj:
        average_rating_at_groups.append(sum(group))
    average_rating = sum(average_rating_at_groups) / len(obj)
    r_max = average_rating_at_groups[0]
    r_min = average_rating_at_groups[0]
    for r in average_rating_at_groups:
        if r > r_max:
            r_max = r
        elif r < r_min:
            r_min = r
    criterion = (r_max - r_min) / average_rating
    return criterion, average_rating_at_groups


if __name__ == '__main__':
    data = {1: {'name': 'a', 'rating': 353, 'assoc': 'a'},
            2: {'name': 'b', 'rating': 350, 'assoc': 's'},
            3: {'name': 'c', 'rating': 348, 'assoc': 'sd'},
            4: {'name': 'd', 'rating': 340, 'assoc': 'a'},
            5: {'name': 'e', 'rating': 333, 'assoc': 'ds'},
            6: {'name': 'f', 'rating': 323, 'assoc': 'a'},
            7: {'name': 'g', 'rating': 300, 'assoc': 'dsad'},
            8: {'name': 'h', 'rating': 290, 'assoc': 'zxc'},
            9: {'name': 'j', 'rating': 287, 'assoc': 'zxc'}}

    for comb in main(9, 3, 1, data):
        print(comb)
