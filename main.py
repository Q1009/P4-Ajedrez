"""
Application entry point for Ajedrez.

This module constructs the top-level MenuView and starts the interactive
console application.

Usage
-----
Run this module as a script to start the application:

    python main.py
"""

from view.menu_view import MenuView


def main():
    """
    Initialize and run the main menu view.

    The function creates a MenuView instance and enters its main loop by
    calling execute(). This function is the central entry point used when
    launching the application as a script.

    Returns
    -------
    None
    """
    menu_view = MenuView()
    menu_view.execute()


if __name__ == "__main__":
    main()