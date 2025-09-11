class ChessPlayer:
    
    def __init__(self, surname, name, date_of_birth, id, elo):
        self.surname = surname
        self.name = name
        self.date_of_birth = date_of_birth
        self.federation_chess_id = id
        self.elo = elo

class ChessClubMember:
    
    def __init__(self):
        self.chess_players = []