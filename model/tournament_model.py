from datetime import datetime
from utils.unique_id_generator import generate_unique_id


class Tournament:
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
        status="À venir",
        tournament_id=None,
    ):
        self.name = name
        self.location = location
        self.start_date = start_date if start_date else ""
        self.end_date = end_date if end_date else ""
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round if current_round is not None else ""
        self.rounds = rounds if rounds is not None else []
        self.players = players if players is not None else []
        self.description = description
        self.status = status # e.g., "À venir", "En cours", "Terminé"
        self.tournament_id = tournament_id if tournament_id else generate_unique_id()

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "rounds": self.rounds, #[r.to_dict() for r in self.rounds],
            "players": self.players, # List of player IDs and not player objects
            "description": self.description,
            "status": self.status,
            "tournament_id": self.tournament_id,
        }

    @classmethod
    def from_dict(cls, data):
        #rounds = [TournamentRound.from_dict(r) for r in data.get("rounds", [])]
        return cls(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            players=data["players"],
            rounds=data["rounds"],
            current_round=data["current_round"],
            number_of_rounds=data["number_of_rounds"],
            description=data["description"],
            status=data["status"],
            tournament_id=data["tournament_id"],
        )


"""class TournamentRound:
    def __init__(self, round_number, matches=None, name=None, start_date=None, start_time=None, end_date=None, end_time=None):
        self.name = name if name else "Round " + str(round_number)
        now = datetime.now()
        self.start_date = start_date if start_date else now.strftime("%Y-%m-%d")
        self.start_time = start_time if start_time else now.strftime("%H:%M:%S")
        self.end_date = end_date
        self.end_time = end_time
        self.matches = matches if matches is not None else []

    def to_dict(self):
        return {
            #générer un id unique (voir lib)
            "name": self.name,
            "start_date": self.start_date,
            "start_time": self.start_time,
            "end_date": self.end_date,
            "end_time": self.end_time,
            "matches": self.matches,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            round_number=0,  # round_number is not used if name is provided
            name=data["name"],
            start_date=["start_date"],
            start_time=data["start_time"],
            end_date=data["end_date"],
            end_time=data["end_time"],
            matches=data["matches", []],
        )"""