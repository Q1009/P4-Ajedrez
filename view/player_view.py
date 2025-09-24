from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

class PlayerView:
    def __init__(self, player_controller):
        self.console = Console()
        self.player_controller = player_controller


    def display_player_menu_view(self):
        table = Table(title="Menu Joueurs", show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Afficher les joueurs")
        table.add_row("[bold cyan]2.[/bold cyan] Ajouter un joueur")
        table.add_row("[bold cyan]3.[/bold cyan] Supprimer un joueur")
        table.add_row("[bold cyan]4.[/bold cyan] Modifier un joueur")
        table.add_row("[bold cyan]5.[/bold cyan] Retour")
        panel = Panel(table, title="[bold yellow]Gestion des Joueurs[/bold yellow]", border_style="magenta")
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def display_display_players_view(self, players):

        table = Table(title=None, show_header=True, header_style="bold blue")
        table.add_column("Index", style="dim", width=6)
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("Date de Naissance", style="magenta")
        table.add_column("ID Fédération", style="green")
        table.add_column("Elo", style="dark_orange")


        for index, player in enumerate(players):
            table.add_row(str(index), player.surname, player.name, player.date_of_birth, player.federation_chess_id, str(player.elo))
        
        panel = Panel(table, title="[bold yellow]Liste des Joueurs[/bold yellow]", subtitle="Appuyez sur 'b' pour revenir au menu précédent", border_style="magenta")
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def display_modify_player_view(self, index, surname, name):
        table = Table(title=str(index) + " : " + name + " " + surname, show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Modifier le nom")
        table.add_row("[bold cyan]2.[/bold cyan] Modifier le prénom")
        table.add_row("[bold cyan]3.[/bold cyan] Modifier la date de naissance")
        table.add_row("[bold cyan]4.[/bold cyan] Modifier l'ID fédération")
        table.add_row("[bold cyan]5.[/bold cyan] Modifier l'elo")
        table.add_row("[bold cyan]6.[/bold cyan] Retour")
        panel = Panel(
            table,
            title="[bold yellow]Modification Joueur[/bold yellow]",
            border_style="magenta",
            )
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def get_new_player_details(self):
        surname = self.console.input("Nom de famille : ")
        name = self.console.input("Prénom : ")
        date_of_birth = self.console.input("Date de naissance (YYYY-MM-DD) : ")
        federation_chess_id = self.console.input("Identifiant fédération : ")
        elo_nok = True
        while elo_nok:
            elo_input = self.console.input("ELO (1000-2500) : ")
            try:
                elo = int(elo_input)
                if elo < 1000 or elo > 2500:
                    self.display_elo_value_error_message()
                else:
                    elo_nok = False
            except ValueError:
                self.display_elo_value_error_message()

        return surname, name, date_of_birth, federation_chess_id, elo

    def get_user_input(self, prompt):
        return self.console.input(prompt)
    
    def execute(self):
        running = True
        while running:
            self.display_player_menu_view()
            player_choice = self.console.input("\n[bold green]Sélectionnez une action (1-5) : [/bold green]")
            if player_choice == "1":
                while True:
                    self.display_display_players_view(self.player_controller.display_players_from_json())
                    player_list_choice = self.console.input("\n[bold green]Sélectionnez une action : [/bold green]")
                    if player_list_choice.lower() == "b":
                        break
            elif player_choice == "2":
                self.display_section_message("Ajouter un joueur")
                surname, name, date_of_birth, federation_chess_id, elo = self.get_new_player_details()
                self.player_controller.add_player(surname, name, date_of_birth, federation_chess_id, elo)
                self.display_player_added_message(name, surname)
            elif player_choice == "3":
                self.display_section_message("Supprimer un joueur")
                players_count = self.player_controller.get_players_count()
                if players_count == 0:
                    self.display_empty_player_remove_list_message()
                    break
                try:
                    index = int(self.console.input(f"Index du joueur à supprimer (0-{players_count - 1}): "))
                    try:
                        name, surname = self.player_controller.remove_player(index)
                        self.display_player_removed_message(name, surname)
                    except IndexError:
                        self.display_player_index_error_message()
                except ValueError:
                    self.display_value_error_message()
            elif player_choice == "4":
                self.display_section_message("Modifier un joueur")
                players_count = self.player_controller.get_players_count()
                if players_count == 0:
                    self.display_empty_player_modify_list_message()
                    break
                try:
                    index = int(self.console.input(f"Index du joueur à modifier (0-{players_count - 1}): "))
                    while True:
                        player = self.player_controller.get_player(index)  # Vérifie si l'index est valide
                        self.display_modify_player_view(index, player.surname, player.name)
                        modify_choice = self.console.input("\n[bold green]Sélectionnez une action (1-6) : [/bold green]")
                        if modify_choice == "1":
                            self.console.print(f"Ancien nom : {player.surname}", style="dim")
                            surname = self.console.input("Nouveau nom : ")
                            self.player_controller.modify_player(index, surname=surname)
                            self.display_player_modified_message(index)
                        elif modify_choice == "2":
                            self.console.print(f"Ancien prénom : {player.name}", style="dim")
                            name = self.console.input("Nouveau prénom : ")
                            self.player_controller.modify_player(index, name=name)
                            self.display_player_modified_message(index)
                        elif modify_choice == "3":
                            self.console.print(f"Ancienne date de naissance : {player.date_of_birth}", style="dim")
                            date_of_birth = self.console.input("Nouvelle date de naissance (YYYY-MM-DD) : ")
                            self.player_controller.modify_player(index, date_of_birth=date_of_birth)
                            self.display_player_modified_message(index)
                        elif modify_choice == "4":
                            self.console.print(f"Ancien ID fédération : {player.federation_chess_id}", style="dim")
                            federation_chess_id = self.console.input("Nouveau ID fédération : ")
                            self.player_controller.modify_player(index, federation_chess_id=federation_chess_id)
                            self.display_player_modified_message(index)
                        elif modify_choice == "5":
                            elo_nok = True
                            while elo_nok:
                                self.console.print(f"Ancien Elo : {player.elo}", style="dim")
                                elo_input = self.console.input("Nouvel Elo (1000-2500) : ")
                                try:
                                    elo = int(elo_input)
                                    if elo < 1000 or elo > 2500:
                                        self.display_elo_value_error_message()
                                    else:
                                        elo_nok = False
                                except ValueError:
                                    self.display_elo_value_error_message()
                            self.player_controller.modify_player(index, elo=elo)
                            self.display_player_modified_message(index)
                        elif modify_choice == "6":
                            break
                        else:
                            self.display_invalid_choice_message()
                except ValueError:
                    self.display_value_error_message()
                except IndexError:
                    self.display_player_index_error_message()
            elif player_choice == "5":
                running = False
            else:
                self.display_invalid_choice_message()
    
    def display_player_added_message(self, name, surname):
        self.console.print(Align.center(f"[bold green]Le joueur {name} {surname} a été ajouté avec succès ![/bold green]"))

    def display_player_removed_message(self, name, surname):
        self.console.print(Align.center(f"[bold red]Le joueur {name} {surname} a été supprimé avec succès ![/bold red]"))
        
    def display_player_index_error_message(self):
        self.console.print(Align.center("[bold red]Index invalide. Aucune action effectuée.[/bold red]"))

    def display_player_modified_message(self, index):
        self.console.print(Align.center(f"[bold blue]Le joueur à l'index {index} a été modifié avec succès ![/bold blue]"))

    def display_exit_message(self):
        self.console.print(Align.center("[bold red]Au revoir ![/bold red]"))

    def display_invalid_choice_message(self):
        self.console.print(Align.center("[bold red]Choix invalide, veuillez réessayer.[/bold red]"))

    def display_section_message(self, section_name):
        self.console.print(Align.center(f"[bold magenta]{section_name}[/bold magenta]"))

    def display_value_error_message(self):
        self.console.print(Align.center("[bold red]Entrée invalide, veuillez entrer un nombre entier pour l'index.[/bold red]"))

    def display_elo_value_error_message(self):
        self.console.print(Align.center("[bold red]ELO invalide. Veuillez entrer un nombre entier entre 1000 et 2500.[/bold red]"))

    def display_empty_player_remove_list_message(self):
        self.console.print(Align.center("[bold magenta]Aucun joueur disponible pour suppression.[/bold magenta]"))

    def display_empty_player_modify_list_message(self):
        self.console.print(Align.center("[bold magenta]Aucun joueur disponible pour modification.[/bold magenta]"))