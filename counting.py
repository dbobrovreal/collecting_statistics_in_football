import json
from pandas import DataFrame, ExcelWriter
from typing import List, TypedDict, Dict
from decisive_action import decisive_action_players
from chemistry_players import formation_table_with_chemistry_of_players
from style import setting_style_for_the_tables
from data_collection import DataPlayer


def creating_table_with_results_of_players(statistics: Dict[str, Dict[str, DataPlayer]]) -> DataFrame:
    """
    Формируют таблицу с статистикой игроков за тур
    :param statistics:
    :return: DataFrame
    """
    name_player: List[str] = [name for name in statistics.keys()]
    position: List[str | None] = [statistics[name].get("position") for name in statistics.keys()]
    club: List[str | None] = [statistics[name].get("club") for name in statistics.keys()]
    saves: List[int | None] = [statistics[name]["statistic"].get("saves") for name in statistics.keys()]
    penalty_save: List[int | None] = [statistics[name]["statistic"].get("penalty_save")
                                      for name in statistics.keys()]
    assists_total: List[int | None] = [statistics[name]["statistic"].get("assists_total")
                                       for name in statistics.keys()]
    clean_sheets: List[int | None] = [statistics[name]["statistic"].get("clean_sheets")
                                      for name in statistics.keys()]

    interception: List[int | None] = [statistics[name]["statistic"].get("interceptions")
                                      for name in statistics.keys()]
    shots_blocked: List[int | None] = [statistics[name]["statistic"].get("shotsblocked")
                                       for name in statistics.keys()]
    tackles: List[int | None] = [statistics[name]["statistic"].get("tackleswon")
                                 for name in statistics.keys()]
    chances_created: List[int | None] = [statistics[name]["statistic"].get("chancescreated")
                                         for name in statistics.keys()]
    shots: List[int | None] = [statistics[name]["statistic"].get("shots") for name in statistics.keys()]
    gols: List[int | None] = [statistics[name]["statistic"].get("goals") for name in statistics.keys()]

    table_formation: DataFrame = DataFrame({
        "Name Player": name_player,
        "Position": position,
        "Club": club,
        "Saves": saves,
        "Penalty_save": penalty_save,
        "Assists-Total": assists_total,
        "CleanSheets": clean_sheets,
        "Goals": gols,
        "Interceptions": interception,
        "ShotsBlocked": shots_blocked,
        "TacklesWon": tackles,
        "ChancesCreated": chances_created,
        "Shots": shots
    })

    return table_formation


def formation_of_table_with_coaches(data_coach) -> DataFrame:
    """
    Метод формирует табличку с данными о тренерах
    :param data_coach:
    :return: DataFrame[Dict[str, str | str, int]]
    """
    name_manager = [name for name in data_coach.keys()]
    points = [data_coach[name].get('point') for name in data_coach.keys()]
    club_manager = [data_coach[name].get('club') for name in data_coach.keys()]
    resul_manager = [data_coach[name].get('result') for name in data_coach.keys()]

    table_manager: DataFrame = DataFrame({
        "Name Manager": name_manager,
        "Point": points,
        "Club": club_manager,
        "Result match": resul_manager,
    })

    return table_manager


def calculating_statistics(
        information_received: Dict[str, Dict[str, DataPlayer]],
        information_manager: Dict[str, Dict[str, int | str]],
        squad_game: Dict[str, List[Dict[str, str]]]
) -> None:
    """
    Метод для формирование итогового результа игры и запись в excel таблицу
    :param squad_game:
    :param information_manager:
    :param information_received:
    :return: None
    """
    table_with_players: DataFrame = creating_table_with_results_of_players(statistics=information_received)
    table_manager: DataFrame = formation_of_table_with_coaches(data_coach=information_manager)

    table_with_players.sort_values("Club", inplace=True, ascending=True)
    table_manager.sort_values("Club", inplace=True, ascending=True)
    table_decisive_action: DataFrame = decisive_action_players(statistic_player=information_received,
                                                               squad_game=squad_game)
    table_goal, table_dry_game, table_chemistry = formation_table_with_chemistry_of_players(
        statistic_player=information_received, squad_gamer=squad_game)

    table_sheets_name: Dict[str, DataFrame] = {
        "Player statistic": table_with_players,
        "Manager": table_manager,
        "Decisive action": table_decisive_action,
        "Goal": table_goal,
        "Clear sheet": table_dry_game,
        "Goal and Assist": table_chemistry
    }

    with open('responses.json', 'r', encoding='utf-8') as file:
        path_dir: str = json.load(file).get("path_dir_save")

    with ExcelWriter(f'{path_dir}\\game.xlsx', engine="openpyxl") as writer:
        for sheet_name in table_sheets_name.keys():
            table_sheets_name[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

    setting_style_for_the_tables(f'{path_dir}\\game.xlsx')
