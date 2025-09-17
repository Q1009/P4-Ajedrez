from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

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

    def display_exit_message(self):
        self.console.print(Align.center("[bold red]Au revoir ![/bold red]"))

    def display_invalid_choice_message(self):
        self.console.print(Align.center("[bold red]Choix invalide, veuillez réessayer.[/bold red]"))

    def display_section_message(self, section_name):
        self.console.print(Align.center(f"[bold magenta]Vous êtes dans la section {section_name}.[/bold magenta]"))