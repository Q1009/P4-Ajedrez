from model.tournament_model import Tournament, TournamentRound
import json
from utils.tournament_utils import generate_first_round_matches
from utils.tournament_utils import inscribe_match_results
from utils.tournament_utils import generate_round_matches
from datetime import datetime


class TournamentController:
    """Controller for managing Tournament instances persisted as JSON.

    Attributes
    ----------
    tournaments : list[Tournament]
        In-memory list of Tournament instances loaded from the JSON store.

    Methods
    -------
    load_tournaments_from_json(filepath="data/tournaments.json"):
        Load tournaments from a JSON file into memory.
    save_tournaments_to_json(filepath="data/tournaments.json"):
        Persist the in-memory tournaments list to a JSON file.
    display_tournaments():
        Return the list of tournaments (loads from storage first).
    add_tournament(name, location, start_date, end_date, description):
        Create and persist a new tournament.
    remove_tournament(index):
        Remove a tournament by index and persist changes.
    modify_tournament(index, ...):
        Update fields of an existing tournament and persist changes.
    subscribe_players(index, player_ids):
        Subscribe players to a tournament.
    get_tournament(index):
        Retrieve a tournament by index (loads from storage first).
    get_tournaments_count():
        Return the number of tournaments stored.
    get_tournament_round_matches_count(index, round_index):
        Return the number of matches in a specific round.
    start_tournament(index):
        Initialize tournament (generate first round, set status).
    tournament_round_status_update(index, round_index):
        Check if all matches in a round have results.
    close_tournament_round(index, round_index):
        Mark a round as finished and set its timestamps.
    put_tournament_round_match_results(index, round_index, match_number, result1):
        Record a match result for a given round.
    update_tournament_round_players_points(index, round_index):
        Update players' points from a finished round.
    initiate_next_tournament_round(index):
        Generate and append the next round pairings.
    close_tournament(index):
        Mark tournament as finished.
    """

    def __init__(self):
        """
        Initialize the TournamentController.

        Starts with an empty in-memory list; callers should use display_tournaments()
        or load_tournaments_from_json() to populate the list from persistent storage.
        """
        self.tournaments = []

    def load_tournaments_from_json(self, filepath="data/tournaments.json"):
        """
        Load tournaments from a JSON file into the in-memory list.

        Parameters
        ----------
        filepath : str
            Path to the JSON file containing tournament records.

        Notes
        -----
        If the file does not exist or contains invalid JSON, the in-memory list
        remains empty (no exception is raised).
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                tournaments_loaded = json.load(f)
                for tournament_data in tournaments_loaded:
                    tournament = Tournament.from_dict(tournament_data)
                    self.tournaments.append(tournament)

        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_tournaments_to_json(self, filepath="data/tournaments.json"):
        """
        Persist the in-memory tournaments list to a JSON file.

        Parameters
        ----------
        filepath : str
            Destination path for the JSON file.
        """
        data = []
        for tournament in self.tournaments:
            data.append(tournament.to_dict())
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def display_tournaments(self):
        """
        Return the list of tournaments, reloading from storage first.

        Returns
        -------
        list[Tournament]
            In-memory list of Tournament instances.
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        return self.tournaments

    def add_tournament(self, name, location, start_date, end_date, description):
        """
        Create a new Tournament and persist it.

        Parameters
        ----------
        name : str
            Tournament name.
        location : str
            Tournament location.
        start_date : str
            Start date string (YYYY-MM-DD).
        end_date : str
            End date string (YYYY-MM-DD).
        description : str
            Optional description for the tournament.
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        new_tournament = Tournament(
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            description=description,
            )
        self.tournaments.append(new_tournament)
        self.save_tournaments_to_json()

    def remove_tournament(self, index):
        """
        Remove a tournament by index and persist changes.

        Parameters
        ----------
        index : int
            Index of the tournament to remove.

        Returns
        -------
        tuple (name, tournament_id)
            Name and unique id of the removed tournament.
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        remove_tournament = self.tournaments.pop(index)
        self.save_tournaments_to_json()
        return remove_tournament.name, remove_tournament.tournament_id

    def modify_tournament(self, index, name=None, location=None, start_date=None, end_date=None, description=None):
        """
        Modify fields of an existing tournament and persist changes.

        Only provided keyword arguments are updated.

        Parameters
        ----------
        index : int
            Index of the tournament to modify.
        name, location, start_date, end_date, description : optional
            New values for corresponding tournament attributes.
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        tournament = self.tournaments[index]
        if name:
            tournament.name = name
        if location:
            tournament.location = location
        if start_date:
            tournament.start_date = start_date
        if end_date:
            tournament.end_date = end_date
        if description:
            tournament.description = description
        self.save_tournaments_to_json()

    def subscribe_players(self, index, player_ids):
        """
        Subscribe players to a tournament.

        Parameters
        ----------
        index : int
            Index of the tournament.
        player_ids : iterable
            Iterable of player federation IDs to subscribe.

        Returns
        -------
        tuple (subscribed_ids, already_subscribed_ids)
            Subscribed IDs and IDs that were already present.
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        tournament = self.tournaments[index]
        subscribed_ids = []
        already_subscribed_ids = []
        for pid in player_ids:
            if pid not in tournament.players.keys():
                tournament.players[pid] = 0.0
                subscribed_ids.append(pid)
            else:
                already_subscribed_ids.append(pid)
        self.save_tournaments_to_json()
        return subscribed_ids, already_subscribed_ids

    def get_tournament(self, index):
        """
        Retrieve a tournament by index after reloading storage.

        Parameters
        ----------
        index : int
            Index of the tournament to retrieve.

        Returns
        -------
        Tournament
            The requested Tournament instance.
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        return self.tournaments[index]

    def get_tournaments_count(self):
        """
        Return the number of tournaments currently stored.

        Returns
        -------
        int
            Number of tournaments.
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        return len(self.tournaments)

    def get_tournament_round_matches_count(self, index, round_index):
        """
        Return the number of matches in a specific tournament round.

        Parameters
        ----------
        index : int
            Tournament index.
        round_index : int
            Round index within the tournament.

        Returns
        -------
        int
            Number of matches in the requested round.
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        return len(self.tournaments[index].rounds[round_index].matches)

    def start_tournament(self, index):
        """
        Initialize a tournament: set status, compute number of rounds and create first round.

        Parameters
        ----------
        index : int
            Index of the tournament to start.
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        tournament = self.tournaments[index]
        tournament.current_round = 1
        tournament.number_of_rounds = len(tournament.players) - 1
        tournament.status = "En cours"
        # Instancier le premier round
        matches, tournament.matches_history = generate_first_round_matches(tournament.players)
        first_round = TournamentRound(round_number=1, matches=matches, status="En cours")
        tournament.rounds.append(first_round)
        self.save_tournaments_to_json()

    def tournament_round_status_update(self, index, round_index):
        """
        Check whether all matches in a round have recorded results.

        Parameters
        ----------
        index : int
            Tournament index.
        round_index : int
            Round index.

        Returns
        -------
        bool | None
            True if all matches have results, otherwise None.
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        tournament = self.tournaments[index]
        round = tournament.rounds[round_index]
        matches_count = len(round.matches)
        matches_over = 0
        for match in round.matches:
            if str(match[0][1]) != "":
                matches_over += 1

        if matches_over == matches_count:
            return True
        self.save_tournaments_to_json()

    def close_tournament_round(self, index, round_index):
        """
        Mark a specific tournament round as finished and set its end timestamp.

        Parameters
        ----------
        index : int
            Tournament index.
        round_index : int
            Round index to close.
        """
        now = datetime.now()
        self.tournaments.clear()
        self.load_tournaments_from_json()
        tournament = self.tournaments[index]
        round = tournament.rounds[round_index]
        round.end_date = now.strftime("%Y-%m-%d")
        round.end_time = now.strftime("%H:%M:%S")
        round.status = "Terminé"
        self.save_tournaments_to_json()

    def put_tournament_round_match_results(self, index, round_index, match_number, result1):
        """
        Record the result of a specific match in a round.

        Parameters
        ----------
        index : int
            Tournament index.
        round_index : int
            Round index.
        match_number : int | str
            Match number/index within the round.
        result1 : str | float
            Result from the white player's perspective ("1", "0", "0.5", etc.).
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        tournament = self.tournaments[index]
        round = tournament.rounds[round_index]
        match = round.matches[int(match_number)]
        round.matches[int(match_number)] = inscribe_match_results(match, result1)
        self.save_tournaments_to_json()

    def update_tournament_round_players_points(self, index, round_index):
        """
        Update players' accumulated points from a completed round.

        Parameters
        ----------
        index : int
            Tournament index.
        round_index : int
            Round index whose match results should be applied.
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        tournament = self.tournaments[index]
        round = tournament.rounds[round_index]
        for match in round.matches:
            tournament.players[match[0][0]] += match[0][1]
            tournament.players[match[1][0]] += match[1][1]
        self.save_tournaments_to_json()

    def initiate_next_tournament_round(self, index):
        """
        Generate pairings and append the next round to the tournament.

        Parameters
        ----------
        index : int
            Tournament index.
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        tournament = self.tournaments[index]
        tournament.current_round += 1
        matches, tournament.matches_history = generate_round_matches(tournament.players, tournament.matches_history)
        next_round = TournamentRound(round_number=tournament.current_round, matches=matches, status="En cours")
        tournament.rounds.append(next_round)
        self.save_tournaments_to_json()

    def close_tournament(self, index):
        """
        Mark a tournament as finished and persist changes.

        Parameters
        ----------
        index : int
            Tournament index.
        """
        self.tournaments.clear()
        self.load_tournaments_from_json()
        tournament = self.tournaments[index]
        tournament.status = "Terminé"
        self.save_tournaments_to_json()
