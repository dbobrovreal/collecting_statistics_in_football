import json
from pandas import DataFrame
from typing import Dict, List
from data_collection import DataPlayer


def formation_goal_table(goal_statistics: list) -> DataFrame:
    """
    Формирование таблицы с голами всех выбранных игроков
    :param goal_statistics: list
    :return: DataFrame
    """
    splitting_into_groups = [list(elem) for elem in zip(*goal_statistics)]
    goal_table = DataFrame({
        "Nicname": splitting_into_groups[0],
        "GK": splitting_into_groups[1],
        "DEF": splitting_into_groups[2],
        "ATT DEF": splitting_into_groups[3],
        "CDM": splitting_into_groups[4],
        "CAM": splitting_into_groups[5],
        "WIN": splitting_into_groups[6],
        "SUM PST": splitting_into_groups[7]
    })

    return goal_table


def formation_dry_match_table(statistic_player_clear_sheets: list) -> DataFrame:
    """
    Метод для формирование таблицы с игроками у кого есть сухая игра
    :param statistic_player_clear_sheets: list
    :return: DataFrame
    """
    splitting_into_groups = [list(elem) for elem in zip(*statistic_player_clear_sheets)]
    table_clear_sheets = DataFrame(
        {
            "Nicname": splitting_into_groups[0],
            "GK": splitting_into_groups[1],
            "DEF": splitting_into_groups[2],
            "ATT DEF": splitting_into_groups[3],
            "CDM": splitting_into_groups[4],
            "Sum Pst": splitting_into_groups[5]
        }
    )

    return table_clear_sheets


def forming_table_with_chemistry(statistic_goal_assist: list) -> DataFrame:
    """
    Метод формирование таблицы Goal/Assist
    :param statistic_goal_assist: list
    :return: DataFrame
    """
    splitting_into_groups = [list(elem) for elem in zip(*statistic_goal_assist)]
    goal_assist_table = DataFrame({
        "Nicname": splitting_into_groups[0],
        "GK": splitting_into_groups[1],
        "DEF": splitting_into_groups[2],
        "ATT DEF": splitting_into_groups[3],
        "CDM": splitting_into_groups[4],
        "CAM": splitting_into_groups[5],
        "WIN": splitting_into_groups[6],
        "FWD": splitting_into_groups[7],
        "Sum Pst": splitting_into_groups[8]
    })

    return goal_assist_table


def scoring_points(
        individual_statistics: dict,
        goal: list | None = None,
        dry_game: list | None = None,
        goal_assist: list | None = None
) -> tuple[list | None, list | None, list | None]:
    """
    Метод просматривает такие показатели, как goals, assists_total, clean_sheets.
    Записывает по каждому игроку в команде сколько очков,
    игрок получил по перечислинным показателям
    :param individual_statistics: dict
    :param goal: list | None
    :param dry_game: list | None
    :param goal_assist: list | None
    :return: tuple[list | None, list | None, list | None]
    """
    with open('responses.json', 'r', encoding='utf-8') as file:
        coefficients_goal = json.load(file).get('coefficients_goal')

    if goal is not None:
        goal.append(coefficients_goal) if individual_statistics.get("goals") != 0 else goal.append(0)

    if dry_game is not None:
        dry_game.append(1) if individual_statistics.get("clean_sheets") != 0 else dry_game.append(0)

    if goal_assist is not None:
        if individual_statistics.get("goals") != 0 or individual_statistics.get("assists_total") != 0:
            goal_assist.append('+')
        else:
            goal_assist.append(None)

    return goal_assist, goal, dry_game


