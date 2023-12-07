from openpyxl.worksheet.worksheet import Worksheet
from typing import List


def set_column_sizes_players_statistical_table(table_statistic: Worksheet) -> None:
    """
    Метод оформляет таблицу Player Statistic.
    Задает размер колонки, окрашивает нужные ячейки
    и выделяет границы полей ячейки
    :param table_statistic: Worksheet - таблица Player Statistic
    :return: None
    """
    table_statistic.column_dimensions['A'].width = 20
    list_of_columns: List[str] = ['E', 'F', 'G', 'I', 'J', 'K', 'L']

    for column in list_of_columns:
        table_statistic.column_dimensions[column].width = 15
