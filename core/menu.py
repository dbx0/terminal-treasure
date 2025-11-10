from blessed import Terminal
from core.memory import GameMemory
from core.utils import check_memory_file
from core.utils import print_color_text
from core.ascii import GAME_NAME
from core.config import COLORS_RGB
class Menu:

    def __init__(self, term: Terminal):
        self.term = term

    def show(self):

        print(self.term.enter_fullscreen)
        print(self.term.hidden_cursor)
        try:

            memory_file_exists = check_memory_file()

            menu_items = [
                {
                    'name': 'start',
                    'label': 'New Game',
                    'enabled': True,
                    'color': 'light_yellow',
                    'selected_color': 'yellow'   ,
                    'return': 0
                },
                {
                    'name': 'load',
                    'label': 'Load Game',
                    'enabled': memory_file_exists,
                    'color': 'light_yellow',
                    'selected_color': 'yellow',
                    'return': 1
                },
                {
                    'name': 'exit',
                    'label': 'Exit',
                    'enabled': True,
                    'color': 'light_brown',
                    'selected_color': 'brown',
                    'return': -1
                }
            ]


            largest_label_length = max(len(item['label']) for item in menu_items)
            starting_position_x = self.term.width // 2 - largest_label_length + 3 

            selected_item = 0
            with self.term.cbreak():
                while True:
                    print(self.term.home + self.term.clear)
                    
                    # Display ASCII game name in gold
                    game_name_lines = GAME_NAME.strip().split('\n')
                    ascii_start_y = self.term.height // 2 - len(menu_items) // 2 - len(game_name_lines) - 2
                    gold_rgb = COLORS_RGB['gold']
                    gold_color = self.term.color_rgb(*gold_rgb)
                    for i, line in enumerate(game_name_lines):
                        ascii_start_x = self.term.width // 2 - len(line) // 2
                        colored_line = gold_color(line) + self.term.normal
                        print(self.term.move_xy(ascii_start_x, ascii_start_y + i) + colored_line)
                    
                    # Display "a game by dbx0" in dim text below the game name
                    credit_text = "a game by dbx0"
                    credit_y = ascii_start_y + len(game_name_lines) + 1
                    credit_x = self.term.width // 2 - len(credit_text) // 2
                    print_color_text(self.term, credit_text, credit_x, credit_y, 'light_yellow', dim=True)
                    
                    for i, item in enumerate(menu_items):
                        if not item['enabled']:
                            print_color_text(self.term, f"{i + 1}. {item['label']}", starting_position_x, self.term.height // 2 + i, item['color'], dim=True)
                        else:
                            print_color_text(self.term, f"{i + 1}. {item['label']}", starting_position_x, self.term.height // 2 + i, item['color'])
                        if i == selected_item:
                            print_color_text(self.term, f"{i + 1}. {item['label']}", starting_position_x, self.term.height // 2 + i, item['selected_color'], bold=True)
                        
                    key = self.term.inkey(timeout=1/60)
                    if not key:
                        continue
                    if hasattr(key, 'name') and key.name == 'KEY_DOWN':
                        # Find next enabled item
                        for i in range(len(menu_items)):
                            next_index = (selected_item + i + 1) % len(menu_items)
                            if menu_items[next_index]['enabled']:
                                selected_item = next_index
                                break
                    elif hasattr(key, 'name') and key.name == 'KEY_UP':
                        # Find previous enabled item
                        for i in range(len(menu_items)):
                            prev_index = (selected_item - i - 1) % len(menu_items)
                            if menu_items[prev_index]['enabled']:
                                selected_item = prev_index
                                break
                    elif (hasattr(key, 'name') and key.name == 'KEY_ENTER') or key == '\r' or key == '\n':
                        if menu_items[selected_item]['enabled']:
                            return menu_items[selected_item]['return']
                    elif (isinstance(key, str) and key.lower() == 'q') or (hasattr(key, 'name') and key.name == 'KEY_ESCAPE'):
                        return -1
        finally:
            print(self.term.exit_fullscreen)
            print(self.term.normal_cursor)
