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

        table = Table(title=None, show_header=True, header_style="bold blue")
        table.add_column("Index", style="dim", width=6)
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("Date de Naissance", style="magenta")
        table.add_column("ID Fédération", style="green")
        table.add_column("Elo", style="dark_orange")


        for index, player in enumerate(players):
            table.add_row(str(index), player.surname, player.name, player.date_of_birth, player.federation_chess_id, str(player.elo))
        
        panel = Panel(table, title="[bold yellow]Liste des Joueurs[/bold yellow]", subtitle="Appuyez sur 'b' pour revenir au menu précédent", border_style="magenta")
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

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

    def get_new_player_details(self):
        surname = self.console.input("Nom de famille : ")
        name = self.console.input("Prénom : ")
        date_of_birth = self.console.input("Date de naissance (YYYY-MM-DD) : ")
        federation_chess_id = self.console.input("Identifiant fédération : ")
        elo_input = self.console.input("ELO (1000-2500) : ")
        elo = int(elo_input)
        return surname, name, date_of_birth, federation_chess_id, elo

    def get_user_input(self, prompt):
        return self.console.input(prompt)
    
    def display_player_added_message(self, name, surname):
        self.console.print(Align.center(f"[bold green]Le joueur {name} {surname} a été ajouté avec succès ![/bold green]"))

    def display_player_removed_message(self, name, surname):
        self.console.print(f"[bold red]Le joueur à l'index {name} {surname} a été supprimé avec succès ![/bold red]")
        
    def display_player_index_error_message(self):
        self.console.print(Align.center("[bold red]Index invalide. Aucun joueur supprimé.[/bold red]"))

    def display_player_modified_message(self, name, surname):
        self.console.print(f"[bold blue]Le joueur {name} {surname} a été modifié avec succès ![/bold blue]")

    def display_exit_message(self):
        self.console.print(Align.center("[bold red]Au revoir ![/bold red]"))

    def display_invalid_choice_message(self):
        self.console.print(Align.center("[bold red]Choix invalide, veuillez réessayer.[/bold red]"))

    def display_section_message(self, section_name):
        self.console.print(Align.center(f"[bold magenta]{section_name}[/bold magenta]"))

    def display_value_error_message(self):
        self.console.print(Align.center("[bold red]Entrée invalide, veuillez entrer un nombre entier pour l'index.[/bold red]"))