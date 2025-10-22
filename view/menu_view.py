from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from view.tournament_view import TournamentView
from controller.tournament_controller import TournamentController
from view.player_view import PlayerView
from controller.player_controller import ChessPlayerController
from view.report_view import ReportView


class MenuView:
    """Console menu view for the application.

    Attributes
    ----------
    console : rich.console.Console
        Console instance used to render panels, tables and read input.

    Methods
    -------
    display_menu_view():
        Render the main menu (Tournois, Joueurs, Rapports, Quitter) as a Rich Panel.
    execute():
        Main loop: display the menu, read user choice and dispatch to sub-views.
    display_exit_message():
        Print a goodbye message centered in the console.
    display_invalid_choice_message():
        Print a centered error message when user input is invalid.
    display_section_message(section_name):
        Print a centered info message indicating the active section.
    """

    def __init__(self):
        """
        Initialize the MenuView.

        Creates a Rich Console instance used by the view.

        Attributes set:
            console (rich.console.Console): console used for rendering and input.
        """
        self.console = Console()

    def display_menu_view(self):
        """
        Render the main menu.

        Builds a Rich Table with the available top-level sections and prints it
        inside a Panel centered in the terminal.

        Returns
        -------
        None
        """
        table = Table(title="Menu Principal", show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Tournois")
        table.add_row("[bold cyan]2.[/bold cyan] Joueurs")
        table.add_row("[bold cyan]3.[/bold cyan] Rapports")
        table.add_row("[bold cyan]4.[/bold cyan] Quitter")
        panel = Panel(
            table, title="[bold yellow]AJEDREZ[/bold yellow]", border_style="blue")
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def execute(self):
        """
        Run the interactive menu loop.

        Displays the menu, reads user input and dispatches to the corresponding
        sub-view (tournament, player, report). The loop continues until the
        user selects the quit option.

        Returns
        -------
        None
        """
        running = True
        while running:
            self.display_menu_view()
            choice = self.console.input(
                "\n[bold green]Sélectionnez une section (1-4) : [/bold green]")
            if choice == "1":
                # Ajouter la logique pour gérer les tournois ici
                tournament_controller = TournamentController()
                tournament_view = TournamentView(tournament_controller)
                tournament_view.execute()
            elif choice == "2":
                # Ajouter la logique pour gérer les joueurs ici
                player_controller = ChessPlayerController()
                player_view = PlayerView(player_controller)
                player_view.execute()
            elif choice == "3":
                # Ajouter la logique pour gérer les rapports ici
                report_view = ReportView()
                report_view.execute()
            elif choice == "4":
                self.display_exit_message()
                running = False
            else:
                self.display_invalid_choice_message()

    def display_exit_message(self):
        """
        Print a goodbye message.

        The message is centered and highlighted in red.

        Returns
        -------
        None
        """
        self.console.print(Align.center("[bold red]Au revoir ![/bold red]"))

    def display_invalid_choice_message(self):
        """
        Inform the user that the entered choice is invalid.

        The message is centered and displayed in red.

        Returns
        -------
        None
        """
        self.console.print(Align.center(
            "[bold red]Choix invalide, veuillez réessayer.[/bold red]"))

    def display_section_message(self, section_name):
        """
        Display a centered informational message about the current section.

        Parameters
        ----------
        section_name : str
            Human-readable name of the section to display.

        Returns
        -------
        None
        """
        self.console.print(Align.center(
            f"[bold magenta]Vous êtes dans la section {section_name}.[/bold magenta]"))
