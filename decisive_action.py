import json

from pandas import DataFrame


def table_formation_decisive_action(result, coefficients) -> DataFrame:
    splitting_into_groups = [list(elem) for elem in zip(*result)]

    splitting_into_groups[0].insert(0, None)
    splitting_into_groups[1].insert(0, coefficients.get('save'))
    splitting_into_groups[2].insert(0, coefficients.get('clean_sheets'))
    splitting_into_groups[3].insert(0, coefficients.get('assist'))
    splitting_into_groups[4].insert(0, coefficients.get('defensive_actions'))
    splitting_into_groups[5].insert(0, coefficients.get('chances_created'))
    splitting_into_groups[6].insert(0, coefficients.get('shots'))
    splitting_into_groups[7].insert(0, coefficients.get('goals'))
    splitting_into_groups[8].insert(0, None)
    splitting_into_groups[9].insert(0, None)

    table_decisive_action = DataFrame({
        "Nicname": splitting_into_groups[0],
        "Saves": splitting_into_groups[1],
        "Clean Sheets": splitting_into_groups[2],
        "Assists": splitting_into_groups[3],
        "Defensive Actions": splitting_into_groups[4],
        "Chances Created": splitting_into_groups[5],
        "Shots": splitting_into_groups[6],
        "Goals": splitting_into_groups[7],
        "Win": splitting_into_groups[8],
        "Sum Pts": splitting_into_groups[9]
    })

    return table_decisive_action


def decisive_action_players(statistic_player, squad_game):
    resul_decisive_action = list()

    with open('responses.json', 'r', encoding='utf-8') as file:
        coefficients = json.load(file).get('coefficients_decisive_action')

    for name_games in squad_game.keys():
        points_scored = list()
        number_players = len(squad_game.get(name_games)) - 1
        points_scored.append(name_games)
        for gamer in squad_game.get(name_games)[:number_players]:
            if not gamer:
                points_scored.append(0)
            else:
                individual_statistics = statistic_player[gamer["name"]].get("statistic")
                match gamer["position"]:
                    case "GK":
                        points_save = (individual_statistics['saves'] + individual_statistics['penalty_save']) * \
                                      coefficients.get('save')
                        points_scored.append(points_save)
                    case "DEF":
                        if individual_statistics['clean_sheets'] != 0:
                            points_scored.append(coefficients.get('clean_sheets'))
                        else:
                            points_scored.append(0)
                    case "ATT DEF":
                        if individual_statistics['assists_total'] != 0:
                            points_scored.append(coefficients.get('assist'))
                        else:
                            points_scored.append(0)
                    case "CDM":
                        defensive_action_points = individual_statistics['interceptions'] + \
                                                  individual_statistics['shotsblocked'] + \
                                                  individual_statistics['tackleswon']
                        points_scored.append(defensive_action_points * coefficients.get('defensive_actions'))
                    case "CAM":
                        points_chances_created = individual_statistics['chancescreated'] * \
                                                 coefficients.get('chances_created')
                        points_scored.append(points_chances_created)
                    case "WIN":
                        points_scored.append(individual_statistics['shots'] * coefficients.get('shots'))
                    case 'FWD':
                        if individual_statistics['goals'] != 0:
                            points_scored.append(coefficients.get('goals'))
                        else:
                            points_scored.append(0)

        if squad_game[name_games][number_players].get('result') == 'win':
            points_scored.append(int(squad_game[name_games][number_players].get('point')))
        else:
            points_scored.append(0)
            
        points_scored.append(sum(points_scored[1:]))

        resul_decisive_action.append(points_scored)

    table = table_formation_decisive_action(result=resul_decisive_action, coefficients=coefficients)

    return table
