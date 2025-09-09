from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

def display_main_menu():
    console = Console()
    table = Table(title="Menu Principal", show_header=False, box=None)
    table.add_row("[bold cyan]1.[/bold cyan] Tournois")
    table.add_row("[bold cyan]2.[/bold cyan] Joueurs")
    table.add_row("[bold cyan]3.[/bold cyan] Rapports")
    table.add_row("[bold cyan]4.[/bold cyan] Quitter")
    panel = Panel(table, title="[bold yellow]AJEDREZ[/bold yellow]", border_style="blue")
    centered_panel = Align.center(panel)
    console.print(centered_panel)

def display_player_menu():
    console = Console()
    table = Table(title="Menu Joueurs", show_header=False, box=None)
    table.add_row("[bold cyan]1.[/bold cyan] Ajouter un joueur")
    table.add_row("[bold cyan]2.[/bold cyan] Supprimer un joueur")
    table.add_row("[bold cyan]3.[/bold cyan] Modifier un joueur")
    table.add_row("[bold cyan]4.[/bold cyan] Retour")
    panel = Panel(table, title="[bold yellow]Gestion des Joueurs[/bold yellow]", border_style="magenta")
    centered_panel = Align.center(panel)
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
            while True:
                display_player_menu()
                choix_joueur = console.input("\n[bold green]Sélectionnez une action (1-4) : [/bold green]")
                if choix_joueur == "1":
                    console.print("[bold magenta]Ajouter un joueur sélectionné.[/bold magenta]")
                    # Ici, ajouter la logique pour ajouter un joueur
                elif choix_joueur == "2":
                    console.print("[bold magenta]Supprimer un joueur sélectionné.[/bold magenta]")
                    # Ici, ajouter la logique pour supprimer un joueur
                elif choix_joueur == "3":
                    console.print("[bold magenta]Modifier un joueur sélectionné.[/bold magenta]")
                    # Ici, ajouter la logique pour modifier un joueur
                elif choix_joueur == "4":
                    break
                else:
                    console.print("[bold red]Choix invalide, veuillez réessayer.[/bold red]")
        elif choix == "3":
            console.print("[bold magenta]Vous êtes dans la section Rapports.[/bold magenta]")
        elif choix == "4":
            console.print("[bold red]Au revoir ![/bold red]")
            break
        else:
            console.print("[bold red]Choix invalide, veuillez réessayer.[/bold red]")

if __name__ == "__main__":
    main()