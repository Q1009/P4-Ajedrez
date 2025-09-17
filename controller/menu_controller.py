from view.menu_view import MenuView
from rich.console import Console
from controller.player_controller import ChessPlayerController
from view.player_view import PlayerView

class MenuController:
    def __init__(self, menu_view):
        self.menu_view = menu_view

    def display_menu(self):
        self.menu_view.display_menu_view()

    def execute(self):
        
        running = True
        while running:
            self.display_menu()
            choice = self.menu_view.console.input("\n[bold green]Sélectionnez une section (1-4) : [/bold green]")
            if choice == "1":
                self.menu_view.display_section_message("Tournois")
                # Ajouter la logique pour gérer les tournois ici
            elif choice == "2":
                self.menu_view.display_section_message("Joueurs")
                # Ajouter la logique pour gérer les joueurs ici
                player_view = PlayerView()
                player_controller = ChessPlayerController(player_view)
                player_controller.execute()
                #fin du player view loop
            elif choice == "3":
                self.menu_view.display_section_message("Rapports")
                # Ajouter la logique pour gérer les rapports ici
            elif choice == "4":
                self.menu_view.display_exit_message()
                running = False
            else:
                self.menu_view.display_invalid_choice_message()