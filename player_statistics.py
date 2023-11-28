import requests
import json
import time
import pandas
from pandas import DataFrame
from counting import calculating_statistics
from typing import Any
from data_collection import filling_in_information_on_managers, fill_data_player


def generating_a_statistics_report(player_statistics: list, result_tour: dict) -> None:
    """
    Метод вытягивает информацию из таблицы участников игры
    :param result_tour:
    :param player_statistics:
    :return: None
    """
    excel_data: DataFrame = pandas.read_excel('test.xlsx', sheet_name='Табличка')
    data: DataFrame = pandas.DataFrame(excel_data.fillna(0), columns=['GK', 'DEF', 'ATT DEF', 'CDM', 'CAM', 'WIN',
                                                                      'FWD', 'COACH', 'Nickname'])
    index: int = 0
    game_result: dict = dict()
    manager = dict()

    while True:
        if data['Nickname'].loc[index] != 0:
            manager = filling_in_information_on_managers(info_manager=manager, info_by_table=data,
                                                         row=index, result=result_tour)
            game_result = fill_data_player(data_club_players=game_result, info_by_table=data,
                                           row=index, statistic=player_statistics)
            index += 1
        else:
            break

    calculating_statistics(information_received=game_result, information_manager=manager)


def match_result(parameters):
    json_result = dict()
    for info in parameters:
        team_home = info["homeTeam"].get('nameCode')
        result_home_team = info["homeTeam"].get("result_math")
        team_away = info["awayTeam"].get('nameCode')
        result_away_team = info["awayTeam"].get("result_math")
        json_result[team_home] = result_home_team
        json_result[team_away] = result_away_team

    return json_result


def getting_player_statistics(tour_parameters: list) -> None:
    """
    Метод запрашивает данные о каждой игре тура и ответ приходит в виде результат статистики игроков в json формате
    :param tour_parameters:
    :return: None
    """
    headers: dict[str, str] = {
        'authority': 'api.sofascore.com',
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"c68e06ac51"',
        'origin': 'https://www.sofascore.com',
        'referer': 'https://www.sofascore.com/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.686 Mobile Safari/537.36',
        "If-Modified-Since": "Tues, 18 Jul 2023 00:00:00 GMT"
    }
    statistic: list = list()

    game_summary = match_result(tour_parameters)

    for games in tour_parameters:
        print(f'{games["homeTeam"]["name"]} - {games["awayTeam"]["name"]}')
        response = requests.get(f'https://api.sofascore.com/api/v1/event/{games["id"]}/lineups', headers=headers)
        json_game_statistics = json.loads(response.text)
        players_home: list[dict[str, Any]] = list()
        players_away = list()

        for player_home in json_game_statistics['home']["players"]:
            players_home.append({
                "name": player_home['player']['name'],
                "position": player_home['position'],
                "shirtNumber": player_home['shirtNumber'],
                "statistics": player_home['statistics']
            })

        for player_away in json_game_statistics['away']["players"]:
            players_away.append({
                "name": player_away['player']['name'],
                "position": player_away['position'],
                "shirtNumber": player_away['shirtNumber'],
                "statistics": player_away['statistics']
            })

        statistic.append(
            {
                f"{games['homeTeam'].get('nameCode')}": players_home,
                "result_match": game_summary.get(games['homeTeam'].get('nameCode')),
                "goals_conceded": games['homeTeam'].get('goals_conceded')
            }
        )
        statistic.append(
            {
                f"{games['awayTeam'].get('nameCode')}": players_away,
                "result_match": game_summary.get(games['awayTeam'].get('nameCode')),
                "goals_conceded": games['awayTeam'].get('goals_conceded')
            }
        )

        time.sleep(5)
    generating_a_statistics_report(player_statistics=statistic, result_tour=game_summary)
