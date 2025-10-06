import random

def generate_first_round_matches(players):
    shuffled_players = []
    for player in players:
        shuffled_players.append(player)
    random.shuffle(shuffled_players)
    matches = []
    for i in range(0, len(players), 2):
        match = ([shuffled_players[i], ""], [shuffled_players[(i+1)], ""]) # ([joueur_i, score_joueur_i], [joueur_i+1, score_joueur_i+1])
        matches.append(match)

    return matches

def inscribe_match_results(match, result1):
    if result1 == 1:
        match[0][1] = result1
        match[1][1] = 0.0
    elif result1 == 0:
        match[0][1] = result1
        match[1][1] = 1.0
    else:
        match[0][1] = 0.5
        match[1][1] = 0.5

    return match
