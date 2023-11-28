from pandas import DataFrame, ExcelWriter
from typing import List


def calculating_statistics(information_received: dict, information_manager) -> None:
    """
    Метод для получения подробной информации о статистике выбранных игроков в матче тура
    :param information_manager:
    :param information_received:
    :return: None
    """
    name_player: List[str] = [name for name in information_received.keys()]
    position: List[str] = [information_received[name].get("position") for name in information_received.keys()]
    club: List[str] = [information_received[name].get("club") for name in information_received.keys()]
    saves: List[int] = [information_received[name]["statistic"].get("saves") for name in information_received.keys()]
    assists_total: List[int] = [information_received[name]["statistic"].get("assists-total")
                                for name in information_received.keys()]
    clean_sheets: List[int] = [information_received[name]["statistic"].get("clean_sheets")
                               for name in information_received.keys()]

    interception: List[int] = [information_received[name]["statistic"].get("interceptions")
                               for name in information_received.keys()]
    shots_blocked: List[int] = [information_received[name]["statistic"].get("shotsblocked")
                                for name in information_received.keys()]
    tackles: List[int] = [information_received[name]["statistic"].get("tacklesWon")
                          for name in information_received.keys()]
    chances_created: List[int] = [information_received[name]["statistic"].get("chancescreated")
                                  for name in information_received.keys()]
    shots: List[int] = [information_received[name]["statistic"].get("shots") for name in information_received.keys()]
    gols: List[int] = [information_received[name]["statistic"].get("goals") for name in information_received.keys()]

    table_formation: DataFrame = DataFrame({
        "Name Player": name_player,
        "Position": position,
        "Club": club,
        "Saves": saves,
        "Assists-Total": assists_total,
        "CleanSheets": clean_sheets,
        "Goals": gols,
        "Interceptions": interception,
        "ShotsBlocked": shots_blocked,
        "TacklesWon": tackles,
        "ChancesCreated": chances_created,
        "Shots": shots
    })

    name_manager = [name for name in information_manager.keys()]
    points = [information_manager[name].get('point') for name in information_manager.keys()]
    club_manager = [information_manager[name].get('club') for name in information_manager.keys()]
    resul_manager = [information_manager[name].get('result') for name in information_manager.keys()]

    table_manager: DataFrame = DataFrame({
        "Name Manager": name_manager,
        "Point": points,
        "Club": club_manager,
        "Result match": resul_manager,
    })

    table_formation.sort_values("Club", inplace=True, ascending=True)
    table_manager.sort_values("Club", inplace=True, ascending=True)

    table_sheets_name = {
        "Player_statistic": table_formation,
        "Manager": table_manager
    }

    with ExcelWriter('game.xlsx', engine="openpyxl") as writer:
        for sheet_name in table_sheets_name.keys():
            table_sheets_name[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
