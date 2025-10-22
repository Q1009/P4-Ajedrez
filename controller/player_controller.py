import json
from model.player_model import ChessPlayer
from utils.tournament_utils import calculate_elo


class ChessPlayerController:
    """Controller for managing ChessPlayer data persisted in JSON.

    Provides simple CRUD operations, lookup helpers and rating updates used by
    the console views and tournament workflow.

    Attributes
    ----------
    chess_players : list[ChessPlayer]
        In-memory list of ChessPlayer instances loaded from the JSON store.

    Methods
    -------
    display_players_from_json()
        Load players from JSON and return the list of ChessPlayer instances.
    add_player(surname, name, date_of_birth, id, elo)
        Create a new ChessPlayer and persist it to JSON.
    remove_player(index)
        Remove a player by index and persist changes.
    modify_player(index, ...)
        Update fields of an existing player and persist changes.
    get_player(index)
        Return the ChessPlayer at the given index (after loading from JSON).
    get_players_count()
        Return the current number of players.
    get_players_id()
        Return a list of federation_chess_id for all players.
    transform_players_id_list(players_id)
        Parse a comma-separated string of IDs and return (valid_ids, invalid_ids).
    get_player_by_federation_id(federation_id)
        Lookup and return a ChessPlayer by their federation ID.
    update_player_by_federation_id(federation_id, player1)
        Update a player's rating and/or games played by federation ID and persist.
    update_players_games_and_elo(tournament)
        Apply tournament results: increment games played, compute and persist new ELOs.
    save_players_to_json(filepath="data/players.json")
        Serialize the in-memory players list to the given JSON file.
    load_players_from_json(filepath="data/players.json")
        Populate the in-memory list by reading the given JSON file.
    """

    def __init__(self):
        """
        Initialize the ChessPlayerController.

        The controller starts with an empty in-memory list; callers should
        invoke display_players_from_json() or load_players_from_json() to
        populate the list from persistent storage.
        """
        self.chess_players = []

    def display_players_from_json(self):
        """
        Load players from the default JSON file into memory and return them.

        Returns
        -------
        list[ChessPlayer]
            List of ChessPlayer instances loaded from storage (may be empty).
        """
        self.chess_players.clear()
        self.load_players_from_json()
        return self.chess_players

    def add_player(self, surname, name, date_of_birth, id, elo):
        """
        Add a new player and persist the updated list.

        Parameters
        ----------
        surname : str
            Family name of the player.
        name : str
            Given name of the player.
        date_of_birth : str
            Date of birth (string).
        id : str
            Federation chess identifier.
        elo : int | float
            Player rating.
        """
        self.chess_players.clear()
        self.load_players_from_json()
        new_player = ChessPlayer(surname, name, date_of_birth, id, elo)
        self.chess_players.append(new_player)
        self.save_players_to_json()

    def remove_player(self, index):
        """
        Remove the player at the provided index and persist changes.

        Parameters
        ----------
        index : int
            Index of the player in the in-memory list.

        Returns
        -------
        tuple (name, surname)
            The removed player's given name and family name.
        """
        self.chess_players.clear()
        self.load_players_from_json()
        removed_player = self.chess_players.pop(index)
        self.save_players_to_json()
        return removed_player.name, removed_player.surname

    def modify_player(self, index, surname=None, name=None, date_of_birth=None, federation_chess_id=None, elo=None):
        """
        Modify fields of an existing player and persist changes.

        Only provided keyword arguments will be updated.

        Parameters
        ----------
        index : int
            Index of the player to modify.
        surname, name, date_of_birth, federation_chess_id, elo : optional
            New values for the corresponding fields.

        Returns
        -------
        None
        """
        self.chess_players.clear()
        self.load_players_from_json()
        player = self.chess_players[index]
        if surname:
            player.surname = surname
        if name:
            player.name = name
        if date_of_birth:
            player.date_of_birth = date_of_birth
        if federation_chess_id:
            player.federation_chess_id = federation_chess_id
        if elo:
            player.elo = elo
        self.save_players_to_json()

    def get_player(self, index):
        """
        Return the ChessPlayer at the specified index.

        Parameters
        ----------
        index : int
            Index of the player to retrieve.

        Returns
        -------
        ChessPlayer
            The requested player instance.
        """
        self.chess_players.clear()
        self.load_players_from_json()
        return self.chess_players[index]

    def get_players_count(self):
        """
        Return the number of players stored in JSON.

        Returns
        -------
        int
            Number of players.
        """
        self.chess_players.clear()
        self.load_players_from_json()
        return len(self.chess_players)

    def get_players_id(self):
        """
        Return a list of federation IDs for all players.

        Returns
        -------
        list[str]
            List of federation_chess_id values.
        """
        self.chess_players.clear()
        self.load_players_from_json()
        return [player.federation_chess_id for player in self.chess_players]

    def transform_players_id_list(self, players_id):
        """
        Parse a comma-separated string of player IDs and classify them.

        Parameters
        ----------
        players_id : str
            Comma-separated IDs entered by the user.

        Returns
        -------
        tuple (valid_ids, invalid_ids)
            valid_ids : list[str] IDs that exist in the store.
            invalid_ids : list[str] IDs that were not found.
        """
        self.chess_players.clear()
        self.load_players_from_json()
        players_id_list = [pid.strip() for pid in players_id.split(",") if pid.strip()]
        existing_players_id = self.get_players_id()
        invalid_ids = [pid for pid in players_id_list if pid not in existing_players_id]
        valid_ids = [pid for pid in players_id_list if pid in existing_players_id]
        return valid_ids, invalid_ids

    def get_player_by_federation_id(self, federation_id):
        """
        Retrieve a player by their federation chess ID.

        Parameters
        ----------
        federation_id : str
            The federation_chess_id of the player to find.

        Returns
        -------
        ChessPlayer | None
            The matching player instance, or None if not found.
        """
        self.chess_players.clear()
        self.load_players_from_json()
        for player in self.chess_players:
            if player.federation_chess_id == federation_id:
                return player
        return None

    def update_player_by_federation_id(self, federation_id, player1):
        """
        Update a player's ELO and/or games played by their federation chess ID.

        Parameters
        ----------
        federation_id : str
            The federation_chess_id of the player to locate.
        player1 : object
            Object supplying new values. Expected attributes (optional):
                - elo (int | float | None): New ELO rating to assign.
                - games_played (int | None): New total number of games played.

        Returns
        -------
        bool
            True if a matching player was found and updated (and changes saved),
            False if no player with the given federation_id was found.

        Notes
        -----
        The method reloads the players from persistent storage, applies any
        provided updates to the matching player, persists the list back to
        storage, and returns whether an update occurred.
        """
        self.chess_players.clear()
        self.load_players_from_json()
        for player in self.chess_players:
            if player.federation_chess_id == federation_id:
                if player1.games_played is not None:
                    player.modify_games_played(player1.games_played)
                if player1.elo is not None:
                    player.modify_elo(player1.elo)
                self.save_players_to_json()
                return True
        return False

    def update_players_games_and_elo(self, tournament):
        """
        Update all players' games played and ELO ratings based on tournament results.

        For each match in each round the method:
          - looks up the two players by federation ID,
          - computes new ELOs using calculate_elo() and each player's K-factor,
          - increments games_played,
          - updates in-memory player objects and persists changes.

        Parameters
        ----------
        tournament : Tournament
            The tournament instance containing rounds and matches to process.

        Notes
        -----
        The method expects `tournament.rounds` to contain rounds with `.matches`
        where each match is represented as ([player1_id, score1], [player2_id, score2]).
        """
        for round in tournament.rounds:
            for match in round.matches:
                player1_id = match[0][0]
                player2_id = match[1][0]
                result1 = match[0][1]
                result2 = match[1][1]

                player1 = self.get_player_by_federation_id(player1_id)
                player2 = self.get_player_by_federation_id(player2_id)

                new_elo_player1 = calculate_elo(
                    elo_player=player1.elo,
                    elo_opponent=player2.elo,
                    k_player=player1.coef_k,
                    w=result1
                )
                new_elo_player2 = calculate_elo(
                    elo_player=player2.elo,
                    elo_opponent=player1.elo,
                    k_player=player2.coef_k,
                    w=result2
                )

                player1.modify_games_played(player1.games_played + 1)
                player2.modify_games_played(player2.games_played + 1)

                player1.modify_elo(new_elo_player1)
                player2.modify_elo(new_elo_player2)

                self.update_player_by_federation_id(player1_id, player1)
                self.update_player_by_federation_id(player2_id, player2)

    def save_players_to_json(self, filepath="data/players.json"):
        """
        Persist the in-memory players list to a JSON file.

        Parameters
        ----------
        filepath : str
            Destination path for the JSON file.
        """
        data = []
        for player in self.chess_players:
            data.append(player.to_dict())
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_players_from_json(self, filepath="data/players.json"):
        """
        Load players from a JSON file into the in-memory list.

        Parameters
        ----------
        filepath : str
            Path to the JSON file to read.

        Notes
        -----
        If the file does not exist or contains invalid JSON, the method
        silently leaves the in-memory list empty.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data_loaded = json.load(f)
                for player_data in data_loaded:
                    player = ChessPlayer.from_dict(player_data)
                    self.chess_players.append(player)

        except (FileNotFoundError, json.JSONDecodeError):
            pass
