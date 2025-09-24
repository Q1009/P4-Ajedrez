from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich import box

class TournamentView:
    def __init__(self, tournament_controller):
        self.console = Console()
        self.tournament_controller = tournament_controller  

    def display_tournament_menu_view(self):
        table = Table(title="Menu Tournois", show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Afficher les tournois")
        table.add_row("[bold cyan]2.[/bold cyan] Créer un tournoi")
        table.add_row("[bold cyan]3.[/bold cyan] Modifier un tournoi")
        table.add_row("[bold cyan]4.[/bold cyan] Mettre à jour un tournoi")
        table.add_row("[bold cyan]5.[/bold cyan] Supprimer un tournoi")
        table.add_row("[bold cyan]6.[/bold cyan] Retour")
        panel = Panel(
            table,
            title="[bold yellow]Gestion des Tournois[/bold yellow]",
            border_style="gold1",
            )
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def display_display_tournaments_view(self, tournaments):

        table = Table(
            title=None,
            show_header=True,
            header_style="bold blue",
            show_lines=True,
            box=box.SQUARE_DOUBLE_HEAD,
        )
        table.add_column("Index", style="dim")
        table.add_column("ID", style="steel_blue3")
        table.add_column("Statut", style="green_yellow")
        table.add_column("Nom", style="cyan")
        table.add_column("Lieu", style="cyan")
        table.add_column("Date de Début", style="magenta")
        table.add_column("Date de Fin", style="magenta")
        table.add_column("Nombre de Joueurs", style="green")
        table.add_column("Nombre de Rounds", style="green")
        table.add_column("Round Actuel", style="green")
        table.add_column("Description", style="dark_orange")

        for index, tournament in enumerate(tournaments):
            table.add_row(
                str(index),
                tournament.tournament_id,
                tournament.status,
                tournament.name,
                tournament.location,
                tournament.start_date,
                tournament.end_date,
                str(len(tournament.players)),
                str(len(tournament.rounds)),
                str(tournament.current_round),
                tournament.description,
            )
        
        panel = Panel(
            table, title="[bold yellow]Liste des Tournois[/bold yellow]",
            subtitle="Appuyez sur 'b' pour revenir au menu précédent",
            border_style="gold1",
        )
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def display_modify_tournament_view(self, index, name):
        table = Table(title=str(index) + " : " + name, show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Modifier le nom")
        table.add_row("[bold cyan]2.[/bold cyan] Modifier le lieu")
        table.add_row("[bold cyan]3.[/bold cyan] Modifier la date de début")
        table.add_row("[bold cyan]4.[/bold cyan] Modifier la date de fin")
        table.add_row("[bold cyan]5.[/bold cyan] Modifier la description")
        table.add_row("[bold cyan]6.[/bold cyan] Retour")
        panel = Panel(
            table,
            title=f"[bold yellow]Modification Tournoi[/bold yellow]",
            border_style="gold1",
        )
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def get_new_tournament_details(self):
        name = self.console.input("Nom du tournoi : ")
        location = self.console.input("Lieu : ")
        start_date = self.console.input("Date de début (YYYY-MM-DD) : ")
        end_date = self.console.input("Date de fin (YYYY-MM-DD) : ")
        description = self.console.input("Description du tournoi : ")
        return name, location, start_date, end_date, description

    def execute(self):
        running = True
        while running:
            self.display_tournament_menu_view()
            choice = self.console.input("\n[bold green]Sélectionnez une option (1-6) : [/bold green]")
            if choice == "1":
                while True:
                    self.display_display_tournaments_view(self.tournament_controller.display_tournaments())
                    tournament_list_choice = self.console.input("\n[bold green]Sélectionnez une action : [/bold green]")
                    if tournament_list_choice.lower() == 'b':
                        break
            elif choice == "2":
                self.display_section_message("Créer un tournoi")
                name, location, start_date, end_date, description = self.get_new_tournament_details()
                self.tournament_controller.add_tournament(name, location, start_date, end_date, description)
                self.display_tournament_added_message(name)
            elif choice == "3":
                self.display_section_message("Modifier un tournoi")
                tournaments_count = self.tournament_controller.get_tournaments_count()
                if tournaments_count == 0:
                    self.display_empty_tournament_modify_list_message()
                    break
                try:
                    index = int(self.console.input(f"Index du tournoi à modifier (0-{tournaments_count - 1}): "))
                    while True:
                        tournament = self.tournament_controller.get_tournament(index)
                        self.display_modify_tournament_view(index, tournament.name)
                        modify_choice = self.console.input("\n[bold green]Sélectionnez une action (1-6) : [/bold green]")
                        if modify_choice == "1":
                            self.console.print(f"Ancien nom : {tournament.name}", style="dim")
                            name = self.console.input("Nouveau nom : ")
                            self.tournament_controller.modify_tournament(index, name=name)
                            self.display_tournament_modified_message(index)
                        elif modify_choice == "2":
                            self.console.print(f"Ancien lieu : {tournament.location}", style="dim")
                            location = self.console.input("Nouveau lieu : ")
                            self.tournament_controller.modify_tournament(index, location=location)
                            self.display_tournament_modified_message(index)
                        elif modify_choice == "3":
                            self.console.print(f"Ancienne date de début : {tournament.start_date}", style="dim")
                            start_date = self.console.input("Nouvelle date de début (YYYY-MM-DD) : ")
                            self.tournament_controller.modify_tournament(index, start_date=start_date)
                            self.display_tournament_modified_message(index)
                        elif modify_choice == "4":
                            self.console.print(f"Ancienne date de fin : {tournament.end_date}", style="dim")
                            end_date = self.console.input("Nouvelle date de fin (YYYY-MM-DD) : ")
                            self.tournament_controller.modify_tournament(index, end_date=end_date)
                            self.display_tournament_modified_message(index)
                        elif modify_choice == "5":
                            self.console.print(f"Ancienne description : {tournament.description}", style="dim")
                            description = self.console.input("Nouvelle description : ")
                            self.tournament_controller.modify_tournament(index, description=description)
                            self.display_tournament_modified_message(index)
                        elif modify_choice == "6":
                            break
                        else:
                            self.display_invalid_choice_message()
                except ValueError:
                    self.display_index_value_error_message()
                except IndexError:
                    self.display_tournament_index_error_message()
            elif choice == "4":
                """
                self.display_section_message("Mettre à jour un tournoi")
                # Logique pour mettre à jour un tournoi (par exemple, avancer le round)
                index = int(self.tournament_view.console.input("Index du tournoi à mettre à jour: "))
                # Exemple simple d'incrémentation du round actuel
                if 0 <= index < len(self.tournaments):
                    current_round = self.tournaments[index].current_round
                    self.modify_tournament(index, current_round=current_round + 1)
                    """
            elif choice == "5":
                self.display_section_message("Supprimer un tournoi")
                tournaments_count = self.tournament_controller.get_tournaments_count()
                if tournaments_count == 0:
                    self.display_empty_tournament_remove_list_message()
                    break
                try:
                    index = int(self.console.input(f"Index du tournoi à supprimer (0-{tournaments_count - 1}): "))
                    name, tournament_id = self.tournament_controller.remove_tournament(index)
                    self.display_tournament_removed_message(tournament_id, name)
                except ValueError:
                    self.display_index_value_error_message()
                except IndexError:
                    self.display_tournament_index_error_message()
            elif choice == "6":
                running = False
            else:
                self.display_invalid_choice_message()

    def display_exit_message(self):
        self.console.print(Align.center("[bold red]Retour au menu principal ![/bold red]"))

    def display_invalid_choice_message(self):
        self.console.print(Align.center("[bold red]Choix invalide, veuillez réessayer.[/bold red]"))

    def display_section_message(self, section_name):
        self.console.print(Align.center(f"[bold magenta]{section_name}[/bold magenta]"))

    def display_index_value_error_message(self):
        self.console.print(Align.center("[bold red]Entrée invalide, veuillez entrer un nombre entier pour l'index.[/bold red]"))
        
    def display_tournament_index_error_message(self):
        self.console.print(Align.center("[bold red]Index invalide. Aucune action effectuée.[/bold red]"))

    def display_tournament_added_message(self, name):
        self.console.print(Align.center(f"[bold green]Le tournoi : {name} a été ajouté avec succès ![/bold green]"))

    def display_tournament_removed_message(self, tournament_id, name):
        self.console.print(Align.center(f"[bold red]Le tournoi {tournament_id} : {name} a été supprimé avec succès ![/bold red]"))

    def display_tournament_modified_message(self, index):
        self.console.print(Align.center(f"[bold blue]Le tournoi à l'index {index} a été modifié avec succès ![/bold blue]"))

    def display_empty_tournament_modify_list_message(self):
        self.console.print(Align.center("[bold yellow]Aucun tournoi disponible pour modification.[/bold yellow]"))

    def display_empty_tournament_remove_list_message(self):
        self.console.print(Align.center("[bold yellow]Aucun tournoi disponible pour suppression.[/bold yellow]"))