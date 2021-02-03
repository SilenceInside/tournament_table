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

from .comb_algorithm import main as comb_alg


def main(m: int, k: int, premade_group_count: int, player_data):
    """
    Строит наиболее оптимальные распределения элементов по группам.

    Сначала расчитываются appr_gr_count первых групп, таким образом чтобы
    средний рейтинг в полученных группах был наиболее близок к оптимальному.
    Затем лексикографически из оставшихся элементов строятся все возможные
    комбинации и дописываются к ранее полученным.
    :param m: число всех элементов
    :param k: число групп
    :param premade_group_count: количество групп для предварительного рассчета
    :param player_data: словарь или список с информацией о элементах
    """
    if type(player_data) == dict:
        player_dict = player_data
    else:
        player_dict = dict()
        for i in range(len(player_data)):
            player_dict[i+1] = {'name': player_data[i][0], 'rating': player_data[i][1], 'assoc': player_data[i][2]}

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

    for _ in range(premade_group_count):

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
