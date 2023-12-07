import requests
from requests import Response
import json
import time
import pandas
from pandas import DataFrame
from counting import calculating_statistics
from typing import Any, Dict
from data_collection import filling_in_information_on_managers, fill_data_player, decoding_words


def generating_a_statistics_report(player_statistics: list, result_tour: dict) -> None:
    """
    Метод вытягивает информацию из таблицы участников игры
    :param result_tour:
    :param player_statistics:
    :return: None
    """
    with open('responses.json', 'r', encoding='utf-8') as file:
        path_file: str = json.load(file).get('file_path')

    excel_data: DataFrame = pandas.read_excel(f"{path_file}", sheet_name='Табличка')
    data: DataFrame = pandas.DataFrame(excel_data.fillna(0), columns=['GK', 'DEF', 'ATT DEF', 'CDM', 'CAM', 'WIN',
                                                                      'FWD', 'COACH', 'Nickname'])
    index: int = 0
    game_result: dict = dict()
    manager: dict = dict()
    information_about_player_team: dict = dict()

    while True:
        try:
            if data['Nickname'].loc[index] != 0:
                game_result, assembled_team = fill_data_player(data_club_players=game_result, info_by_table=data,
                                                               row=index, statistic=player_statistics)
                manager, assembled_team = filling_in_information_on_managers(info_manager=manager, info_by_table=data,
                                                                             row=index, result=result_tour,
                                                                             team=assembled_team)
                information_about_player_team[data['Nickname'].loc[index]] = assembled_team
                index += 1
            else:
                break
        except KeyError:
            break

    calculating_statistics(information_received=game_result, information_manager=manager,
                           squad_game=information_about_player_team)


def match_result(parameters: list) -> Dict[str, str]:
    """
    Метод записывает в словарь результат матча каждого клуба
    :param parameters: list
    :return: Dict[str, str]
    """
    json_result: dict = dict()
    for info in parameters:
        team_home: str = info["homeTeam"].get('nameCode')
        result_home_team: str = info["homeTeam"].get("result_math")
        team_away: str = info["awayTeam"].get('nameCode')
        result_away_team: str = info["awayTeam"].get("result_math")
        json_result[team_home] = result_home_team
        json_result[team_away] = result_away_team

    return json_result


def getting_player_statistics(tour_parameters: list) -> None:
    """
    Метод запрашивает данные о каждой игре тура и ответ приходит в виде результат статистики игроков в json формате
    :param tour_parameters:
    :return: None
    """
    headers: Dict[str, str] = {
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
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/116.0.5845.686 Mobile Safari/537.36',
        "If-Modified-Since": "Tues, 18 Jul 2023 00:00:00 GMT"
    }

    headers_events: Dict[str, str] = {
        'authority': 'api.sofascore.com',
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9',
        'if-none-match': 'W/"1df332c938"',
        'origin': 'https://www.sofascore.com',
        'referer': 'https://www.sofascore.com/',
        'sec-ch-ua': '"Chromium";v="118", "YaBrowser";v="23", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/118.0.5993.2470 YaBrowser/23.11.0.2470 Yowser/2.5 Safari/537.36',
        "If-Modified-Since": "Tues, 18 Jul 2023 00:00:00 GMT"
    }

    statistic: list = list()

    game_summary: Dict[str, str] = match_result(parameters=tour_parameters)

    for games in tour_parameters:
        try:
            print(f'Программа запрашивает данные матча: {games["homeTeam"]["name"]} - {games["awayTeam"]["name"]}',
                  end=' ')
            response: Response = requests.get(f'https://api.sofascore.com/api/v1/event/{games["id"]}/lineups',
                                              headers=headers)
            json_game_statistics: dict = json.loads(response.text)
            players_home: list[dict[str, Any]] = list()
            players_away = list()
            statistic_home_team: dict = dict()
            statistic_away_team: dict = dict()
            for player_home in json_game_statistics['home']["players"]:
                if player_home.get('statistics'):
                    statistic_home_team: dict = player_home.get('statistics')

                players_home.append({
                    "name": decoding_words(player_home['player']['name']),
                    "position": player_home['position'],
                    "shirtNumber": player_home['shirtNumber'],
                    "statistics": statistic_home_team
                })

            for player_away in json_game_statistics['away']["players"]:
                if player_away.get('statistics'):
                    statistic_away_team = player_away.get('statistics')

                players_away.append({
                    "name": decoding_words(player_away['player']['name']),
                    "position": player_away['position'],
                    "shirtNumber": player_away['shirtNumber'],
                    "statistics": statistic_away_team
                })
            response_events = requests.get(f'https://api.sofascore.com/api/v1/event/{games["id"]}/incidents',
                                           headers=headers_events)
            missed_home: list = list()
            missed_away: list = list()
            list_incidents: list = response_events.json()['incidents']
            for elem in list_incidents[-1::-1]:
                if elem['incidentType'] == 'goal':
                    if elem['isHome']:
                        missed_away.append(elem['time'])
                    else:
                        missed_home.append(elem['time'])

            statistic.append(
                {
                    f"{games['homeTeam'].get('nameCode')}": players_home,
                    "result_match": game_summary.get(games['homeTeam'].get('nameCode')),
                    "goals_conceded": games['homeTeam'].get('goals_conceded'),
                    "minutes_missed": missed_home
                }
            )
            statistic.append(
                {
                    f"{games['awayTeam'].get('nameCode')}": players_away,
                    "result_match": game_summary.get(games['awayTeam'].get('nameCode')),
                    "goals_conceded": games['awayTeam'].get('goals_conceded'),
                    "minutes_missed": missed_away
                }
            )

            time.sleep(5)
            print("\033[32m Успешно \033[0m")
        except:
            print('\033[31m Ошибка \033[0m')
    generating_a_statistics_report(player_statistics=statistic, result_tour=game_summary)
