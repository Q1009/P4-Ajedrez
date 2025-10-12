import random

def generate_first_round_matches(players):
    shuffled_players = []
    for player_id in players.keys():
        shuffled_players.append(player_id)
    random.shuffle(shuffled_players)
    matches = []
    for i in range(0, len(players), 2):
        match = ([shuffled_players[i], ""], [shuffled_players[(i+1)], ""]) # ([joueur_i, score_joueur_i], [joueur_i+1, score_joueur_i+1])
        matches.append(match)

    return matches

def generate_round_matches(players):
    sorted_players_id = []
    sorted_players = {k: v for k, v in sorted(players.items(), key=lambda item: item[1], reverse=True)}
    for key in sorted_players.keys():
        sorted_players_id.append(key)

    matches = []
    for i in range(0, len(players), 2):
        match = ([sorted_players_id[i], ""], [sorted_players_id[(i+1)], ""]) # ([joueur_i, score_joueur_i], [joueur_i+1, score_joueur_i+1])
        matches.append(match)

    return matches

def inscribe_match_results(match, result1):
    result2 = float(result1)
    if result2 == 1.0:
        match[0][1] = result2
        match[1][1] = 0.0
    elif result2 == 0.0:
        match[0][1] = result2
        match[1][1] = 1.0
    elif result2 == 0.5:
        match[0][1] = result2
        match[1][1] = 0.5
    else:
        print("Le résultat saisi est invalide")

    return match