class ChessPlayer:
    
    def __init__(self, surname, name, date_of_birth, id, elo):
        self.surname = surname
        self.name = name
        self.date_of_birth = date_of_birth
        self.federation_chess_id = id
        self.elo = elo

    def to_dict(self):
        return {
            "surname": self.surname,
            "name": self.name,
            "date_of_birth": self.date_of_birth,
            "federation_chess_id": self.federation_chess_id,
            "elo": self.elo
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            surname=data["surname"],
            name=data["name"],
            date_of_birth=data["date_of_birth"],
            id=data["federation_chess_id"],
            elo=data["elo"]
        )

class ChessClubMember: #le typer en array de ChessPlayer
    
    def __init__(self):
        self.chess_club_members = []