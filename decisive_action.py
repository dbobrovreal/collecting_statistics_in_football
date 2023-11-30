from pandas import DataFrame


def table_formation_decisive_action(result) -> DataFrame:
    splitting_into_groups = [list(elem) for elem in zip(*result)]
    table_decisive_action = DataFrame({
        "Nicname": splitting_into_groups[0],
        "Saves": splitting_into_groups[1],
        "Clean Sheets": splitting_into_groups[2],
        "Assists": splitting_into_groups[3],
        "Defensive Actions": splitting_into_groups[4],
        "Chances Created": splitting_into_groups[5],
        "Shots": splitting_into_groups[6],
        "Goals": splitting_into_groups[7],
        "Win": splitting_into_groups[8]
    })

    return table_decisive_action


def decisive_action_players(statistic_player, squad_game):
    resul_decisive_action = list()
    for name_games in squad_game.keys():
        points_scored = list()
        number_players = len(squad_game.get(name_games)) - 1
        points_scored.append(name_games)
        for gamer in squad_game.get(name_games)[:number_players]:
            individual_statistics = statistic_player[gamer["name"]].get("statistic")
            if gamer["position"] == "GK":
                points_scored.append(individual_statistics['saves'] * 2)
            elif gamer["position"] == "DEF":
                if individual_statistics['clean_sheets'] != 0:
                    points_scored.append(8)
                else:
                    points_scored.append(0)
            elif gamer["position"] == "ATT DEF":
                if individual_statistics['assists-total'] != 0:
                    points_scored.append(8)
                else:
                    points_scored.append(0)
            elif gamer["position"] == "CDM":
                defensive_action_points = individual_statistics['interceptions'] + \
                                          individual_statistics['shotsblocked'] + \
                                          individual_statistics['tacklesWon']
                points_scored.append(defensive_action_points)
            elif gamer["position"] == 'CAM':
                points_scored.append(individual_statistics['chancescreated'] * 2)
            elif gamer["position"] == 'WIN':
                points_scored.append(individual_statistics['shots'] * 2)
            elif gamer["position"] == 'FWD':
                if individual_statistics['goals'] != 0:
                    points_scored.append(8)
                else:
                    points_scored.append(0)

        if squad_game[name_games][number_players].get('result') == 'win':
            points_scored.append(squad_game[name_games][number_players].get('point'))
        else:
            points_scored.append(0)
        resul_decisive_action.append(points_scored)

    table = table_formation_decisive_action(result=resul_decisive_action)

    return table
