from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich import print
from controller.player_controller import ChessPlayerController
from controller.tournament_controller import TournamentController
import os

class ReportView:
    def __init__(self, report_controller):
        self.console = Console()
        self.report_controller = report_controller


    def display_report_menu_view(self):
        table = Table(title="Menu Rapports", show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Générer les rapports")
        table.add_row("[bold cyan]2.[/bold cyan] Retour")
        panel = Panel(table, title="[bold yellow]Gestion des Rapports[/bold yellow]", border_style="magenta")
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def display_players_jinja_view(self, players):
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('players.html.j2')

        # Rendre le template avec des données
        html_rendu = template.render(players=players)
        directory = 'reports' 
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = f'{directory}/players.html'
        with open(file_path, "w") as fh:
            fh.write(html_rendu)

        self.display_successful_generation_message("joueurs")

    def display_tournaments_jinja_view(self, tournaments):
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('tournaments.html.j2')

        # Rendre le template avec des données
        html_rendu = template.render(tournaments=tournaments)
        directory = 'reports' 
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = f'{directory}/tournaments.html'
        with open(file_path, "w") as fh:
            fh.write(html_rendu)

        self.display_successful_generation_message("tournois")
    
    def display_tournament_players_jinja_view(self, tournament, players):
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('tournament_players.html.j2')

        # Rendre le template avec des données
        html_rendu = template.render(tournament=tournament, players=players)
        tournament_id = tournament.tournament_id
        directory = 'reports' 
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = f'{directory}/{tournament_id}_players.html'
        with open(file_path, "w") as fh:
            fh.write(html_rendu)

        self.display_successful_generation_message(f"info joueurs tournoi {tournament_id}")

    def display_tournament_rounds_jinja_view(self, tournament, players):
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('tournament_rounds.html.j2')

        # Rendre le template avec des données
        html_rendu = template.render(tournament=tournament, players=players)
        tournament_id = tournament.tournament_id
        directory = 'reports' 
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = f'{directory}/{tournament_id}_rounds.html'
        with open(file_path, "w") as fh:
            fh.write(html_rendu)

        self.display_successful_generation_message(f"info tours tournoi {tournament_id}")
        

    def display_index_jinja_view(self, tournaments, players):
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('index.html.j2')

        # Rendre le template avec des données
        html_rendu = template.render(tournaments=tournaments, players=players)
        directory = 'reports' 
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = f'{directory}/index.html'
        with open(file_path, "w") as fh:
            fh.write(html_rendu)

        self.display_successful_generation_message("accueil")

    def execute(self):
        running = True
        while running:
            self.display_report_menu_view()
            choice = self.console.input("\n[bold green]Sélectionnez une option (1-2) : [/bold green]")
            if choice == "1":
                player_controller = ChessPlayerController()
                tournament_controller = TournamentController()
                players = player_controller.display_players_from_json()
                tournaments = tournament_controller.display_tournaments()
                self.display_index_jinja_view(tournaments, players)
                self.display_players_jinja_view(players)
                self.display_tournaments_jinja_view(tournaments)
                for tournament in tournaments:
                    self.display_tournament_players_jinja_view(tournament, players)
                    self.display_tournament_rounds_jinja_view(tournament, players)
                self.display_link()
            elif choice == "2":
                running = False
            else:
                self.display_invalid_choice_message()

    def display_invalid_choice_message(self):
        self.console.print(Align.left("[bold red]Choix invalide, veuillez réessayer.[/bold red]"))

    def display_successful_generation_message(self, file):
        self.console.print(Align.left(f"[yellow]Le rapport {file} à été généré.[/yellow]"))

    def display_link(self):
        self.console.print(Align.left(f"[bold bright_magenta]------------------------[/bold bright_magenta]"))
        self.console.print(Align.left(f"[bold bright_magenta][link=./reports/index.html]Consultez les rapports ![/link][/bold bright_magenta]"))
        self.console.print(Align.left(f"[bold bright_magenta]------------------------[/bold bright_magenta]"))
        self.console.print(Align.left("Si le lien ne fonctionne pas, dans le dossier Reports ouvrez index.html dans un navigateur. "))