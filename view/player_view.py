from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

class PlayerView:
    def __init__(self):
        self.console = Console()

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
        if not players:
            self.console.print("[bold yellow]Aucun joueur disponible.[/bold yellow]")
            return

        table = Table(title="Liste des Joueurs", show_header=True, header_style="bold blue")
        table.add_column("Index", style="dim", width=6)
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("Date de Naissance", style="magenta")
        table.add_column("ID Fédération", style="green")
        table.add_column("Elo", style="dark_orange")

        for index, player in enumerate(players):
            table.add_row(str(index), player.surname, player.name, player.date_of_birth, player.federation_chess_id, str(player.elo))
        
        centered_table = Align.center(table)
        self.console.print(centered_table)

    def display_modify_player_view(self, index):
        table = Table(title="Modifier un joueur", show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Modifier le nom")
        table.add_row("[bold cyan]2.[/bold cyan] Modifier le prénom")
        table.add_row("[bold cyan]3.[/bold cyan] Modifier la date de naissance")
        table.add_row("[bold cyan]4.[/bold cyan] Modifier l'ID Fédération")
        table.add_row("[bold cyan]5.[/bold cyan] Modifier l'Elo")
        table.add_row("[bold cyan]6.[/bold cyan] Retour")
        panel = Panel(table, title="[bold yellow]Modification Joueur[/bold yellow]", border_style="magenta")
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)