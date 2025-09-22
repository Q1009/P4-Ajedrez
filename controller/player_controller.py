import json
from model.player_model import ChessPlayer, ChessClubMember

class ChessPlayerController:

    def __init__(self):
        """Initialise le model ChessPlayer."""
        self.chess_players = []

    def display_players_from_json(self, filepath="data/players.json"):
        self.chess_players.clear()
        self.load_players_from_json()
        return self.chess_players

    def add_player(self, surname, name, date_of_birth, id, elo):
        self.chess_players.clear()
        self.load_players_from_json()
        new_player = ChessPlayer(surname, name, date_of_birth, id, elo)
        self.chess_players.append(new_player)
        self.save_players_to_json()

    def remove_player(self, index):
        self.chess_players.clear()
        self.load_players_from_json()
        removed_player = self.chess_players.pop(index)
        self.save_players_to_json()
        return removed_player.name, removed_player.surname

    def modify_player(self, index, surname=None, name=None, date_of_birth=None, federation_chess_id=None, elo=None):
        self.chess_players.clear()
        self.load_players_from_json()
        player = self.chess_players[index]
        if surname:
            player.surname = surname
        if name:
            player.name = name
        if date_of_birth:
            player.date_of_birth = date_of_birth
        if id:
            player.federation_chess_id = federation_chess_id
        if elo:
            player.elo = elo
        self.save_players_to_json()

    def get_player(self, index):
        self.chess_players.clear()
        self.load_players_from_json()
        return self.chess_players[index]

    def save_players_to_json(self, filepath="data/players.json"):
        data = []
        for member in self.chess_players:
            player = member.to_dict()
            data.append(player)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_players_from_json(self, filepath="data/players.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data_loaded = json.load(f)
                    for player_data in data_loaded:
                        player = ChessPlayer.from_dict(player_data)
                        self.chess_players.append(player)

            except (FileNotFoundError, json.JSONDecodeError):
                print("Aucun joueur trouvé dans le fichier JSON.")
                data = []
                return data