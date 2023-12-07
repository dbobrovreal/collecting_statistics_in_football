import re
from re import Match
import unidecode
from typing import List, Dict, TypedDict
from pandas import DataFrame


class StatisticPlayer(TypedDict):
    saves: int
    penalty_save: int
    assists_total: int
    clean_sheets: int
    goals: int
    interceptions: int
    shotsblocked: int
    tackleswon: int
    chancescreated: int
    shots: int


class DataPlayer(StatisticPlayer):
    position: str
    club: str
    statistic: StatisticPlayer


def decoding_words(word) -> str:
    return unidecode.unidecode(word)


def getting_detailed_statistics(
    statistic: Dict[str, int],
    missed_balls: int,
    minutes_missed: list
) -> Dict[str, int]:
    """
    Метод для получения точной статистики игроков
    :param minutes_missed: list - Время когда команда пропустила мяч
    :param missed_balls: int - пропущенные мячи
    :param statistic:
    :return: dict
    """
    saves: int = statistic.get('saves', 0)
    penalty_save: int = statistic.get('penaltySave', 0)
    assists_total: int = statistic.get('goalAssist', 0)
    interception: int = statistic.get('interceptionWon', 0)
    shots_blocked: int = statistic.get("blockedScoringAttempt", 0)
    tackles: int = statistic.get("totalTackle", 0)
    chances_created: int = statistic.get("keyPass", 0)
    shot_off: int = statistic.get("shotOffTarget", 0)
    shot_on: int = statistic.get("onTargetScoringAttempt", 0)
    shot_blocked: int = statistic.get("blockedScoringAttempt", 0)
    shots: int = shot_on + shot_off + shot_blocked
    gols: int = statistic.get("goals", 0)
    minute: int = statistic.get('minutesPlayed', 0)
    if minute >= 60 and missed_balls == 0:
        clean_sheets = 1
    elif 60 <= minute < minutes_missed[0]:
        clean_sheets = 1
    else:
        clean_sheets = 0

    processed_statistics: Dict[str, int] = {
        "saves": saves,
        "penalty_save": penalty_save,
        "assists_total": assists_total,
        "clean_sheets": clean_sheets,
        "goals": gols,
        "interceptions": interception,
        "shotsblocked": shots_blocked,
        "tackleswon": tackles,
        "chancescreated": chances_created,
        "shots": shots,
    }

    return processed_statistics


def filling_in_information_on_managers(
    info_manager: dict,
    info_by_table: DataFrame,
    row: int,
    result: dict,
    team: list
) -> (Dict[str, Dict[str, int | str]], List[Dict[str, Dict[str, int | str]]]):
    """
    Метод заполняет информацию о тренере который выбрал игрок
    :param team: list
    :param info_by_table:
    :param info_manager:
    :param row:
    :param result:
    :return: dict
    """
    if re.search(r'\d+', info_by_table.iat[row, 7]):
        point: Match[str] = re.search(r'\d+', info_by_table.iat[row, 7])
        club_manager: Match[str] = re.search(r'\(\w+\)', info_by_table.iat[row, 7])
        split_name_manager = info_by_table.iat[row, 7].split(":")
        split_name_manager = split_name_manager[1] if len(split_name_manager) > 1 else split_name_manager[0]
        split_name_manager = split_name_manager.split('(')[0]
        name_manager = split_name_manager.split()[0] if len(split_name_manager.split()) == 1 \
            else ' '.join(split_name_manager.split())

        info_manager[name_manager] = {
            "point": point.group(),
            "club": club_manager.group()[1:-1].upper(),
            "result": result.get(club_manager.group()[1:-1].upper())
        }
        team.append({
            "name_manager": name_manager,
            "point": point.group(),
            "club": club_manager.group()[1:-1].upper(),
            "result": result.get(club_manager.group()[1:-1].upper())
            })
    else:
        team.append({})

    return info_manager, team


def name_similarity_check(name_from_plate: list, name_from_site: str) -> bool:
    """
    Метод производит поиск по имени
    :param name_from_plate:
    :param name_from_site:
    :return:
    """
    if len(name_from_plate) == 2:
        if re.search(name_from_plate[0], name_from_site) and re.search(name_from_plate[1], name_from_site):
            return True
    else:
        if re.search(name_from_plate[0], name_from_site):
            return True

    return False


def fill_data_player(
    data_club_players: dict,
    info_by_table: DataFrame, row: int,
    statistic: list
) -> tuple[Dict[str, Dict[str, DataPlayer]], List[Dict[str, str]]]:
    """
    Метод формирует точные данные об игроках
    :param data_club_players: dict -
    :param info_by_table:
    :param row:
    :param statistic:
    :return: dict
    """
    squad_list = list()
    list_positions: list = ['GK', 'DEF', 'ATT DEF', 'CDM', 'CAM', 'WIN', 'FWD']

    for column in range(0, 7):
        position: str = list_positions[column]
        if re.search('\([A-Z]{3}\)', f'{info_by_table.iat[row, column]}'):
            club: str = re.search('\([A-Z]{3}\)', info_by_table.iat[row, column]).group()[1:-1]
        else:
            squad_list.append({})
            continue
        split_name_player: list = info_by_table.iat[row, column].split(":")
        split_name_player: str = split_name_player[1] if len(split_name_player) > 1 else split_name_player[0]
        name: str = re.split('\(', split_name_player.split()[0])[0]
        name: str = decoding_words(re.sub(r'(?<!-)(?=[A-Z])', r' \g<0>', name))
        squad_list.append({
            "name": name,
            "position": position,
            "club": club
        })
        if name not in data_club_players.keys():
            for static in statistic:
                if static.get(club):
                    for club_player_statistics in static[club]:
                        search_name: str = decoding_words(club_player_statistics['name'])
                        name_separation: list = name.split()
                        if name_similarity_check(name_from_plate=name_separation, name_from_site=search_name):
                            stats: StatisticPlayer = getting_detailed_statistics(
                                statistic=club_player_statistics.get('statistics'),
                                missed_balls=static.get('goals_conceded'),
                                minutes_missed=static.get('minutes_missed')
                            )
                            data_club_players[name]: DataPlayer = {
                                "position": position,
                                "club": club,
                                'statistic': stats
                            }
                            break
                    else:
                        data_club_players[name]: DataPlayer = {
                            "position": position,
                            "club": club,
                            'statistic': {
                                "saves": 0,
                                "penalty_save": 0,
                                "assists_total": 0,
                                "clean_sheets": 0,
                                "goals": 0,
                                "interceptions": 0,
                                "shotsblocked": 0,
                                "tackleswon": 0,
                                "chancescreated": 0,
                                "shots": 0
                            },
                        }
                    break

    return data_club_players, squad_list
