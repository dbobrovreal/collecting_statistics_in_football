import re
from re import Match
from pandas import DataFrame
import unidecode


def decoding_words(word) -> str:
    return unidecode.unidecode(word)


def getting_detailed_statistics(statistic: dict, game_status: str, missed_balls: int) -> dict:
    """
    Метод для получения точной статистики игроков
    :param missed_balls:
    :param game_status:
    :param statistic:
    :return: dict
    """
    saves, assists_total, interception, shots_blocked, tackles, \
        chances_created, gols, minute, clean_sheets = 0, 0, 0, 0, 0, 0, 0, 0, 0

    if statistic.get('saves'):
        saves: int = statistic.get('saves')

    if statistic.get('goalAssist'):
        assists_total: int = statistic.get('goalAssist')

    if statistic.get('interceptionWon'):
        interception: int = statistic.get('interceptionWon')

    if statistic.get("blockedScoringAttempt"):
        shots_blocked: int = statistic.get("blockedScoringAttempt")

    if statistic.get("totalTackle"):
        tackles: int = statistic.get("totalTackle")

    if statistic.get("keyPass"):
        chances_created: int = statistic.get("keyPass")

    shot_off: int = 0
    if statistic.get("shotOffTarget"):
        shot_off: int = statistic.get("shotOffTarget")

    shot_on: int = 0
    if statistic.get("onTargetScoringAttempt"):
        shot_on: int = statistic.get("onTargetScoringAttempt")

    shots: int = shot_on + shot_off

    if statistic.get("goals"):
        gols: int = statistic.get("goals")

    if statistic.get('minutesPlayed'):
        minute: int = statistic.get('minutesPlayed')

    if game_status == 'win' and missed_balls == 0 and minute >= 60:
        clean_sheets: int = 1

    processed_statistics: dict[str, int] = {
        "saves": saves,
        "assists-total": assists_total,
        "clean_sheets": clean_sheets,
        "goals": gols,
        "interceptions": interception,
        "shotsblocked": shots_blocked,
        "tacklesWon": tackles,
        "chancescreated": chances_created,
        "shots": shots,
    }

    return processed_statistics


def filling_in_information_on_managers(info_manager, info_by_table: DataFrame, row: int, result: dict, team: list):
    """
    Метод заполняет информацию о тренере который выбрал игрок
    :param team:
    :param info_by_table:
    :param info_manager:
    :param row:
    :param result:
    :return: dict
    """
    point: Match[str] = re.search(r'\d+', info_by_table.iat[row, 7])
    club_manager: Match[str] = re.search(r'\(\w+\)', info_by_table.iat[row, 7])
    name_manager: Match[str] = re.search(r':.*\(', info_by_table.iat[row, 7])
    info_manager[name_manager.group()[2:-2]] = {
        "point": point.group(),
        "club": club_manager.group()[1:-1].upper(),
        "result": result.get(club_manager.group()[1:-1].upper())
    }
    team.append({
        "name_manager": name_manager.group()[2:-2],
        "point": point.group(),
        "club": club_manager.group()[1:-1].upper(),
        "result": result.get(club_manager.group()[1:-1].upper())
        })

    return info_manager, team


def fill_data_player(data_club_players: dict, info_by_table: DataFrame, row: int, statistic) -> tuple[dict,
    list[dict[str, str]]]:
    """
    Метод формирует точные данные об игроках
    :param data_club_players:
    :param info_by_table:
    :param row:
    :param statistic:
    :return: dict
    """
    squad_list = list()
    list_positions = ['GK', 'DEF', 'ATT DEF', 'CDM', 'CAM', 'WIN', 'FWD']

    for column in range(0, 7):
        player: list = info_by_table.iat[row, column].split()
        position: str = list_positions[column]
        club: str = player[2][1:4].upper()
        full_name: str = re.sub(r'\([^)]*\)', '', info_by_table.iat[row, column])
        name: str = decoding_words(re.sub(r'(?<!-)(?=[A-Z])', r' \g<0>', re.sub(r'([^:]+:)', '', full_name)))
        squad_list.append({
            "name": name[2:-1],
            "position": position,
            "club": club
        })
        if name[2:-1] not in data_club_players.keys():
            for static in statistic:
                if static.get(club):
                    for club_player_statistics in static[club]:
                        search_name: str = decoding_words(club_player_statistics['name'])
                        if re.search(name[2:-1], search_name):
                            stats = getting_detailed_statistics(club_player_statistics.get('statistics'),
                                                                game_status=static.get('result_match'),
                                                                missed_balls=static.get('goals_conceded'))
                            data_club_players[name[2:-1]] = {
                                "position": position,
                                "club": club,
                                'statistic': stats
                            }
                            break
                    else:
                        data_club_players[name[2:-1]] = {
                            "position": position,
                            "club": club,
                            'statistic': {
                                "saves": 0,
                                "assists-total": 0,
                                "clean_sheets": 0,
                                "goals": 0,
                                "interceptions": 0,
                                "shotsblocked": 0,
                                "tacklesWon": 0,
                                "chancescreated": 0,
                                "shots": 0
                            },
                        }
                    break

    return data_club_players, squad_list
