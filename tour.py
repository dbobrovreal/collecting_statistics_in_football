import requests
from requests import Response
import json
from player_statistics import getting_player_statistics


def request_to_receive_a_tour_id() -> bool:
    """
    Метод запрашивает у сайта по номеру тура информацию о играх
    (название команды которые играют между собой и id встречи)
    :return: None
    """
    with open('responses.json', 'r', encoding='utf-8') as file:
        tour: str = json.load(file).get('num_tour')

    headers_statistics: dict[str, str] = {
        'authority': 'api.sofascore.com',
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"ab5091d1a3"',
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

    print(f'Запрашиваем данные о {tour} туре с сайта sofascore.com')

    response_statistics: Response = requests.get(
        f'https://api.sofascore.com/api/v1/unique-tournament/17/season/52186/events/round/{tour}',
        headers=headers_statistics)

    information_about_tours: list = list()

    status_flag: bool = False

    for rouds in json.loads(response_statistics.text)['events']:
        goal_home: int = 0
        goal_away: int = 0
        result_home: None = None
        result_away: None = None
        if rouds['status']['code'] != 100:
            print(f'\033[31m Еще не сыгран матч {rouds["homeTeam"].get("name")} - {rouds["awayTeam"].get("name")}'
                  f'\033[0m')
        else:
            status_flag: bool = True
            if rouds['homeScore'].get('normaltime') > rouds['awayScore'].get('normaltime'):
                result_home: str = "win"
                result_away: str = "def"
            elif rouds['homeScore'].get('normaltime') < rouds['awayScore'].get('normaltime'):
                result_home: str = "def"
                result_away: str = "win"
            else:
                result_home: str = "draw"
                result_away: str = "draw"

            if rouds['awayScore'].get('normaltime') != 0:
                goal_away: int = rouds['awayScore'].get('normaltime')

            if rouds['homeScore'].get('normaltime') != 0:
                goal_home: int = rouds['homeScore'].get('normaltime')

        information_about_tours.append(
            {
                "homeTeam": {
                    "name": rouds['homeTeam'].get('name'),
                    "nameCode": rouds['homeTeam'].get('nameCode'),
                    "homeTeam_slug": rouds['homeTeam']['slug'],
                    "result_math": result_home,
                    "goals_conceded": goal_away
                },
                "awayTeam": {
                    "name": rouds['awayTeam'].get('name'),
                    "awayTeam_slug": rouds['awayTeam']['slug'],
                    "nameCode": rouds['awayTeam'].get('nameCode'),
                    "result_math": result_away,
                    "goals_conceded": goal_home
                },
                "id": rouds['id']
            }
        )

    if not status_flag:
        return False

    getting_player_statistics(tour_parameters=information_about_tours)
    print('Работа завершина')
    return True


if __name__ == '__main__':
    request_to_receive_a_tour_id()
