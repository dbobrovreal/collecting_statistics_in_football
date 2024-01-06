from openpyxl.worksheet.worksheet import Worksheet
from typing import List


def creating_table_with_commands(table_squad: Worksheet) -> None:
    """
    Метод оформляет таблицу Табличка.
    Задает размер колонки
    :param table_squad: Worksheet - таблица Табличка
    :return: None
    """
    list_of_columns: List[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    for column in list_of_columns:
        table_squad.column_dimensions[column].width = 25

    table_squad.column_dimensions['H'].width = 30
    table_squad.column_dimensions['I'].width = 20
