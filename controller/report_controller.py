class ReportController:
    """Controller coordinating report generation data.

    Attributes
    ----------
    chess_players : list
        In-memory list of ChessPlayer objects or dicts used to build reports.
    tournaments : list
        In-memory list of Tournament objects or dicts used to build reports.
    """

    def __init__(self):
        """
        Initialize the ReportController.

        Sets up empty containers for players and tournaments. Callers should
        populate these via load_data() or by assigning data before asking the
        ReportView to render reports.
        """
        self.chess_players = []
        self.tournaments = []
