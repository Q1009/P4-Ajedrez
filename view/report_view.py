from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from controller.player_controller import ChessPlayerController
from controller.tournament_controller import TournamentController
import os


class ReportView:
    """View responsible for generating HTML reports from templates.

    Attributes
    ----------
    console : rich.console.Console
        Console used to display messages and receive simple input.

    Methods
    -------
    display_report_menu_view():
        Render the report generation menu in the console.
    display_players_jinja_view(players):
        Render and write a players HTML report using Jinja2.
    display_tournaments_jinja_view(tournaments):
        Render and write a tournaments HTML report using Jinja2.
    display_tournament_players_jinja_view(tournament, players):
        Render and write a tournament-specific players report.
    display_tournament_rounds_jinja_view(tournament, players):
        Render and write a tournament-specific rounds report.
    display_index_jinja_view(tournaments, players):
        Render and write the index (home) HTML report.
    execute():
        Interactive loop to trigger report generation from console.
    display_invalid_choice_message():
        Print an error message for invalid menu choices.
    display_successful_generation_message(file):
        Print a success message after a report is generated.
    display_link():
        Print a clickable link (in supporting terminals) or path to reports.
    """

    def __init__(self):
        """
        Initialize the ReportView.

        Parameters
        ----------
        None
        """
        self.console = Console()

    def display_report_menu_view(self):
        """
        Render the report menu in the console.

        The menu offers to generate reports or return to the previous menu.
        """
        table = Table(title="Menu Rapports", show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Générer les rapports")
        table.add_row("[bold cyan]2.[/bold cyan] Retour")
        panel = Panel(
            table, title="[bold yellow]Gestion des Rapports[/bold yellow]", border_style="magenta")
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def _ensure_reports_dir(self, directory="reports"):
        """
        Ensure the output directory for reports exists.

        Parameters
        ----------
        directory : str
            Path to the reports directory (default 'reports').

        Returns
        -------
        str
            The directory path.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def _write_html_file(self, file_path, content):
        """
        Write rendered HTML content to file.

        Parameters
        ----------
        file_path : str
            Destination file path.
        content : str
            Rendered HTML content to write.
        """
        with open(file_path, "w", encoding="utf-8") as fh:
            fh.write(content)

    def display_players_jinja_view(self, players):
        """
        Render and save the players report from the 'players.html.j2' template.

        Parameters
        ----------
        players : iterable
            List of player objects passed to the template.
        """
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('players.html.j2')
        html_rendu = template.render(players=players)
        directory = self._ensure_reports_dir()
        file_path = f'{directory}/players.html'
        self._write_html_file(file_path, html_rendu)
        self.display_successful_generation_message("joueurs")

    def display_tournaments_jinja_view(self, tournaments):
        """
        Render and save the tournaments report from the 'tournaments.html.j2' template.

        Parameters
        ----------
        tournaments : iterable
            List of tournament objects passed to the template.
        """
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('tournaments.html.j2')
        html_rendu = template.render(tournaments=tournaments)
        directory = self._ensure_reports_dir()
        file_path = f'{directory}/tournaments.html'
        self._write_html_file(file_path, html_rendu)
        self.display_successful_generation_message("tournois")

    def display_tournament_players_jinja_view(self, tournament, players):
        """
        Render and save a tournament-specific players report.

        Parameters
        ----------
        tournament : object
            Tournament instance passed to the template.
        players : iterable
            List of player objects passed to the template.
        """
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('tournament_players.html.j2')
        html_rendu = template.render(tournament=tournament, players=players)
        tournament_id = tournament.tournament_id
        directory = self._ensure_reports_dir()
        file_path = f'{directory}/{tournament_id}_players.html'
        self._write_html_file(file_path, html_rendu)
        self.display_successful_generation_message(
            f"info joueurs tournoi {tournament_id}")

    def display_tournament_rounds_jinja_view(self, tournament, players):
        """
        Render and save a tournament-specific rounds report.

        Parameters
        ----------
        tournament : object
            Tournament instance passed to the template.
        players : iterable
            List of player objects passed to the template.
        """
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('tournament_rounds.html.j2')
        html_rendu = template.render(tournament=tournament, players=players)
        tournament_id = tournament.tournament_id
        directory = self._ensure_reports_dir()
        file_path = f'{directory}/{tournament_id}_rounds.html'
        self._write_html_file(file_path, html_rendu)
        self.display_successful_generation_message(
            f"info tours tournoi {tournament_id}")

    def display_index_jinja_view(self, tournaments, players):
        """
        Render and save the index (home) HTML report.

        Parameters
        ----------
        tournaments : iterable
            List of tournament objects.
        players : iterable
            List of player objects.
        """
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('index.html.j2')
        html_rendu = template.render(tournaments=tournaments, players=players)
        directory = self._ensure_reports_dir()
        file_path = f'{directory}/index.html'
        self._write_html_file(file_path, html_rendu)
        self.display_successful_generation_message("accueil")

    def execute(self):
        """
        Run the interactive report generation loop.

        Presents the user with the report menu, triggers report generation when
        requested and prints the final link to the generated reports.
        """
        running = True
        while running:
            self.display_report_menu_view()
            choice = self.console.input(
                "\n[bold green]Sélectionnez une option (1-2) : [/bold green]")
            if choice == "1":
                player_controller = ChessPlayerController()
                tournament_controller = TournamentController()
                players = player_controller.display_players_from_json()
                tournaments = tournament_controller.display_tournaments()
                self.display_index_jinja_view(tournaments, players)
                self.display_players_jinja_view(players)
                self.display_tournaments_jinja_view(tournaments)
                for tournament in tournaments:
                    self.display_tournament_players_jinja_view(
                        tournament, players)
                    self.display_tournament_rounds_jinja_view(
                        tournament, players)
                self.display_link()
            elif choice == "2":
                running = False
            else:
                self.display_invalid_choice_message()

    def display_invalid_choice_message(self):
        """
        Print an error message for invalid menu choices.
        """
        self.console.print(Align.left(
            "[bold red]Choix invalide, veuillez réessayer.[/bold red]"))

    def display_successful_generation_message(self, file):
        """
        Print a success message after generating a report.

        Parameters
        ----------
        file : str
            Human-readable name of the generated file/report.
        """
        self.console.print(Align.left(
            f"[yellow]Le rapport {file} à été généré.[/yellow]"))

    def display_link(self):
        """
        Print a link (or path) pointing to the generated reports index.

        The printed link is clickable in terminals that support rich 'link' markup.
        """
        self.console.print(Align.left(
            "[bold bright_magenta]------------------------[/bold bright_magenta]"))
        self.console.print(Align.left(
            "[bold bright_magenta][link=./reports/index.html]Consultez les rapports ![/link][/bold bright_magenta]"))
        self.console.print(Align.left(
            "[bold bright_magenta]------------------------[/bold bright_magenta]"))
        self.console.print(Align.left(
            "Si le lien ne fonctionne pas, dans le dossier Reports ouvrez index.html dans un navigateur. "))
