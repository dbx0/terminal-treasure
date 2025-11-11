import argparse
from blessed import Terminal
from core.game import Game
from core.menu import Menu

parser = argparse.ArgumentParser(description='A game about money')
parser.add_argument('--debug', action='store_true', help='Enable debug mode')
args = parser.parse_args()

debug = args.debug

if __name__ == '__main__':
    try:
        term = Terminal()
        menu = Menu(term)
        menu_result = menu.show()

        game = None
        if menu_result == -1:
            exit()
        elif menu_result == 0:
            game = Game(term, debug)
            game.run()
        elif menu_result == 1:
            game = Game(term, debug)
            game.load_game_memory()
            game.run()
    except KeyboardInterrupt:
        print(term.normal_cursor)
        print(term.exit_fullscreen)
        exit()