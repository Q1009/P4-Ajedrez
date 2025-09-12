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
        self.load_players_from_json()
        self.ui.display_display_players_view(self.chess_players.chess_club_members)
        self.chess_players.chess_club_members.clear()

    def add_player(self, surname, name, date_of_birth, id, elo):
        self.load_players_from_json()
        new_player = ChessPlayer(surname, name, date_of_birth, id, elo)
        self.chess_players.chess_club_members.append(new_player)
        self.save_players_to_json()
        self.chess_players.chess_club_members.clear()

    def remove_player(self, index):
        self.load_players_from_json()
        try:
            removed_player = self.chess_players.chess_club_members.pop(index)
            self.ui.console.print(f"[bold green]Le joueur {removed_player.name} {removed_player.surname} a été supprimé avec succès ![/bold green]")
        except IndexError:
            self.ui.console.print("[bold red]Index invalide. Aucun joueur supprimé.[/bold red]")
        self.save_players_to_json()
        self.chess_players.chess_club_members.clear()

    def modify_player(self, index, surname=None, name=None, date_of_birth=None, id=None, elo=None):
        self.load_players_from_json()
        try:
            player = self.chess_players.chess_club_members[index]
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
            self.ui.console.print(f"[bold blue]Le joueur {player.name} {player.surname} a été modifié avec succès ![/bold blue]")      
        except IndexError:
            self.ui.console.print("[bold red]Index invalide. Aucun joueur modifié.[/bold red]")
        
        self.save_players_to_json()
        self.chess_players.chess_club_members.clear()


    def save_players_to_json(self, filepath="data/players.json"):
        data = []
        for member in self.chess_players.chess_club_members:
            player = {
                "surname": member.surname,
                "name": member.name,
                "date_of_birth": member.date_of_birth,
                "federation_chess_id": member.federation_chess_id,
                "elo": member.elo
            }
            data.append(player)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_players_from_json(self, filepath="data/players.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data_loaded = json.load(f)
                    for player_data in data_loaded:
                        player = ChessPlayer(
                            surname=player_data["surname"],
                            name=player_data["name"],
                            date_of_birth=player_data["date_of_birth"],
                            id=player_data["federation_chess_id"],
                            elo=player_data["elo"]
                        )
                        self.chess_players.chess_club_members.append(player)
                #return self.chess_players.chess_club_members

            except (FileNotFoundError, json.JSONDecodeError):
                print("Aucun joueur trouvé dans le fichier JSON.")
                data = []
                return data