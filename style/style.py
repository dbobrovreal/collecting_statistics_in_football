import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl import Workbook
from style.example import table_layout_example
from style.goal_and_assist import table_layout_goal_and_assist
from style.clean_sheet import table_layout_clear_sheet
from style.player_statistic import set_column_sizes_players_statistical_table
from style.manager import design_of_manager_table
from style.decisive_action import table_layout_decisive_action
from style.layout_goal import table_layout_goal
from style.table_squad import creating_table_with_commands


def setting_style_for_the_tables(path_file: str) -> None:
    """
    Метод оформляет стили для каждой таблице excel с итоговой информацией
    :param path_file: str - путь до файла с итоговыми результатоми
    :return: None
    """
    file_tables: Workbook = openpyxl.load_workbook(path_file)

    table_with_commands: Worksheet = file_tables['Табличка']
    creating_table_with_commands(table_squad=table_with_commands)

    player_statistics: Worksheet = file_tables['Player statistic']
    set_column_sizes_players_statistical_table(table_statistic=player_statistics)

    manager_statistic: Worksheet = file_tables['Manager']
    design_of_manager_table(table_manager=manager_statistic)

    decisive_action: Worksheet = file_tables['Decisive action']
    table_layout_decisive_action(table_decisive_action=decisive_action)

    goal: Worksheet = file_tables['Goal']
    table_layout_goal(table_goal=goal)

    clear_sheet: Worksheet = file_tables['Clean sheet']
    table_layout_clear_sheet(table_clear_sheet=clear_sheet)

    goal_and_assist: Worksheet = file_tables['Goal and Assist']
    table_layout_goal_and_assist(table_goal_and_assist=goal_and_assist)

    example: Worksheet = file_tables['Example']
    table_layout_example(table_example=example)

    file_tables.save(path_file)
