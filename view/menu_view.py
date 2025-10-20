from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from view.tournament_view import TournamentView
from controller.tournament_controller import TournamentController
from view.player_view import PlayerView
from controller.player_controller import ChessPlayerController
from view.report_view import ReportView
from controller.report_controller import ReportController

class MenuView:
    def __init__(self):
        self.console = Console()

    def display_menu_view(self):
        table = Table(title="Menu Principal", show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Tournois")
        table.add_row("[bold cyan]2.[/bold cyan] Joueurs")
        table.add_row("[bold cyan]3.[/bold cyan] Rapports")
        table.add_row("[bold cyan]4.[/bold cyan] Quitter")
        panel = Panel(table, title="[bold yellow]AJEDREZ[/bold yellow]", border_style="blue")
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def execute(self):
        
        running = True
        while running:
            self.display_menu_view()
            choice = self.console.input("\n[bold green]Sélectionnez une section (1-4) : [/bold green]")
            if choice == "1":
                # Ajouter la logique pour gérer les tournois ici
                tournament_controller = TournamentController()
                tournament_view = TournamentView(tournament_controller)
                tournament_view.execute()
            elif choice == "2":
                # Ajouter la logique pour gérer les joueurs ici
                player_controller = ChessPlayerController()
                player_view = PlayerView(player_controller)
                player_view.execute()
            elif choice == "3":
                # Ajouter la logique pour gérer les rapports ici
                report_controller = ReportController()
                report_view = ReportView(report_controller)
                report_view.execute()
            elif choice == "4":
                self.display_exit_message()
                running = False
            else:
                self.display_invalid_choice_message()

    def display_exit_message(self):
        self.console.print(Align.center("[bold red]Au revoir ![/bold red]"))

    def display_invalid_choice_message(self):
        self.console.print(Align.center("[bold red]Choix invalide, veuillez réessayer.[/bold red]"))

    def display_section_message(self, section_name):
        self.console.print(Align.center(f"[bold magenta]Vous êtes dans la section {section_name}.[/bold magenta]"))