from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

class PlayerView:
    def __init__(self):
        self.console = Console()

    def display_player_view(self):
        table = Table(title="Menu Joueurs", show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Afficher les joueurs")
        table.add_row("[bold cyan]2.[/bold cyan] Ajouter un joueur")
        table.add_row("[bold cyan]3.[/bold cyan] Supprimer un joueur")
        table.add_row("[bold cyan]4.[/bold cyan] Modifier un joueur")
        table.add_row("[bold cyan]5.[/bold cyan] Retour")
        panel = Panel(table, title="[bold yellow]Gestion des Joueurs[/bold yellow]", border_style="magenta")
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def display_players(self, players):
        if not players:
            self.console.print("[bold yellow]Aucun joueur disponible.[/bold yellow]")
            return

        table = Table(title="Liste des Joueurs", show_header=True, header_style="bold blue")
        table.add_column("Index", style="dim", width=6)
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("Date de Naissance", style="magenta")
        table.add_column("ID Fédération", style="green")
        table.add_column("Elo", style="green")

        for index, player in enumerate(players):
            table.add_row(str(index), player.surname, player.name, player.date_of_birth, player.federation_chess_id, str(player.elo))
        
        centered_table = Align.center(table)
        self.console.print(centered_table)