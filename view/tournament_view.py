from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

class TournamentView:
    def __init__(self):
        self.console = Console()

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

    def display_exit_message(self):
        self.console.print(Align.center("[bold red]Retour au menu principal ![/bold red]"))

    def display_invalid_choice_message(self):
        self.console.print(Align.center("[bold red]Choix invalide, veuillez réessayer.[/bold red]"))

    def display_section_message(self, section_name):
        self.console.print(Align.center(f"[bold magenta]{section_name}[/bold magenta]"))