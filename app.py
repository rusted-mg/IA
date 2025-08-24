"""
Point d'entrée principal de l'application d'enquête policière
"""
from ui.main_window import FactEntryWindow

def main():
    """Lance l'application principale"""
    app = FactEntryWindow()
    app.run()

if __name__ == "__main__":
    main()