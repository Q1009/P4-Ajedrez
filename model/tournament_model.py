from datetime import datetime
from utils.unique_id_generator import generate_unique_id


class Tournament:
    """Represent a tournament with metadata, players, rounds and match history.

    Attributes
    ----------
    name : str
        Tournament name.
    location : str
        Tournament location.
    start_date : str
        Start date (YYYY-MM-DD) or empty string if not set.
    end_date : str
        End date (YYYY-MM-DD) or empty string if not set.
    number_of_rounds : int
        Total number of rounds planned.
    current_round : int | str
        Current round number or identifier (can be empty string).
    matches_history : list
        Historical match records.
    rounds : list
        List of TournamentRound instances.
    players : dict
        Mapping of player_id -> points (float).
    description : str
        Short description of the tournament.
    status : str
        Tournament status (e.g. "À venir", "En cours", "Terminé").
    tournament_id : str
        Unique tournament identifier.

    Methods
    -------
    to_dict():
        Return a serializable dictionary representation of the tournament.
    from_dict(data):
        Create a Tournament instance from a dictionary (deserialisation).
    """

    def __init__(
        self,
        name,
        location,
        start_date=None,
        end_date=None,
        players=None,
        description="",
        rounds=None,
        current_round=None,
        number_of_rounds=4,
        matches_history=None,
        status="À venir",
        tournament_id=None,
    ):
        """
        Initialize a Tournament instance.

        Args:
            name (str): Tournament name.
            location (str): Tournament location.
            start_date (str | None): Start date (YYYY-MM-DD).
            end_date (str | None): End date (YYYY-MM-DD).
            players (dict | None): Mapping of player_id -> points.
            description (str): Short description.
            rounds (list | None): List of TournamentRound objects.
            current_round (int | str | None): Current round number.
            number_of_rounds (int): Total number of rounds planned.
            matches_history (list | None): Historical match records.
            status (str): Tournament status.
            tournament_id (str | None): Uniquely generated ID.
        """
        self.name = name
        self.location = location
        self.start_date = start_date if start_date else ""
        self.end_date = end_date if end_date else ""
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round if current_round is not None else ""
        self.matches_history = matches_history if matches_history else []
        self.rounds = rounds if rounds is not None else []
        self.players = players if players is not None else {}
        self.description = description
        self.status = status
        self.tournament_id = tournament_id if tournament_id else generate_unique_id()

    def to_dict(self):
        """
        Return a dictionary representation of the tournament.

        Useful for JSON serialization in order to save data.

        Converts rounds to dictionaries if they are TournamentRound instances.
        """
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "matches_history": self.matches_history,
            "rounds": self.rounds if not self.rounds else [r.to_dict() for r in self.rounds],
            "players": self.players,
            "description": self.description,
            "status": self.status,
            "tournament_id": self.tournament_id,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Tournament instance from a dictionary.

        Expects keys matching the structure produced by to_dict(). Rounds are
        reconstructed as TournamentRound objects via TournamentRound.r_from_dict.

        Useful for JSON deserialization in order to load data.
        """
        return cls(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            players=data["players"],
            rounds=[TournamentRound.from_dict(r) for r in data["rounds"]],
            current_round=data["current_round"],
            matches_history=data["matches_history"],
            number_of_rounds=data["number_of_rounds"],
            description=data["description"],
            status=data["status"],
            tournament_id=data["tournament_id"],
        )


class TournamentRound:
    """Represent a single round within a tournament, containing matches and timestamps.

    Attributes
    ----------
    name : str
        Human readable name for the round (e.g. "Round 1").
    round_id : str
        Unique identifier for the round.
    start_date : str
        Start date string (YYYY-MM-DD).
    start_time : str
        Start time string (HH:MM:SS).
    end_date : str | None
        End date string or None.
    end_time : str | None
        End time string or None.
    matches : list
        List of match records for the round (each match is expected to be serializable).
    status : str
        Round status string.

    Methods
    -------
    to_dict():
        Return a dictionary representation of the round for serialization.
    from_dict(data):
        Reconstruct a TournamentRound instance from a dictionary.
    """

    def __init__(
        self,
        round_number=None,
        round_id=None,
        start_date=None,
        start_time=None,
        matches=None,
        name=None,
        end_date=None,
        end_time=None,
        status=None
    ):
        """
        Initialize a TournamentRound.

        Args:
            round_number (int | None): Ordinal number of the round; used to build a default name.
            round_id (str | None): Unique identifier for the round; generated if omitted.
            start_date (str | None): Start date string (ISO).
            start_time (str | None): Start time string (HH:MM:SS).
            matches (list | None): List of match records for the round.
            name (str | None): Optional explicit name; if not provided a default 'Round {n}' is used.
            end_date (str | None): End date string.
            end_time (str | None): End time string.
            status (str | None): Round status.
        """
        self.name = f'Round {round_number}' if round_number else ""
        self.round_id = round_id if round_id else generate_unique_id()
        now = datetime.now()
        self.start_date = start_date if start_date else now.strftime(
            "%Y-%m-%d")
        self.start_time = start_time if start_time else now.strftime(
            "%H:%M:%S")
        self.end_date = end_date
        self.end_time = end_time
        self.matches = matches if matches is not None else []
        self.status = status if status else ""

    def to_dict(self):
        """
        Return a dictionary representation of the round.

        Keeps match data as-is (expects matches to be serializable).

        Useful for JSON serialization in order to save data.
        """
        return {
            "name": self.name,
            "round_id": self.round_id,
            "start_date": self.start_date,
            "start_time": self.start_time,
            "end_date": self.end_date,
            "end_time": self.end_time,
            "matches": self.matches,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Reconstruct a TournamentRound instance from a dictionary.

        Useful for JSON serialization in order to save data.
        """
        return cls(
            name=data["name"],
            round_number=data["name"][-1:],
            round_id=data["round_id"],
            start_date=data["start_date"],
            start_time=data["start_time"],
            end_date=data["end_date"],
            end_time=data["end_time"],
            matches=data["matches"],
            status=data["status"],
        )
