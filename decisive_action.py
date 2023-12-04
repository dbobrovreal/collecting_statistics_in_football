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
        "Win": splitting_into_groups[8],
        "Sum Pts": splitting_into_groups[9]
    })

    return table_decisive_action


def decisive_action_players(statistic_player, squad_game):
    resul_decisive_action = list()
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
                        points_scored.append((individual_statistics['saves'] + individual_statistics['penalty_save']) * 2)
                    case "DEF":
                        if individual_statistics['clean_sheets'] != 0:
                            points_scored.append(8)
                        else:
                            points_scored.append(0)
                    case "ATT DEF":
                        if individual_statistics['assists_total'] != 0:
                            points_scored.append(8)
                        else:
                            points_scored.append(0)
                    case "CDM":
                        defensive_action_points = individual_statistics['interceptions'] + \
                                                  individual_statistics['shotsblocked'] + \
                                                  individual_statistics['tackleswon']
                        points_scored.append(defensive_action_points)
                    case "CAM":
                        points_scored.append(individual_statistics['chancescreated'] * 2)
                    case "WIN":
                        points_scored.append(individual_statistics['shots'] * 2)
                    case 'FWD':
                        if individual_statistics['goals'] != 0:
                            points_scored.append(8)
                        else:
                            points_scored.append(0)

        if squad_game[name_games][number_players].get('result') == 'win':
            points_scored.append(int(squad_game[name_games][number_players].get('point')))
        else:
            points_scored.append(0)
            
        points_scored.append(sum(points_scored[1:]))

        resul_decisive_action.append(points_scored)

    table = table_formation_decisive_action(result=resul_decisive_action)

    return table
