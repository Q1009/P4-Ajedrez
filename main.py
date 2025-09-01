from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align  # Ajout de l'import

def display_main_menu():
    console = Console()
    table = Table(title="Menu Principal", show_header=True, box=None)
    table.add_row("[bold cyan]1.[/bold cyan] Tournois")
    table.add_row("[bold cyan]2.[/bold cyan] Joueurs")
    table.add_row("[bold cyan]3.[/bold cyan] Rapports")
    table.add_row("[bold cyan]4.[/bold cyan] Quitter")
    panel = Panel(table, title="[bold yellow]AJEDREZ[/bold yellow]", border_style="blue")
    centered_panel = Align.center(panel)  # Centrage du panel
    console.print(centered_panel)

def main():
    console = Console()
    while True:
        display_main_menu()
        choix = console.input("\n[bold green]Sélectionnez une section (1-4) : [/bold green]")
        if choix == "1":
            console.print("[bold magenta]Vous êtes dans la section Tournois.[/bold magenta]")
        elif choix == "2":
            console.print("[bold magenta]Vous êtes dans la section Joueurs.[/bold magenta]")
        elif choix == "3":
            console.print("[bold magenta]Vous êtes dans la section Rapports.[/bold magenta]")
        elif choix == "4":
            console.print("[bold red]Au revoir ![/bold red]")
            break
        else:
            console.print("[bold red]Choix invalide, veuillez réessayer.[/bold red]")

if __name__ == "__main__":
    main()