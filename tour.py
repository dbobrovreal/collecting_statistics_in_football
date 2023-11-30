import requests
from requests import Response
import json
from player_statistics import getting_player_statistics


def request_to_receive_a_tour_id() -> None:
    """
    Метод запрашивает у сайта по номеру тура информацию о играх
    (название команды которые играют между собой и id встречи)
    :return: None
    """
    with open('responses.json', 'r', encoding='utf-8') as file:
        tour = json.load(file).get('num_tour')

    headers: dict[str, str] = {
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
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.686 Mobile Safari/537.36',
        "If-Modified-Since": "Tues, 18 Jul 2023 00:00:00 GMT"
    }

    response: Response = requests.get(
        f'https://api.sofascore.com/api/v1/unique-tournament/17/season/52186/events/round/{tour}',
        headers=headers)

    information_about_tours: list = list()

    for rouds in json.loads(response.text)['events']:
        if rouds['status']['code'] == 100:
            if rouds['homeScore'].get('normaltime') > rouds['awayScore'].get('normaltime'):
                result_home = "win"
                result_away = "def"
            elif rouds['homeScore'].get('normaltime') < rouds['awayScore'].get('normaltime'):
                result_home = "def"
                result_away = "win"
            else:
                result_home = "draw"
                result_away = "draw"

            information_about_tours.append(
                {
                    "homeTeam": {
                        "name": rouds['homeTeam'].get('name'),
                        "nameCode": rouds['homeTeam'].get('nameCode'),
                        "homeTeam_slug": rouds['homeTeam']['slug'],
                        "result_math": result_home,
                        "goals_conceded":  rouds['awayScore'].get('normaltime')
                    },
                    "awayTeam": {
                        "name": rouds['awayTeam'].get('name'),
                        "awayTeam_slug": rouds['awayTeam']['slug'],
                        "nameCode": rouds['awayTeam'].get('nameCode'),
                        "result_math": result_away,
                        "goals_conceded": rouds['homeScore'].get('normaltime')
                    },
                    "id": rouds['id']
                }
            )
        else:
            print(f'Не сыгран матч {rouds["homeTeam"].get("name")} - {rouds["awayTeam"].get("name")}')

    getting_player_statistics(tour_parameters=information_about_tours)


if __name__ == '__main__':
    request_to_receive_a_tour_id()
