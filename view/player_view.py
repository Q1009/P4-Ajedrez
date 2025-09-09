from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

class PlayerView:
    def __init__(self):
        self.console = Console()

    def display_player_view(self):
        table = Table(title="Menu Joueurs", show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Ajouter un joueur")
        table.add_row("[bold cyan]2.[/bold cyan] Supprimer un joueur")
        table.add_row("[bold cyan]3.[/bold cyan] Modifier un joueur")
        table.add_row("[bold cyan]4.[/bold cyan] Retour")
        panel = Panel(table, title="[bold yellow]Gestion des Joueurs[/bold yellow]", border_style="magenta")
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)