import json
from view.menu_view import MenuView
from view.player_view import PlayerView
from model.player_model import ChessPlayer, ChessClubMember

class ChessPlayerController:

    def __init__(self):
        """Initialise le model ChessPlayer."""
        self.chess_players = ChessClubMember()

        self.ui = PlayerView()

    def display_players_from_json(self, filepath="data/players.json"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.ui.display_players(data)

        except (FileNotFoundError, json.JSONDecodeError):
            data = []
            return

    def add_player(self, surname, name, date_of_birth, id, elo):
        new_player = ChessPlayer(surname, name, date_of_birth, id, elo)
        self.chess_players.chess_players.append(new_player)
        self.ui.console.print(f"[bold green]Le joueur {name} {surname} a été ajouté avec succès ![/bold green]")

    def remove_player(self, index):
        try:
            removed_player = self.chess_players.chess_players.pop(index)
            self.ui.console.print(f"[bold green]Le joueur {removed_player.name} {removed_player.surname} a été supprimé avec succès ![/bold green]")
        except IndexError:
            self.ui.console.print("[bold red]Index invalide. Aucun joueur supprimé.[/bold red]")

    def modify_player(self, index, surname=None, name=None, date_of_birth=None, id=None, elo=None):
        try:
            player = self.chess_players.chess_players[index]
            if surname:
                player.surname = surname
            if name:
                player.name = name
            if date_of_birth:
                player.date_of_birth = date_of_birth
            if id:
                player.federation_chess_id = id
            if elo:
                player.elo = elo
            self.ui.console.print(f"[bold green]Le joueur {player.name} {player.surname} a été modifié avec succès ![/bold green]")
        except IndexError:
            self.ui.console.print("[bold red]Index invalide. Aucun joueur modifié.[/bold red]")


    def save_players_to_json(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        for player in self.chess_players.chess_players:
            data.append(player)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
