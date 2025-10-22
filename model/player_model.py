class ChessPlayer:
    """Represent a chess player with personal information, rating and activity.

    Attributes
    ----------
    surname : str
        Family name / last name of the player.
    name : str
        Given name / first name of the player.
    date_of_birth : str
        Player date of birth (stored as string).
    federation_chess_id : str
        Federation identifier for the player.
    elo : int | float
        Current ELO rating.
    coef_k : int
        Coefficient K used for ELO updates (determined by experience / rating).
    games_played : int
        Number of games recorded for this player in the application.

    Methods
    -------
    __init__(surname, name, date_of_birth, id, elo)
        Initialize a new ChessPlayer instance.
    modify_elo(new_elo)
        Update the player's ELO and adjust the K coefficient according to rules.
    modify_games_played(new_games_played)
        Set the player's total games played.
    to_dict()
        Return a JSON-serializable dict representation of the player.
    from_dict(data)
        Class method: construct a ChessPlayer from a dict (deserialization).
    """

    def __init__(self, surname, name, date_of_birth, id, elo, coef_k=40, games_played=0):
        """
        Initialize a ChessPlayer instance.

        Parameters
        ----------
        surname : str
            Player's family name / last name.
        name : str
            Player's given name / first name.
        date_of_birth : str
            Date of birth (string, e.g. "YYYY-MM-DD").
        id : str
            Federation chess identifier (unique).
        elo : int | float
            Initial ELO rating for the player.

        Notes
        -----
        coef_k is initialized to 40 and games_played to 0 by default;
        coef_k may be adjusted later based on games_played and ELO.
        """
        self.surname = surname
        self.name = name
        self.date_of_birth = date_of_birth
        self.federation_chess_id = id
        self.elo = elo
        self.coef_k = coef_k
        self.games_played = games_played

    def modify_elo(self, new_elo):
        """
        Update the player's ELO rating and adjust the K coefficient.

        Parameters
        ----------
        new_elo : int | float
            The new ELO rating to assign.

        Behavior
        --------
        - Sets self.elo to new_elo.
        - Updates self.coef_k according to common rules:
            * coef_k = 40 if games_played < 30
            * coef_k = 20 if games_played >= 30 and elo < 2400
            * coef_k = 10 if elo >= 2400
        """
        self.elo = new_elo
        if self.games_played < 30:
            self.coef_k = 40
        elif self.elo < 2400:
            self.coef_k = 20
        else:
            self.coef_k = 10

    def modify_games_played(self, new_games_played):
        """
        Update the player's total games played.

        Parameters
        ----------
        new_games_played : int
            New total number of games played for this player.
        """
        self.games_played = new_games_played

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
            "elo": self.elo,
            "coef_k": self.coef_k,
            "games_played": self.games_played
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
            elo=data["elo"],
            coef_k=data["coef_k"],
            games_played=data["games_played"]
        )
