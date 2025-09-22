from model.tournament_model import Tournament

import json

class TournamentController:
    def __init__(self):
        self.tournaments = []

    def load_tournaments_from_json(self, filepath="data/tournaments.json"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                tournaments_loaded = json.load(f)
                for tournament_data in tournaments_loaded:
                    tournament = Tournament.from_dict(tournament_data)
                    self.tournaments.append(tournament)

        except (FileNotFoundError, json.JSONDecodeError):
            print("Aucun tournoi trouvé dans le fichier JSON.")
            tournaments = []
            return tournaments

    def save_tournaments_to_json(self, filepath="data/tournaments.json"):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([t.__dict__ for t in self.tournaments], f, ensure_ascii=False, indent=4)

    def display_tournaments(self):
        self.load_tournaments_from_json()
        self.tournament_view.display_tournaments(self.tournaments)

    def add_tournament(self, name, location, start_date, end_date, players, description):
        self.tournaments.clear()
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