from view.menu_view import MenuView
from view.player_view import PlayerView
from controller.player_controller import ChessPlayerController

def main():
    # Affichage du menu principal avec la création de l'instance menu_view
    menu_view = MenuView()
    chess_player_controller = ChessPlayerController()
    while True:
        menu_view.display_menu_view()
        menu_view_user_choice = menu_view.console.input("\n[bold green]Sélectionnez une section (1-4) : [/bold green]")
        if menu_view_user_choice == "1":
            menu_view.console.print("[bold magenta]Vous êtes dans la section Tournois.[/bold magenta]")
        elif menu_view_user_choice == "2":
            menu_view.console.print("[bold magenta]Vous êtes dans la section Joueurs.[/bold magenta]")
            player_view = PlayerView()
            while True:
                player_view.display_player_view()
                player_view_user_choice = player_view.console.input("\n[bold green]Sélectionnez une action (1-5) : [/bold green]")
                if player_view_user_choice == "1":
                    #while True:
                    chess_player_controller.display_players_from_json()
                elif player_view_user_choice == "2":
                    player_view.console.print("[bold magenta]Ajouter un joueur.[/bold magenta]")
                    # Ici, ajouter la logique pour ajouter un joueur
                    surname = player_view.console.input("Nom de famille : ")
                    name = player_view.console.input("Prénom : ")
                    date_of_birth = player_view.console.input("Date de naissance (YYYY-MM-DD) : ")
                    federation_chess_id = player_view.console.input("Identifiant fédération : ")
                    elo_input = player_view.console.input("ELO (1000-2500) : ")
                    elo = int(elo_input)
                    # Ici, ajouter la logique pour sauvegarder le joueur
                    chess_player_controller.add_player(surname, name, date_of_birth, federation_chess_id, elo)
                elif player_view_user_choice == "3":
                    player_view.console.print("[bold magenta]Supprimer un joueur sélectionné.[/bold magenta]")
                    # Ici, ajouter la logique pour supprimer un joueur
                elif player_view_user_choice == "4":
                    player_view.console.print("[bold magenta]Modifier un joueur sélectionné.[/bold magenta]")
                    # Ici, ajouter la logique pour modifier un joueur
                elif player_view_user_choice == "5":
                    break
                else:
                    player_view.console.print("[bold red]Choix invalide, veuillez réessayer.[/bold red]")
        elif menu_view_user_choice == "3":
            menu_view.console.print("[bold magenta]Vous êtes dans la section Rapports.[/bold magenta]")
        elif menu_view_user_choice == "4":
            menu_view.console.print("[bold red]Au revoir ![/bold red]")
            break
        else:
            menu_view.console.print("[bold red]Choix invalide, veuillez réessayer.[/bold red]")

if __name__ == "__main__":
    main()