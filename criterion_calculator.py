from operator import add, truediv
from typing import Any, List, Sequence, Tuple


class CriteriaCalculator:
    @staticmethod
    def calculate(distributions: List[List[Tuple[int]]],
                  players_data: List[List[Any]],
                  rating_coef: float = 1,
                  assoc_coef: float = 0) -> List[float]:
        """
        Расчитывает значение целевой функции для каждого распроедения.
        :param distributions: список распределений участников, где участник
        представлен натуральным числом
        :param players_data: список данных об участниках, каждый участник представлен
        как [name: str, rating: int, association: str]
        :param rating_coef: значение весового коэффициента критерия, отвечающего
        за равномерность распределения по рейтингу 0 <= rating_coef <= 1
        :param assoc_coef: значение весового коэффициента критерия, отвечающего
        за равномерность распределения по ассоциациям 0 <= assoc_coef <= 1
        rating_coef + assoc_coef = 1
        :return: список значений целевой функции для каждого распределения
        """
        result_criteria = []

        if rating_coef == 1:
            for distribution in distributions:
                result_criteria.append(CriteriaCalculator.calculate_rating_criteria(distribution, players_data))
        elif assoc_coef == 1:
            for distribution in distributions:
                result_criteria.append(CriteriaCalculator.calculate_association_criteria(distribution, players_data))
        else:
            association_criteria = []
            rating_criteria = []
            for distribution in distributions:
                temp = CriteriaCalculator.calculate_association_criteria(distribution, players_data)
                association_criteria.append(temp)

                temp = CriteriaCalculator.calculate_rating_criteria(distribution, players_data)
                rating_criteria.append(temp)
            association_criteria = CriteriaCalculator.normalize_list_values(association_criteria)
            rating_criteria = CriteriaCalculator.normalize_list_values(rating_criteria)

            result_criteria = list(map(add, association_criteria, rating_criteria))
        
        return CriteriaCalculator.normalize_list_values(result_criteria)

    @staticmethod
    def calculate_rating_criteria(distribution: List[Tuple[int]],
                                  players_data: List[List[Any]]) -> float:
        """Расчитывает не нормированное значение критерия распределения по рейтингу.
        Для каждой группы рассчитывается суммарное значение рейтинга её участников.
        Затем от наибольшего значения отнимается наименьшее и результат делится на
        среднее значение сумарных рейтинов для групп.
        :param distribution: единичное распределение участников, где участник
        представлен натуральным числом
        :param players_data: список данных об участниках, каждый участник представлен
        как [name: str, rating: int, association: str]
        :return: float
        """
        # Для каждой группы считается суммарный рейтинг участников
        sum_rating_at_groups = []
        for group in distribution:
            sum_rating = 0
            for player in group:
                sum_rating += players_data[player-1][1]
            sum_rating_at_groups.append(sum_rating)

        average_rating = sum(sum_rating_at_groups) / len(sum_rating_at_groups)
        return (max(sum_rating_at_groups) - min(sum_rating_at_groups)) / average_rating

    @staticmethod
    def calculate_association_criteria(distribution: List[Tuple[int]],
                                       players_data: List[List[Any]]) -> float:
        """Рассчитывает не нормированные значения критерия распределения по ассоциациям.
        В каждой группе для каждой ассоциации подсчитывается число ее представителей и
        возводится в квадрат. Результатом является сумма всех этих значений.
        :param distribution: единичное распределение участников, где участник
        представлен натуральным числом
        :param players_data: список данных об участниках, каждый участник представлен
        как [name: str, rating: int, association: str]
        :return: float
        """
        unique_association = set()
        for player in players_data:
            unique_association.add(player[2])
        unique_association.discard('')

        result = 0

        for group in distribution:
            associations_at_current_group = []

            for player in group:
                associations_at_current_group.append(players_data[player-1][2])

            for association in unique_association:
                result += associations_at_current_group.count(association) ** 2
        return result
    
    @staticmethod
    def normalize_list_values(values_list: List[float]) -> List[float]:
        norm_value = max(values_list)
        return list([truediv(x, norm_value) for x in values_list])
