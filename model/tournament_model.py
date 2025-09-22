from datetime import datetime


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
        current_round=1,
        number_of_rounds=4,
        status="À venir",
    ):
        self.name = name
        self.location = location
        self.start_date = start_date if start_date else datetime.now().strftime("%Y-%m-%d")
        self.end_date = end_date if end_date else ""
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.rounds = rounds if rounds is not None else []
        self.players = players if players is not None else []
        self.description = description
        self.status = status  # e.g., "À venir", "En cours", "Terminé"

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "rounds": [r.to_dict() for r in self.rounds],
            "players": self.players, # List of player IDs and not player objects
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data):
        rounds = [TournamentRound.from_dict(r) for r in data.get("rounds", [])]
        return cls(
            name=data.get("name"),
            location=data.get("location"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            players=data.get("players", []),
            description=data.get("description", ""),
            rounds=rounds,
            current_round=data.get("current_round", 1),
            number_of_rounds=data.get("number_of_rounds", 4),
        )


class TournamentRound:
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
        )