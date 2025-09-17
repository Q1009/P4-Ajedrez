from view.menu_view import MenuView
from controller.menu_controller import MenuController

def main():
    # Initialisation et exécution du contrôleur principal
    menu_view = MenuView()
    menu_controller = MenuController(menu_view)
    menu_controller.execute()

if __name__ == "__main__":
    main()