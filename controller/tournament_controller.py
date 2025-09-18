from view.tournament_view import TournamentView
from model.tournament_model import Tournament

import json

class TournamentController:
    def __init__(self, tournament_view):
        self.tournament_view = tournament_view
        self.tournaments = []

    def load_tournaments_from_json(self, filepath="data/tournaments.json"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                tournaments_data = json.load(f)
                self.tournaments = [Tournament(**t) for t in tournaments_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tournaments = []

    def save_tournaments_to_json(self, filepath="data/tournaments.json"):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([t.__dict__ for t in self.tournaments], f, ensure_ascii=False, indent=4)

    def display_tournaments(self):
        self.load_tournaments_from_json()
        self.tournament_view.display_tournaments(self.tournaments)

    def add_tournament(self, name, location, start_date, end_date, players, description):
        self.load_tournaments_from_json()
        new_tournament = Tournament(name, location, start_date, end_date, players, description)
        self.tournaments.append(new_tournament)
        self.save_tournaments_to_json()

    def remove_tournament(self, index):
        self.load_tournaments_from_json()
        if 0 <= index < len(self.tournaments):
            del self.tournaments[index]
            self.save_tournaments_to_json()

    def modify_tournament(self, index, **kwargs):
        self.load_tournaments_from_json()
        if 0 <= index < len(self.tournaments):
            for key, value in kwargs.items():
                if hasattr(self.tournaments[index], key):
                    setattr(self.tournaments[index], key, value)
            self.save_tournaments_to_json()

    def status_update(self, index, status=None):
        from datetime import datetime

        self.load_tournaments_from_json()
        if 0 <= index < len(self.tournaments):
            tournament = self.tournaments[index]
            today = datetime.now().date()
            try:
                start_date = datetime.strptime(tournament.start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(tournament.end_date, "%Y-%m-%d").date() if tournament.end_date else None
            except Exception:
                # Si les dates sont mal formatées, on ne change rien
                return

            if status:
                tournament.status = status
            elif end_date and today > end_date:
                tournament.status = "Terminé"
            elif today < start_date:
                tournament.status = "À venir"
            else:
                tournament.status = "En cours"
            self.save_tournaments_to_json()

    def execute(self):
        # À compléter selon la logique de navigation de votre application
        running = True
        while running:
            self.tournament_view.display_tournament_menu_view()
            choice = self.tournament_view.console.input("\n[bold green]Sélectionnez une option (1-6) : [/bold green]")
            if choice == "1":
                self.display_tournaments()
            elif choice == "2":
                self.display_section_message("Créer un tournoi")
                # Logique pour ajouter un tournoi
                name = self.tournament_view.console.input("Nom du tournoi: ")
                location = self.tournament_view.console.input("Lieu du tournoi: ")
                start_date = self.tournament_view.console.input("Date de début (YYYY-MM-DD): ")
                end_date = self.tournament_view.console.input("Date de fin (YYYY-MM-DD): ")
                players = []  # Logique pour ajouter des joueurs
                description = self.tournament_view.console.input("Description du tournoi: ")
                self.add_tournament(name, location, start_date, end_date, players, description)
            elif choice == "3":
                self.display_section_message("Modifier un tournoi")
                # Logique pour modifier un tournoi
                index = int(self.tournament_view.console.input("Index du tournoi à modifier: "))
                name = self.tournament_view.console.input("Nouveau nom du tournoi (laisser vide pour ne pas changer): ")
                location = self.tournament_view.console.input("Nouveau lieu du tournoi (laisser vide pour ne pas changer): ")
                start_date = self.tournament_view.console.input("Nouvelle date de début (YYYY-MM-DD) (laisser vide pour ne pas changer): ")
                end_date = self.tournament_view.console.input("Nouvelle date de fin (YYYY-MM-DD) (laisser vide pour ne pas changer): ")
                description = self.tournament_view.console.input("Nouvelle description du tournoi (laisser vide pour ne pas changer): ")
                updates = {k: v for k, v in {
                    "name": name,
                    "location": location,
                    "start_date": start_date,
                    "end_date": end_date,
                    "description": description
                }.items() if v}
                self.modify_tournament(index, **updates)
            elif choice == "4":
                self.display_section_message("Mettre à jour un tournoi")
                # Logique pour mettre à jour un tournoi (par exemple, avancer le round)
                index = int(self.tournament_view.console.input("Index du tournoi à mettre à jour: "))
                # Exemple simple d'incrémentation du round actuel
                if 0 <= index < len(self.tournaments):
                    current_round = self.tournaments[index].current_round
                    self.modify_tournament(index, current_round=current_round + 1)
            elif choice == "5":
                self.display_section_message("Supprimer un tournoi")
                # Logique pour supprimer un tournoi
                index = int(self.tournament_view.console.input("Index du tournoi à supprimer: "))
                self.remove_tournament(index)
            elif choice == "6":
                running = False
            else:
                self.tournament_view.display_invalid_choice_message()