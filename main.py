from view.menu_view import MenuView
from view.player_view import PlayerView
from controller.player_controller import ChessPlayerController

def main():
    # Affichage du menu principal avec la création de l'instance menu_view
    menu_view = MenuView()
    #Mettre dans le choix Joueurs du menu principal

    while True:
        menu_view.display_menu_view()
        menu_view_user_choice = menu_view.console.input("\n[bold green]Sélectionnez une section (1-4) : [/bold green]")
        if menu_view_user_choice == "1":
            menu_view.console.print("[bold magenta]Vous êtes dans la section Tournois.[/bold magenta]")
        elif menu_view_user_choice == "2":
            menu_view.console.print("[bold magenta]Vous êtes dans la section Joueurs.[/bold magenta]")
            player_view = PlayerView()
            while True:
                player_view.display_player_menu_view()
                chess_player_controller = ChessPlayerController()
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
                    player_view.console.print(f"[bold green]Le joueur {name} {surname} a été ajouté avec succès ![/bold green]")
                elif player_view_user_choice == "3":
                    player_view.console.print("[bold magenta]Supprimer un joueur sélectionné.[/bold magenta]")
                    # Ici, ajouter la logique pour supprimer un joueur
                    index = int(player_view.console.input("Index du joueur à supprimer : "))
                    chess_player_controller.remove_player(index)
                elif player_view_user_choice == "4":
                    player_view.console.print("[bold magenta]Modifier un joueur sélectionné.[/bold magenta]")
                    index = int(player_view.console.input("Index du joueur à modifier : "))
                    while True:
                        player_view.display_modify_player_view(index)
                        # Ici, ajouter la logique pour modifier un joueur
                        modify_player_view_user_choice = player_view.console.input("\n[bold green]Sélectionnez une action (1-6) : [/bold green]")
                        if modify_player_view_user_choice == "1":
                            surname = player_view.console.input("Nouveau nom : ")
                            chess_player_controller.modify_player(index, surname=surname)
                        elif modify_player_view_user_choice == "2":
                            name = player_view.console.input("Nouveau prénom : ")
                            chess_player_controller.modify_player(index, name=name)
                        elif modify_player_view_user_choice == "3":
                            date_of_birth = player_view.console.input("Nouvelle date de naissance (YYYY-MM-DD) : ")
                            chess_player_controller.modify_player(index, date_of_birth=date_of_birth)
                        elif modify_player_view_user_choice == "4":
                            federation_chess_id = player_view.console.input("Nouveau identifiant fédération : ")
                            chess_player_controller.modify_player(index, federation_chess_id=federation_chess_id)
                        elif modify_player_view_user_choice == "5":
                            elo = player_view.console.input("Nouvel Elo : ")
                            chess_player_controller.modify_player(index, elo=elo)
                        elif modify_player_view_user_choice == "6":
                            break
                        else:
                            player_view.console.print("[bold red]Choix invalide, veuillez réessayer.[/bold red]")
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