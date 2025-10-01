from model.tournament_model import Tournament, TournamentRound
import random
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
            pass

    def save_tournaments_to_json(self, filepath="data/tournaments.json"):
        data = []
        for tournament in self.tournaments:
            data.append(tournament.to_dict())
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def display_tournaments(self):
        self.tournaments.clear()
        self.load_tournaments_from_json()
        return self.tournaments

    def add_tournament(self, name, location, start_date, end_date, description):
        self.tournaments.clear()
        self.load_tournaments_from_json()
        new_tournament = Tournament(
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            description=description,
            )
        self.tournaments.append(new_tournament)
        self.save_tournaments_to_json()

    def remove_tournament(self, index):
        self.tournaments.clear()
        self.load_tournaments_from_json()
        remove_tournament = self.tournaments.pop(index)
        self.save_tournaments_to_json()
        return remove_tournament.name, remove_tournament.tournament_id

    def modify_tournament(self, index, name=None, location=None, start_date=None, end_date=None, description=None):
        #Rajouter possibilité de modifier les joueurs inscrits
        self.tournaments.clear()
        self.load_tournaments_from_json()
        tournament = self.tournaments[index]
        if name:
            tournament.name = name
        if location:
            tournament.location = location
        if start_date:
            tournament.start_date = start_date
        if end_date:
            tournament.end_date = end_date
        if description:
            tournament.description = description
        self.save_tournaments_to_json()

    def subscribe_players(self, index, player_ids):
        self.tournaments.clear()
        self.load_tournaments_from_json()
        tournament = self.tournaments[index]
        subscribed_ids = []
        already_subscribed_ids = []
        for pid in player_ids:
            if pid not in tournament.players:
                tournament.players.append(pid)
                subscribed_ids.append(pid)
            else:
                already_subscribed_ids.append(pid)
        self.save_tournaments_to_json()
        return subscribed_ids, already_subscribed_ids

    def get_tournament(self, index):
        self.tournaments.clear()
        self.load_tournaments_from_json()
        return self.tournaments[index]
    
    def get_tournaments_count(self):
        self.tournaments.clear()
        self.load_tournaments_from_json()
        return len(self.tournaments)
    
    def start_tournament(self, index):
        self.tournaments.clear()
        self.load_tournaments_from_json()
        tournament = self.tournaments[index]
        tournament.current_round = 1
        tournament.number_of_rounds = len(tournament.players) - 1
        tournament.status = "En cours"
        # Instancier le premier round
        matches = self.generate_first_round_matches(tournament.players)
        first_round = TournamentRound(round_number=1, matches=matches)
        tournament.rounds.append(first_round.round_id)
        self.save_tournaments_to_json()

    def generate_first_round_matches(self, players):
        random.shuffle(players)
        matches = []
        for i in range(len(players)//2):
            match = ([players[i], ""], [players[(i+1)], ""]) # ([joueur_i, score_joueur_i], [joueur_i+1, score_joueur_i+1])
            matches.append(match)

        return matches

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