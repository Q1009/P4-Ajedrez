from menu_view import MenuView
from player_view import PlayerView

def main():
    # Affichage du menu principal avec la création de l'instance menu_view
    menu_view = MenuView()
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
                player_view_user_choice = player_view.console.input("\n[bold green]Sélectionnez une action (1-4) : [/bold green]")
                if player_view_user_choice == "1":
                    player_view.console.print("[bold magenta]Ajouter un joueur sélectionné.[/bold magenta]")
                    # Ici, ajouter la logique pour ajouter un joueur
                elif player_view_user_choice == "2":
                    player_view.console.print("[bold magenta]Supprimer un joueur sélectionné.[/bold magenta]")
                    # Ici, ajouter la logique pour supprimer un joueur
                elif player_view_user_choice == "3":
                    player_view.console.print("[bold magenta]Modifier un joueur sélectionné.[/bold magenta]")
                    # Ici, ajouter la logique pour modifier un joueur
                elif player_view_user_choice == "4":
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