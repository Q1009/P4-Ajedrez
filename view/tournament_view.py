from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

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
        panel = Panel(table, title="[bold yellow]Gestion des Tournois[/bold yellow]", border_style="blue")
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def display_display_tournaments_view(self, tournaments):
        if not tournaments:
            self.console.print("[bold yellow]Aucun tournoi disponible.[/bold yellow]")
            return

        table = Table(title=None, show_header=True, header_style="bold blue")
        table.add_column("Index", style="dim", width=6)
        table.add_column("Statut", style="green_yellow", width=6)
        table.add_column("Nom", style="cyan")
        table.add_column("Lieu", style="cyan")
        table.add_column("Date de Début", style="magenta")
        table.add_column("Date de Fin", style="magenta")
        table.add_column("Nombre de Joueurs", style="green")
        table.add_column("Nombre de Rounds", style="green")
        table.add_column("Round Actuel", style="green")
        table.add_column("Description", style="dark_orange")

        for index, tournament in enumerate(tournaments):
            table.add_row(str(index), tournament.status, tournament.name, tournament.location, tournament.start_date, tournament.end_date, str(len(tournament.players)), tournament.description)
        
        panel = Panel(table, title="[bold yellow]Liste des Tournois[/bold yellow]", subtitle="Appuyez sur 'b' pour revenir au menu précédent", border_style="blue")
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def execute(self):
        # À compléter selon la logique de navigation de votre application
        running = True
        while running:
            self.display_tournament_menu_view()
            choice = self.console.input("\n[bold green]Sélectionnez une option (1-6) : [/bold green]")
            if choice == "1":
                self.display_tournaments()
            elif choice == "2":
                self.display_section_message("Créer un tournoi")
                # Logique pour ajouter un tournoi
                name = self.tournament_view.console.input("Nom du tournoi: ")
                location = self.tournament_view.console.input("Lieu du tournoi: ")
                start_date = self.tournament_view.console.input("Date de début (YYYY-MM-DD): ")
                end_date = self.tournament_view.console.input("Date de fin (YYYY-MM-DD): ")
                players = []  # Logique pour ajouter des joueurs
                description = self.tournament_view.console.input("Description du tournoi: ")
                self.add_tournament(name, location, start_date, end_date, players, description)
            elif choice == "3":
                self.display_section_message("Modifier un tournoi")
                # Logique pour modifier un tournoi
                index = int(self.tournament_view.console.input("Index du tournoi à modifier: "))
                name = self.tournament_view.console.input("Nouveau nom du tournoi (laisser vide pour ne pas changer): ")
                location = self.tournament_view.console.input("Nouveau lieu du tournoi (laisser vide pour ne pas changer): ")
                start_date = self.tournament_view.console.input("Nouvelle date de début (YYYY-MM-DD) (laisser vide pour ne pas changer): ")
                end_date = self.tournament_view.console.input("Nouvelle date de fin (YYYY-MM-DD) (laisser vide pour ne pas changer): ")
                description = self.tournament_view.console.input("Nouvelle description du tournoi (laisser vide pour ne pas changer): ")
                updates = {k: v for k, v in {
                    "name": name,
                    "location": location,
                    "start_date": start_date,
                    "end_date": end_date,
                    "description": description
                }.items() if v}
                self.modify_tournament(index, **updates)
            elif choice == "4":
                self.display_section_message("Mettre à jour un tournoi")
                # Logique pour mettre à jour un tournoi (par exemple, avancer le round)
                index = int(self.tournament_view.console.input("Index du tournoi à mettre à jour: "))
                # Exemple simple d'incrémentation du round actuel
                if 0 <= index < len(self.tournaments):
                    current_round = self.tournaments[index].current_round
                    self.modify_tournament(index, current_round=current_round + 1)
            elif choice == "5":
                self.display_section_message("Supprimer un tournoi")
                # Logique pour supprimer un tournoi
                index = int(self.tournament_view.console.input("Index du tournoi à supprimer: "))
                self.remove_tournament(index)
            elif choice == "6":
                running = False
            else:
                self.tournament_view.display_invalid_choice_message()

    def display_exit_message(self):
        self.console.print(Align.center("[bold red]Retour au menu principal ![/bold red]"))

    def display_invalid_choice_message(self):
        self.console.print(Align.center("[bold red]Choix invalide, veuillez réessayer.[/bold red]"))

    def display_section_message(self, section_name):
        self.console.print(Align.center(f"[bold magenta]{section_name}[/bold magenta]"))