from model.tournament_model import Tournament, TournamentRound
from model.player_model import ChessPlayer
import json
from utils.tournament_utils import generate_first_round_matches
from utils.tournament_utils import inscribe_match_results
from utils.tournament_utils import generate_round_matches
from datetime import datetime

class ReportController:

    def __init__(self):
        """Initialise le model ChessPlayer."""
        self.chess_players = []
        self.tournaments = []

    def display_players_from_json(self, filepath="data/players.json"):
        self.chess_players.clear()
        self.load_players_from_json()
        return self.chess_players