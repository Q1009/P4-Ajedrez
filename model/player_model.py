class ChessPlayer:
    """Represent a chess player with personal data and rank."""

    def __init__(self, surname, name, date_of_birth, id, elo):
        """
        Initialize a ChessPlayer.

        Args:
            surname (str): Player's family name / last name.
            name (str): Player's given name / first name.
            date_of_birth (str): Date of birth.
            id (str): Federation chess identifier (unique ID)
            elo (int | float): Player's ELO / rank.
        """
        self.surname = surname
        self.name = name
        self.date_of_birth = date_of_birth
        self.federation_chess_id = id
        self.elo = elo

    def to_dict(self):
        """
        Return a dictionary representation of the player.

        Useful for JSON serialization in order to save data.
        """
        return {
            "surname": self.surname,
            "name": self.name,
            "date_of_birth": self.date_of_birth,
            "federation_chess_id": self.federation_chess_id,
            "elo": self.elo
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a ChessPlayer instance from a dictionary.

        Useful for JSON deserialization in order to load data.
        """
        return cls(
            surname=data["surname"],
            name=data["name"],
            date_of_birth=data["date_of_birth"],
            id=data["federation_chess_id"],
            elo=data["elo"]
        )
