from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich import box
from controller.player_controller import ChessPlayerController


class TournamentView:
    """Console view for tournament management (Rich-based).

    Attributes
    ----------
    console : rich.console.Console
        Console instance used to render UI and read input.
    tournament_controller :
        Controller responsible for tournament CRUD and workflow operations.

    Methods
    -------
    display_tournament_menu_view():
        Render the tournament management main menu.
    display_display_tournaments_view(tournaments):
        Render a table listing tournaments.
    display_modify_tournament_view(index, name):
        Render the modify-tournament submenu for the given tournament.
    display_update_tournament_view(index, name):
        Render the update-tournament submenu for the given tournament.
    display_tournament_round(rounds):
        Render rounds overview for a tournament.
    display_tournament_round_matches(matches):
        Return a Rich Table representing the matches of a round.
    get_new_tournament_details():
        Prompt user for new tournament data and return it.
    get_match_result():
        Prompt user for a match result and return the entered value.
    demand_round_status_update_validation():
        Ask user to validate completed round results (Y/N) and return answer.
    execute():
        Run the interactive tournament menu loop.
    display_*_message(...):
        Various convenience methods to print status / error messages centered.
    """

    def __init__(self, tournament_controller):
        """
        Initialize TournamentView.

        Parameters
        ----------
        tournament_controller :
            Instance of the controller managing tournament operations.
        """
        self.console = Console()
        self.tournament_controller = tournament_controller

    def display_tournament_menu_view(self):
        """
        Render the tournament menu in the console.

        Shows the list of available tournament-related actions.
        Returns
        -------
        None
        """
        table = Table(title="Menu Tournois", show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Afficher les tournois")
        table.add_row("[bold cyan]2.[/bold cyan] Créer un tournoi")
        table.add_row("[bold cyan]3.[/bold cyan] Modifier un tournoi")
        table.add_row("[bold cyan]4.[/bold cyan] Inscrire des joueurs")
        # remplir les résultats de chaque match puis passer au round suivant
        table.add_row("[bold cyan]5.[/bold cyan] Demarrer un tournoi")
        # reprise si jamais programme arrêté en cours de tournoi
        table.add_row("[bold cyan]6.[/bold cyan] Mettre à jour un tournoi")
        table.add_row("[bold cyan]7.[/bold cyan] Supprimer un tournoi")
        table.add_row("[bold cyan]8.[/bold cyan] Retour")
        panel = Panel(
            table,
            title="[bold yellow]Gestion des Tournois[/bold yellow]",
            border_style="gold1",
        )
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def display_display_tournaments_view(self, tournaments):
        """
        Display a table listing tournaments.

        Parameters
        ----------
        tournaments : iterable
            Iterable of Tournament instances to display.

        Returns
        -------
        None
        """
        table = Table(
            title=None,
            show_header=True,
            header_style="bold blue",
            show_lines=True,
            box=box.SQUARE_DOUBLE_HEAD,
        )
        table.add_column("Index", style="dim")
        table.add_column("ID", style="steel_blue3")
        table.add_column("Statut", style="green_yellow")
        table.add_column("Nom", style="cyan")
        table.add_column("Lieu", style="cyan")
        table.add_column("Date de Début", style="magenta")
        table.add_column("Date de Fin", style="magenta")
        table.add_column("Nombre de Joueurs", style="green")
        table.add_column("Nombre de Rounds", style="green")
        table.add_column("Round Actuel", style="green")
        table.add_column("Description", style="dark_orange")

        for index, tournament in enumerate(tournaments):
            table.add_row(
                str(index),
                tournament.tournament_id,
                tournament.status,
                tournament.name,
                tournament.location,
                tournament.start_date,
                tournament.end_date,
                str(len(tournament.players)),
                str(tournament.number_of_rounds),
                str(tournament.current_round),
                tournament.description,
            )

        panel = Panel(
            table, title="[bold yellow]Liste des Tournois[/bold yellow]",
            subtitle="Appuyez sur 'b' pour revenir au menu précédent",
            border_style="gold1",
        )
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def display_modify_tournament_view(self, index, name):
        """
        Render the modify-tournament submenu.

        Parameters
        ----------
        index : int
            Index of the tournament being modified.
        name : str
            Current name of the tournament.

        Returns
        -------
        None
        """
        table = Table(title=str(index) + " : " + name,
                      show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Modifier le nom")
        table.add_row("[bold cyan]2.[/bold cyan] Modifier le lieu")
        table.add_row("[bold cyan]3.[/bold cyan] Modifier la date de début")
        table.add_row("[bold cyan]4.[/bold cyan] Modifier la date de fin")
        table.add_row("[bold cyan]5.[/bold cyan] Modifier la description")
        table.add_row("[bold cyan]6.[/bold cyan] Retour")
        panel = Panel(
            table,
            title="[bold yellow]Modification Tournoi[/bold yellow]",
            border_style="gold1",
        )
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def display_update_tournament_view(self, index, name):
        """
        Render the update-tournament submenu.

        Parameters
        ----------
        index : int
            Index of the tournament to update.
        name : str
            Current tournament name.

        Returns
        -------
        None
        """
        table = Table(title=str(index) + " : " + name,
                      show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Inscrire des joueurs")
        # générer le nombre de rounds et les matchs du round 1
        table.add_row("[bold cyan]2.[/bold cyan] Clôturer les inscriptions")
        table.add_row("[bold cyan]3.[/bold cyan] Inscrire les résultats")
        # générer les matchs du round suivant
        table.add_row("[bold cyan]4.[/bold cyan] Clôturer le round")
        table.add_row("[bold cyan]5.[/bold cyan] Retour")
        panel = Panel(
            table,
            title="[bold yellow]Mise à jour Tournoi[/bold yellow]",
            border_style="gold1",
        )
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def display_tournament_round(self, rounds):
        """
        Display an overview of rounds as a Rich panel.

        Parameters
        ----------
        rounds : iterable
            Iterable of TournamentRound instances.

        Returns
        -------
        None
        """
        rounds_table = Table(
            title=None,
            show_header=True,
            header_style="bold blue",
            show_lines=True,
            box=box.SQUARE_DOUBLE_HEAD,
            expand=True,
        )
        rounds_table.add_column("Index", style="dim", justify="center")
        rounds_table.add_column(
            "Round ID", style="steel_blue3", justify="center")
        rounds_table.add_column(
            "Statut", style="green_yellow", justify="center")
        rounds_table.add_column("Round", style="cyan", justify="center")
        rounds_table.add_column("Matches", justify="center")

        for index, round in enumerate(rounds):
            rounds_table.add_row(
                str(index),
                round.round_id,
                round.status,
                round.name,
                self.display_tournament_round_matches(round.matches),
            )

        panel = Panel(
            rounds_table, title="[bold yellow]Liste des Rounds[/bold yellow]",
            subtitle="Appuyez sur 'b' pour revenir au menu précédent",
            border_style="gold1",
            expand=True
        )
        centered_panel = Align.center(panel)
        self.console.print(centered_panel)

    def display_tournament_round_matches(self, matches):
        """
        Build and return a Rich Table showing the matches of a round.

        Parameters
        ----------
        matches : iterable
            Iterable where each match is represented (commonly) as
            [(white_id, white_score), (black_id, black_score)].

        Returns
        -------
        rich.table.Table
            Table object ready to be printed inside a panel.
        """
        matches_table = Table(
            title=None,
            show_header=True,
            header_style="orange_red1",
            show_lines=True,
            box=box.MINIMAL_HEAVY_HEAD,
        )
        matches_table.add_column("N°", style="dim", justify="center")
        matches_table.add_column(
            "Joueur Blanc", style="steel_blue3", justify="right")
        matches_table.add_column("Score", style="steel_blue3", justify="right")
        matches_table.add_column("", style="cyan", justify="center")
        matches_table.add_column(
            "Score", style="medium_orchid", justify="left")
        matches_table.add_column(
            "Joueur Noir", style="medium_orchid", justify="left")

        for index, match in enumerate(matches):
            matches_table.add_row(
                str(index),
                match[0][0],
                str(match[0][1]),
                "VS",
                str(match[1][1]),
                match[1][0],
            )
        return matches_table

    def get_new_tournament_details(self):
        """
        Prompt the user for new tournament details.

        Returns
        -------
        tuple
            (name, location, start_date, end_date, description)
        """
        name = self.console.input("Nom du tournoi : ")
        location = self.console.input("Lieu : ")
        start_date = self.console.input("Date de début (YYYY-MM-DD) : ")
        end_date = self.console.input("Date de fin (YYYY-MM-DD) : ")
        description = self.console.input("Description du tournoi : ")
        return name, location, start_date, end_date, description

    def get_match_result(self):
        """
        Prompt the user for a match result.

        Returns
        -------
        str
            The user-entered result string (e.g. "1", "0", "0.5").
        """
        result = self.console.input(
            "Entrer le score du joueur blanc (1, 0 ou 0.5): ")
        return result

    def demand_round_status_update_validation(self):
        """
        Ask the user to validate the completed round results.

        Returns
        -------
        str
            The user's raw response (expected 'O'/'N' or similar).
        """
        validation = self.console.input(
            "Tous les résultats ont été renseignés. Validez-vous ces scores ? (O/N): ")
        return validation

    def execute(self):
        """
        Run the interactive tournament menu loop.

        The method displays the tournament menu, handles user choices and
        delegates operations to the tournament controller until the user exits.
        """
        running = True
        while running:
            self.display_tournament_menu_view()
            choice = self.console.input(
                "\n[bold green]Sélectionnez une option (1-8) : [/bold green]")
            if choice == "1":
                while True:
                    self.display_display_tournaments_view(
                        self.tournament_controller.display_tournaments())
                    tournament_list_choice = self.console.input(
                        "\n[bold green]Sélectionnez une action : [/bold green]")
                    if tournament_list_choice.lower() == 'b':
                        break
            elif choice == "2":
                self.display_section_message("Créer un tournoi")
                name, location, start_date, end_date, description = self.get_new_tournament_details()
                self.tournament_controller.add_tournament(
                    name, location, start_date, end_date, description)
                self.display_tournament_added_message(name)
            elif choice == "3":
                self.display_section_message("Modifier un tournoi")
                tournaments_count = self.tournament_controller.get_tournaments_count()
                if tournaments_count == 0:
                    self.display_empty_tournament_modify_list_message()
                    break
                try:
                    index = int(self.console.input(
                        f"Index du tournoi à modifier (0-{tournaments_count - 1}): "))
                    while True:
                        tournament = self.tournament_controller.get_tournament(
                            index)
                        self.display_modify_tournament_view(
                            index, tournament.name)
                        modify_choice = self.console.input(
                            "\n[bold green]Sélectionnez une action (1-6) : [/bold green]")
                        if modify_choice == "1":
                            self.console.print(
                                f"Ancien nom : {tournament.name}", style="dim")
                            name = self.console.input("Nouveau nom : ")
                            self.tournament_controller.modify_tournament(
                                index, name=name)
                            self.display_tournament_modified_message(index)
                        elif modify_choice == "2":
                            self.console.print(
                                f"Ancien lieu : {tournament.location}", style="dim")
                            location = self.console.input("Nouveau lieu : ")
                            self.tournament_controller.modify_tournament(
                                index, location=location)
                            self.display_tournament_modified_message(index)
                        elif modify_choice == "3":
                            self.console.print(
                                f"Ancienne date de début : {tournament.start_date}", style="dim")
                            start_date = self.console.input(
                                "Nouvelle date de début (YYYY-MM-DD) : ")
                            self.tournament_controller.modify_tournament(
                                index, start_date=start_date)
                            self.display_tournament_modified_message(index)
                        elif modify_choice == "4":
                            self.console.print(
                                f"Ancienne date de fin : {tournament.end_date}", style="dim")
                            end_date = self.console.input(
                                "Nouvelle date de fin (YYYY-MM-DD) : ")
                            self.tournament_controller.modify_tournament(
                                index, end_date=end_date)
                            self.display_tournament_modified_message(index)
                        elif modify_choice == "5":
                            self.console.print(
                                f"Ancienne description : {tournament.description}", style="dim")
                            description = self.console.input(
                                "Nouvelle description : ")
                            self.tournament_controller.modify_tournament(
                                index, description=description)
                            self.display_tournament_modified_message(index)
                        elif modify_choice == "6":
                            break
                        else:
                            self.display_invalid_choice_message()
                except ValueError:
                    self.display_index_value_error_message()
                except IndexError:
                    self.display_tournament_index_error_message()
            elif choice == "4":
                self.display_section_message("Inscrire des joueurs")
                # Logique pour inscrire des joueurs à un tournoi
                tournaments_count = self.tournament_controller.get_tournaments_count()
                if tournaments_count == 0:
                    self.display_empty_tournament_subscribe_list_message()
                    break
                try:
                    index = int(self.console.input(
                        f"Index du tournoi pour inscrire des joueurs (0-{tournaments_count - 1}): "))
                    # Logique pour inscrire des joueurs dans le tournoi à l'index spécifié
                    # Par exemple, demander les IDs des joueurs à inscrire
                    tournament = self.tournament_controller.get_tournament(
                        index)
                    if tournament.status != "À venir":
                        self.display_tournament_subscription_closed_message()
                        break
                    self.console.print(
                        f"Inscrire des joueurs pour le tournoi : {tournament.name}", style="bold green")
                    players_id = self.console.input(
                        "Entrez les IDs des joueurs à inscrire (séparés par des virgules) : ")
                    # Vous pouvez ajouter une validation pour vérifier si les IDs existent
                    # dans la liste des joueurs avant de les inscrire
                    player_controller = ChessPlayerController()
                    valid_players_id_list, invalid_players_id_list = player_controller.transform_players_id_list(
                        players_id)
                    if valid_players_id_list:
                        subscribed_ids, already_subscribed_ids = self.tournament_controller.subscribe_players(
                            index, valid_players_id_list)
                        if subscribed_ids:
                            self.display_tournament_valid_subscription_message(
                                subscribed_ids)
                        if already_subscribed_ids:
                            self.display_tournament_already_subscribed_message(
                                already_subscribed_ids)
                    if invalid_players_id_list:
                        self.display_tournament_invalid_subscription_message(
                            invalid_players_id_list)
                except ValueError:
                    self.display_index_value_error_message()
                except IndexError:
                    self.display_tournament_index_error_message()
            elif choice == "5":
                self.display_section_message("Démarrer un tournoi")
                tournaments_count = self.tournament_controller.get_tournaments_count()
                if tournaments_count == 0:
                    self.display_empty_tournament_start_list_message()
                    break
                try:
                    index = int(self.console.input(
                        f"Index du tournoi à démarrer (0-{tournaments_count - 1}): "))
                    tournament = self.tournament_controller.get_tournament(
                        index)
                    if tournament.status == "À venir":
                        self.tournament_controller.start_tournament(index)
                        round_index = 0
                        self.display_tournament_started_message(index)
                        started_tournament = self.tournament_controller.get_tournament(
                            index)
                        started_tournament_round_status = started_tournament.rounds[round_index].status
                        while started_tournament_round_status != "Terminé":
                            self.display_tournament_round(
                                started_tournament.rounds)
                            matches_count = self.tournament_controller.get_tournament_round_matches_count(
                                index, round_index)
                            valid_matches_number = []
                            for n in range(matches_count):
                                valid_matches_number.append(str(n))
                            tournament_list_choice = self.console.input(
                                "\nSélectionnez le numéro d'un match du round en cours "
                                f"pour inscrire les scores (0-{matches_count - 1}): ")
                            if tournament_list_choice in valid_matches_number:
                                self.console.print(
                                    f"Résultats du match N°{tournament_list_choice} :", style="bold")
                                self.tournament_controller.put_tournament_round_match_results(
                                    index=index,
                                    round_index=round_index,
                                    match_number=tournament_list_choice,
                                    result1=self.get_match_result()
                                )
                                matches_over = self.tournament_controller.tournament_round_status_update(
                                    index, round_index)
                                if matches_over:
                                    validation = self.demand_round_status_update_validation()
                                    if validation.lower() == "o":
                                        self.tournament_controller.close_tournament_round(
                                            index, round_index)
                                        self.tournament_controller.update_tournament_round_players_points(
                                            index, round_index)
                                        if started_tournament.current_round == started_tournament.number_of_rounds:
                                            self.display_end_of_tournament_message()
                                            self.tournament_controller.close_tournament(
                                                index)
                                        else:
                                            self.tournament_controller.initiate_next_tournament_round(
                                                index)
                                            round_index += 1

                                started_tournament = self.tournament_controller.get_tournament(
                                    index)
                                started_tournament_round_status = started_tournament.rounds[
                                    round_index].status
                            elif tournament_list_choice.lower() == 'b':
                                break
                            else:
                                self.display_tournament_round_match_number_error_message()
                    elif tournament.status == "En cours":
                        self.display_tournament_already_started_message()
                    elif tournament.status == "Terminé":
                        self.display_tournament_already_ended_message()
                    else:
                        self.display_tournament_status_error_message()
                except ValueError:
                    self.display_index_value_error_message()
                except IndexError:
                    self.display_tournament_index_error_message()

            elif choice == "6":
                self.display_section_message("Mettre à jour un tournoi")
                tournaments_count = self.tournament_controller.get_tournaments_count()
                if tournaments_count == 0:
                    self.display_empty_tournament_start_list_message()
                    break
                try:
                    index = int(self.console.input(
                        f"Index du tournoi à mettre à jour (0-{tournaments_count - 1}): "))
                    tournament = self.tournament_controller.get_tournament(
                        index)
                    if tournament.status == "En cours":
                        round_index = len(tournament.rounds) - 1
                        ongoing_tournament = self.tournament_controller.get_tournament(
                            index)
                        ongoing_tournament_round_status = ongoing_tournament.rounds[round_index].status
                        while ongoing_tournament_round_status != "Terminé":
                            self.display_tournament_round(
                                ongoing_tournament.rounds)
                            matches_count = self.tournament_controller.get_tournament_round_matches_count(
                                index, round_index)
                            valid_matches_number = []
                            for n in range(matches_count):
                                valid_matches_number.append(str(n))
                            tournament_list_choice = self.console.input(
                                "\nSélectionnez le numéro d'un match du round en cours "
                                f"pour inscrire les scores (0-{matches_count - 1}): ")
                            if tournament_list_choice in valid_matches_number:
                                self.console.print(
                                    f"Résultats du match N°{tournament_list_choice} :", style="bold")
                                self.tournament_controller.put_tournament_round_match_results(
                                    index=index,
                                    round_index=round_index,
                                    match_number=tournament_list_choice,
                                    result1=self.get_match_result()
                                )
                                matches_over = self.tournament_controller.tournament_round_status_update(
                                    index, round_index)
                                if matches_over:
                                    validation = self.demand_round_status_update_validation()
                                    if validation.lower() == "o":
                                        self.tournament_controller.close_tournament_round(
                                            index, round_index)
                                        self.tournament_controller.update_tournament_round_players_points(
                                            index, round_index)
                                        if ongoing_tournament.current_round == ongoing_tournament.number_of_rounds:
                                            self.display_end_of_tournament_message()
                                            self.tournament_controller.close_tournament(
                                                index)
                                        else:
                                            self.tournament_controller.initiate_next_tournament_round(
                                                index)
                                            round_index += 1

                                ongoing_tournament = self.tournament_controller.get_tournament(
                                    index)
                                ongoing_tournament_round_status = ongoing_tournament.rounds[
                                    round_index].status
                            elif tournament_list_choice.lower() == 'b':
                                break
                            else:
                                self.display_tournament_round_match_number_error_message()
                    elif tournament.status == "À venir":
                        self.display_tournament_not_started_message()
                    elif tournament.status == "Terminé":
                        self.display_tournament_already_ended_message()
                    else:
                        self.display_tournament_status_error_message()
                except ValueError:
                    self.display_index_value_error_message()
                except IndexError:
                    self.display_tournament_index_error_message()

            elif choice == "7":
                self.display_section_message("Supprimer un tournoi")
                tournaments_count = self.tournament_controller.get_tournaments_count()
                if tournaments_count == 0:
                    self.display_empty_tournament_remove_list_message()
                    break
                try:
                    index = int(self.console.input(
                        f"Index du tournoi à supprimer (0-{tournaments_count - 1}): "))
                    name, tournament_id = self.tournament_controller.remove_tournament(
                        index)
                    self.display_tournament_removed_message(
                        tournament_id, name)
                except ValueError:
                    self.display_index_value_error_message()
                except IndexError:
                    self.display_tournament_index_error_message()
            elif choice == "8":
                running = False
            else:
                self.display_invalid_choice_message()

    def display_exit_message(self):
        """
        Print a goodbye message when returning to main menu.
        """
        self.console.print(Align.center(
            "[bold red]Retour au menu principal ![/bold red]"))

    def display_invalid_choice_message(self):
        """
        Inform the user that the selected option is invalid.
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
        """
        self.console.print(Align.center(
            f"[bold magenta]{section_name}[/bold magenta]"))

    def display_index_value_error_message(self):
        """
        Inform the user that a non-integer was provided where an integer was expected.
        """
        self.console.print(Align.center(
            "[bold red]Entrée invalide, veuillez entrer un nombre entier pour l'index.[/bold red]"))

    def display_tournament_index_error_message(self):
        """
        Inform the user that the chosen tournament index is invalid.
        """
        self.console.print(Align.center(
            "[bold red]Index invalide. Aucune action effectuée.[/bold red]"))

    def display_tournament_added_message(self, name):
        """
        Inform the user that a tournament was added.

        Parameters
        ----------
        name : str
            Name of the newly created tournament.
        """
        self.console.print(Align.center(
            f"[bold green]Le tournoi : {name} a été ajouté avec succès ![/bold green]"))

    def display_tournament_removed_message(self, tournament_id, name):
        """
        Inform the user that a tournament was removed.

        Parameters
        ----------
        tournament_id : str
            Unique identifier of the removed tournament.
        name : str
            Name of the removed tournament.
        """
        self.console.print(Align.center(
            f"[bold red]Le tournoi {tournament_id} : {name} a été supprimé avec succès ![/bold red]"))

    def display_tournament_modified_message(self, index):
        """
        Inform the user that a tournament was modified.

        Parameters
        ----------
        index : int
            Index of the modified tournament.
        """
        self.console.print(Align.center(
            f"[bold blue]Le tournoi à l'index {index} a été modifié avec succès ![/bold blue]"))

    def display_tournament_started_message(self, index):
        """
        Inform the user that a tournament has been started.

        Parameters
        ----------
        index : int
            Index of the started tournament.
        """
        self.console.print(Align.center(
            f"[bold green]Le tournoi à l'index {index} a été initialisé avec succès ![/bold green]"))

    def display_empty_tournament_modify_list_message(self):
        """
        Inform the user there are no tournaments available to modify.
        """
        self.console.print(Align.center(
            "[bold yellow]Aucun tournoi disponible pour modification.[/bold yellow]"))

    def display_empty_tournament_subscribe_list_message(self):
        """
        Inform the user there are no tournaments available for subscription.
        """
        self.console.print(Align.center(
            "[bold yellow]Aucun tournoi disponible pour inscription.[/bold yellow]"))

    def display_empty_tournament_remove_list_message(self):
        """
        Inform the user there are no tournaments available to remove.
        """
        self.console.print(Align.center(
            "[bold yellow]Aucun tournoi disponible pour suppression.[/bold yellow]"))

    def display_empty_tournament_update_list_message(self):
        """
        Inform the user there are no tournaments available to update.
        """
        self.console.print(Align.center(
            "[bold yellow]Aucun tournoi disponible pour mise à jour.[/bold yellow]"))

    def display_empty_tournament_start_list_message(self):
        """
        Inform the user there are no tournaments available to start.
        """
        self.console.print(Align.center(
            "[bold yellow]Aucun tournoi disponible pour démarrage.[/bold yellow]"))

    def display_tournament_valid_subscription_message(self, valid_ids):
        """
        Show the list of successfully subscribed player IDs.

        Parameters
        ----------
        valid_ids : iterable
            Iterable of player federation IDs that were subscribed.
        """
        self.console.print(Align.center(
            "[bold green]Le(s) joueur(s) aux IDs suivants ont été inscrits avec succès :[/bold green]"))
        self.console.print(Align.center(
            f"[green]{',\n'.join(valid_ids)}[/green]"))

    def display_tournament_already_subscribed_message(self, already_subscribed_ids):
        """
        Show player IDs that were already subscribed.

        Parameters
        ----------
        already_subscribed_ids : iterable
            Iterable of player federation IDs that were already in the tournament.
        """
        self.console.print(Align.center(
            "[bold yellow]Le(s) joueur(s) aux IDs suivants sont déjà inscrits dans le tournoi :[/bold yellow]"))
        self.console.print(Align.center(
            f"[yellow]{',\n'.join(already_subscribed_ids)}[/yellow]"))

    def display_tournament_invalid_subscription_message(self, invalid_ids):
        """
        Show player IDs that were invalid and thus not subscribed.

        Parameters
        ----------
        invalid_ids : iterable
            Iterable of invalid player IDs provided by the user.
        """
        self.console.print(Align.center(
            "[bold red]Le(s) ID(s) suivant(s) sont invalides et aucune action n'a été effectuée avec :[/bold red]"))
        self.console.print(Align.center(
            f"[red]{',\n'.join(invalid_ids)}[/red]"))

    def display_tournament_subscription_closed_message(self):
        """
        Inform the user that the tournament is not accepting subscriptions.
        """
        self.console.print(Align.center(
            "[bold red]Les inscriptions sont clôturées pour ce tournoi.[/bold red]"))

    def display_tournament_already_started_message(self):
        """
        Inform the user that the tournament has already started.
        """
        self.console.print(Align.center(
            "[bold yellow]Ce tournoi a déjà commencé.[/bold yellow]"))

    def display_tournament_already_ended_message(self):
        """
        Inform the user that the tournament has already ended.
        """
        self.console.print(Align.center(
            "[bold yellow]Ce tournoi est terminé.[/bold yellow]"))

    def display_tournament_not_started_message(self):
        """
        Inform the user that the tournament has not started yet.
        """
        self.console.print(Align.center(
            "[bold yellow]Ce tournoi n'a pas commencé encore.[/bold yellow]"))

    def display_end_of_tournament_message(self):
        """
        Show a message indicating the tournament has finished.
        """
        self.console.print(Align.center(
            "[bold deep_pink3]Ce tournoi est maintenant terminé.[/bold deep_pink3]"))

    def display_tournament_status_error_message(self):
        """
        Inform the user that the tournament status could not be retrieved or is invalid.
        """
        self.console.print(Align.center(
            "[bold red]Impossible de récupérer le statut de ce tournoi. Aucune action effectuée.[/bold red]"))

    def display_tournament_round_match_number_error_message(self):
        """
        Inform the user that the chosen match number for a round is invalid.
        """
        self.console.print(Align.center(
            "[bold red]Numéro invalide. Aucune action effectuée.[/bold red]"))
