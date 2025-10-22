"""
Utilities to generate and manage tournament match pairings and results.

This module provides:
- generate_first_round_matches(players): produce randomized first-round pairings.
- generate_round_matches(players, previous_matches): produce pairings for subsequent rounds
  using score groups and avoiding previous pairings when possible.
- inscribe_match_results(match, result1): write a match result (from white player's POV).

Note: match representations used across the app are kept simple and serializable:
    match = ([white_id, white_score], [black_id, black_score])
Previous matches are tracked as a list of two-item lists: [[p1, p2], ...].
"""
from typing import Dict, List, Tuple, Any
import random


def generate_first_round_matches(players: Dict[str, Any]) -> Tuple[List[Tuple[List[Any], List[Any]]], List[List[Any]]]:
    """
    Generate randomized pairings for the first round.

    Parameters
    ----------
    players : dict
        Mapping of player_id -> points (points are ignored for the first round).

    Returns
    -------
    matches : list of tuple
        List of matches. Each match is a tuple: ([white_id, ""], [black_id, ""])
        Scores are initialized to empty strings.
    matches_used : list of list
        List of paired player ids [[p1, p2], ...] used to record that these players met.
    """
    shuffled_players: List[Any] = []
    for player_id in players.keys():
        shuffled_players.append(player_id)
    random.shuffle(shuffled_players)

    matches: List[Tuple[List[Any], List[Any]]] = []
    matches_used: List[List[Any]] = []
    for i in range(0, len(shuffled_players), 2):
        # If odd number of players, the last one will be left without a pair.
        if i + 1 >= len(shuffled_players):
            break
        p1 = shuffled_players[i]
        p2 = shuffled_players[i + 1]
        match = ([p1, ""], [p2, ""])
        matches.append(match)
        matches_used.append([p1, p2])

    return matches, matches_used


def generate_round_matches(
    players: Dict[str, float],
    previous_matches: List[List[Any]]
) -> Tuple[List[Tuple[List[Any], List[Any]]], List[List[Any]]]:
    """
    Generate pairings for a subsequent round.

    Strategy:
    - Group players by their current points.
    - Within each score group shuffle players to avoid deterministic ordering.
    - Attempt to pair players with the same (or nearest) score while avoiding
      pairings that already occurred (tracked in previous_matches).
    - If no eligible opponent is found for a player, that player remains unpaired
      for this round (caller may handle by giving bye or other rules).

    Parameters
    ----------
    players : dict
        Mapping player_id -> points (float).
    previous_matches : list
        Mutable list of previously paired id pairs, e.g. [[p1, p2], ...].
        This list will be appended with newly created pairs.

    Returns
    -------
    matches : list of tuple
        Newly generated matches in the format ([white_id, ""], [black_id, ""]).
    previous_matches : list
        The updated previous_matches list including the newly scheduled pairs.
    """
    # Group players by score
    score_groups: Dict[float, List[Any]] = {}
    for player_id, points in players.items():
        score_groups.setdefault(points, []).append(player_id)

    # Sort scores high -> low and flatten groups after shuffling each group
    sorted_scores = sorted(score_groups.keys(), reverse=True)
    sorted_players_id: List[Any] = []
    for score in sorted_scores:
        group = score_groups[score]
        random.shuffle(group)
        sorted_players_id.extend(group)

    matches: List[Tuple[List[Any], List[Any]]] = []
    used: List[Any] = []
    i = 0
    while i < len(sorted_players_id):
        p1 = sorted_players_id[i]
        if p1 in used:
            i += 1
            continue
        # Find next player p2 that p1 hasn't played with
        for j in range(i + 1, len(sorted_players_id)):
            p2 = sorted_players_id[j]
            if p2 in used:
                continue
            already_played = [p1, p2] in previous_matches or [p2, p1] in previous_matches
            if not already_played:
                matches.append(([p1, ""], [p2, ""]))
                used.append(p1)
                used.append(p2)
                previous_matches.append([p1, p2])
                break
        # If no partner found, player remains unpaired (handled by caller if needed)
        i += 1

    return matches, previous_matches


def inscribe_match_results(match: Tuple[List[Any], List[Any]], result1: Any) -> Tuple[List[Any], List[Any]]:
    """
    Record the result of a match given the white player's result.

    The function expects `match` to be mutable (lists) and sets both players'
    scores according to `result1`.

    Parameters
    ----------
    match : tuple of lists
        Match representation: ([white_id, white_score], [black_id, black_score]).
    result1 : str | float
        Result for the white player. Accepts values like "1", "0", "0.5" or numeric.

    Returns
    -------
    match : tuple of lists
        The same match structure with updated numeric scores (floats).

    Notes
    -----
    - If an invalid value is provided, the function prints an error message and
      leaves the match unchanged.
    """
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
