import random

def generate_first_round_matches(players):
    shuffled_players = []
    for player_id in players.keys():
        shuffled_players.append(player_id)
    random.shuffle(shuffled_players)
    matches = []
    matches_used = []
    for i in range(0, len(players), 2):
        p1 = shuffled_players[i]
        p2 = shuffled_players[(i+1)]
        match = ([p1, ""], [p2, ""]) # ([joueur_1, score_joueur_1], [joueur_2, score_joueur_2])
        matches.append(match)
        matches_used.append([p1, p2])

    return matches, matches_used

def generate_round_matches(players, previous_matches):
    # players: dict {player_id: points}
    # previous_matches: set of frozenset({player1, player2}) for all previous rounds

    # Regroupe les joueurs par score
    score_groups = {}
    for player_id, points in players.items():
        score_groups.setdefault(points, []).append(player_id)

    # Mélange les joueurs ayant le même score
    sorted_scores = sorted(score_groups.keys(), reverse=True)
    sorted_players_id = []
    for score in sorted_scores:
        group = score_groups[score]
        random.shuffle(group)
        sorted_players_id.extend(group)

    # Génère les paires en évitant les doublons
    matches = []
    used = []
    i = 0
    while i < len(sorted_players_id):
        p1 = sorted_players_id[i]
        # Cherche le prochain joueur avec qui p1 n'a pas encore joué
        for j in range(i+1, len(sorted_players_id)):
            p2 = sorted_players_id[j]
            # Vérifie si le match a déjà eu lieu
            already_played = [p1, p2] in previous_matches or [p2, p1] in previous_matches
            if not already_played and p1 not in used and p2 not in used:
                matches.append(([p1, ""], [p2, ""]))
                used.append(p1)
                used.append(p2)
                previous_matches.append([p1, p2])
                break
        i += 1
        # Si p1 n'a pas trouvé de partenaire, il reste sans match ce tour

    return matches, previous_matches

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