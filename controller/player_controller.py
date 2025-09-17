import json
from view.menu_view import MenuView
from view.player_view import PlayerView
from model.player_model import ChessPlayer, ChessClubMember

class ChessPlayerController:

    def __init__(self, player_view):
        """Initialise le model ChessPlayer."""
        self.player_view = player_view
        self.chess_players = ChessClubMember()

    def display_players_from_json(self, filepath="data/players.json"):
        self.load_players_from_json()
        self.player_view.display_display_players_view(self.chess_players.chess_club_members)
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
            self.player_view.display_player_removed_message(removed_player.name, removed_player.surname)
        except IndexError:
            self.player_view.display_player_index_error_message()
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
            self.player_view.display_player_modified_message(player.name, player.surname)     
        except IndexError:
            self.player_view.display_player_index_error_message()
        
        self.save_players_to_json()
        self.chess_players.chess_club_members.clear()


    def save_players_to_json(self, filepath="data/players.json"):
        data = []
        for member in self.chess_players.chess_club_members:
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
                        self.chess_players.chess_club_members.append(player)

            except (FileNotFoundError, json.JSONDecodeError):
                print("Aucun joueur trouvé dans le fichier JSON.")
                data = []
                return data
            
    def execute(self):
        running = True
        while running:
            self.player_view.display_player_menu_view()
            player_choice = self.player_view.console.input("\n[bold green]Sélectionnez une action (1-5) : [/bold green]")
            if player_choice == "1":
                while True:
                    self.display_players_from_json()
                    player_list_choice = self.player_view.console.input("\n[bold green]Sélectionnez une action : [/bold green]")
                    if player_list_choice == "b":
                        break
            elif player_choice == "2":
                self.player_view.display_section_message("Ajouter un joueur")
                surname, name, date_of_birth, federation_chess_id, elo = self.player_view.get_new_player_details()
                self.add_player(surname, name, date_of_birth, federation_chess_id, elo)
                self.player_view.console.print(f"[bold green]Le joueur {name} {surname} a été ajouté avec succès ![/bold green]")
            elif player_choice == "3":
                self.player_view.display_section_message("Supprimer un joueur")
                try:
                    index = int(self.player_view.console.input("Index du joueur à supprimer : "))
                    self.remove_player(index)
                except ValueError:
                    self.player_view.display_value_error_message()
            elif player_choice == "4":
                self.player_view.display_section_message("Modifier un joueur")
                try:
                    index = int(self.player_view.console.input("Index du joueur à modifier : "))
                    while True:
                        self.player_view.display_modify_player_view(index)
                        modify_choice = self.player_view.console.input("\n[bold green]Sélectionnez une action (1-6) : [/bold green]")
                        if modify_choice == "1":
                            surname = self.player_view.console.input("Nouveau nom : ")
                            self.modify_player(index, surname=surname)
                        elif modify_choice == "2":
                            name = self.player_view.console.input("Nouveau prénom : ")
                            self.modify_player(index, name=name)
                        elif modify_choice == "3":
                            date_of_birth = self.player_view.console.input("Nouvelle date de naissance (YYYY-MM-DD) : ")
                            self.modify_player(index, date_of_birth=date_of_birth)
                        elif modify_choice == "4":
                            federation_chess_id = self.player_view.console.input("Nouveau identifiant fédération : ")
                            self.modify_player(index, federation_chess_id=federation_chess_id)
                        elif modify_choice == "5":
                            elo = self.player_view.console.input("Nouvel Elo : ")
                            self.modify_player(index, elo=elo)
                        elif modify_choice == "6":
                            break
                        else:
                            self.player_view.display_invalid_choice_message()
                except ValueError:
                    self.player_view.display_value_error_message()
            elif player_choice == "5":
                running = False
            else:
                self.player_view.display_invalid_choice_message()