def formation_table_with_chemistry_of_players(
    statistic_player:  dict[str, dict[str, DataPlayer]],
    squad_gamer: Dict[str, List[Dict[str, str]]]
) -> tuple[DataFrame, DataFrame, DataFrame]:
    """
    Метод формирует таблицы goals, assists_total, clean_sheets.
    :param statistic_player: dict[str, dict[str, DataPlayer]]
    :param squad_gamer: Dict[str, List[Dict[str, str]]]
    :return: tuple[DataFrame, DataFrame, DataFrame]
    """
    with open('responses.json', 'r', encoding='utf-8') as file:
        coefficients = json.load(file)

    result_goals_scored = list()
    result_clean_game = list()
    result_goals_assist = list()
    for nicname in squad_gamer.keys():
        goals_scored = list()
        clean_game = list()
        goals_assist = list()
        number_players = len(squad_gamer.get(nicname)) - 1
        goals_scored.append(nicname)
        clean_game.append(nicname)
        goals_assist.append(nicname)
        for squad in squad_gamer.get(nicname)[:number_players]:
            if not squad:
                goals_assist.append(None)
                goals_scored.append(0)
                clean_game.append(0)
                continue
            else:
                individual_statistics = statistic_player[squad["name"]].get("statistic")
                match squad.get('position'):
                    case 'GK':
                        goals_scored, clean_game = scoring_points(
                            individual_statistics=individual_statistics,
                            goal=goals_scored,
                            dry_game=clean_game,
                        )[1:]
                        goals_assist.append(None)
                    case 'DEF':
                        goals_scored, clean_game = scoring_points(
                            individual_statistics=individual_statistics,
                            goal=goals_scored,
                            dry_game=clean_game
                        )[1:]
                        goals_assist.append(None)
                    case 'ATT DEF':
                        goals_scored, clean_game = scoring_points(
                            individual_statistics=individual_statistics,
                            goal=goals_scored,
                            dry_game=clean_game
                        )[1:]
                        goals_assist.append(None)
                    case 'CDM':
                        goals_assist, goals_scored, clean_game = scoring_points(
                            individual_statistics=individual_statistics,
                            goal=goals_scored,
                            dry_game=clean_game,
                            goal_assist=goals_assist
                        )
                    case 'CAM':
                        goals_assist, goals_scored = scoring_points(individual_statistics=individual_statistics,
                                                                    goal=goals_scored,
                                                                    goal_assist=goals_assist)[:2]

                    case 'WIN':
                        goals_assist, goals_scored = scoring_points(individual_statistics=individual_statistics,
                                                                    goal=goals_scored,
                                                                    goal_assist=goals_assist)[:2]
                    case 'FWD':
                        goals_assist = scoring_points(individual_statistics=individual_statistics,
                                                      goal_assist=goals_assist)[0]
        goals_scored.append(sum(goals_scored[1:]))

        match sum(clean_game[1:]):
            case 0:
                clean_game.append(0)
            case 1:
                clean_game.append(coefficients['coefficients_clean_sheet'].get('for_one'))
            case 2:
                clean_game.append(coefficients['coefficients_clean_sheet'].get('in_two'))
            case 3:
                clean_game.append(coefficients['coefficients_clean_sheet'].get('for_three'))
            case 4:
                clean_game.append(coefficients['coefficients_clean_sheet'].get('for_four'))

        number_of_advantages = 0

        for element in goals_assist[1:]:
            if element == '+':
                number_of_advantages += 1

        match number_of_advantages:
            case 0:
                goals_assist.append(0)
            case 1:
                goals_assist.append(coefficients['coefficients_goal_and_assist'].get('for_one'))
            case 2:
                goals_assist.append(coefficients['coefficients_goal_and_assist'].get('in_two'))
            case 3:
                goals_assist.append(coefficients['coefficients_goal_and_assist'].get('for_three'))
            case 4:
                goals_assist.append(coefficients['coefficients_goal_and_assist'].get('for_four'))

        result_goals_scored.append(goals_scored)
        result_clean_game.append(clean_game)
        result_goals_assist.append(goals_assist)

    table_goals_scored = formation_goal_table(goal_statistics=result_goals_scored)
    table_clear_sheet = formation_dry_match_table(statistic_player_clear_sheets=result_clean_game)
    table_goals_assist = forming_table_with_chemistry(statistic_goal_assist=result_goals_assist)

    return table_goals_scored, table_clear_sheet, table_goals_assist
