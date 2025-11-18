from blessed import Terminal
from core.user import User
from core.user import InventoryItem
from core.memory import GameMemory
from core.utils import draw_ascii_art, get_next_unlockable_currency, check_memory_file
from core.utils import print_color_text, print_color_text_with_accent, move_cursor_off_screen
from core.ascii import CHEST
import sys
import random
from core.particle import Particle
from core.inventory import Inventory

class Game:

    def __init__(self, term: Terminal, debug: bool = False):
        self.term = term
        self.game_memory = None
        self.debug = debug
        self.show_instructions = True

    def load_game_memory(self):
        if not check_memory_file():
            self.game_memory = GameMemory()
            return

        self.game_memory = GameMemory()
        self.game_memory.load()

        self.user = self.game_memory.read('user')
    
    def _draw_chest(self, buffer: list = None):
        x, y = draw_ascii_art(self.term, CHEST, self.term.width // 2, self.term.height // 2, True, buffer=buffer)
        return x, y

    def _draw_user_inventory(self, inventory: Inventory, selected_item: int, current_coins: int, buffer: list = None):

        def get_top_border(width: int):
            return "┌" + "─" * (width - 2) + "┐"

        def get_header(width: int):
            header_text = "Inventory"
            padding = width - len(header_text) - 2
            left_padding = padding // 2
            right_padding = padding - left_padding
            return "│" + " " * left_padding + header_text + " " * right_padding + "│"

        def get_separator(width: int):
            return "├" + "─" * (width - 2) + "┤"

        def get_bottom_border(width: int):
            return "└" + "─" * (width - 2) + "┘"
        
        inventory_width = 30

        inventory_print_rows = []

        for i, item in enumerate(inventory, start=1):
            item_symbol = item.get_item().get_symbol() if item.get_item() else '-'
            item_type = item.get_item().get_type().capitalize() if item.get_item() else 'Unknown'
            item_amount = f"{item.get_amount():,.0f}" 
            item_current_level = item.get_item().get_current_level()
            item_max_level = item.get_item().get_max_level()
            level_indicator = f"Lv. {item_current_level}" if item_current_level < item_max_level else "MAX"
            item_message = f"{item_symbol} {item_amount} {item_type} ({level_indicator})"

            can_upgrade = item.get_item().get_upgrade_cost() <= current_coins and item.get_item().get_current_level() < item.get_item().get_max_level()

            item_row = {
                'message': item_message,
                'can_upgrade': can_upgrade,
                'selected': i == selected_item,
            }

            inventory_print_rows.append(item_row)

            if len(item_message) > inventory_width:
                inventory_width = len(item_message)

        # Add padding to item rows
        for row in inventory_print_rows:
            spacing = inventory_width - len(row['message']) - 4
            row['message'] = "│" + " " * 2 + row['message'] + " " * (spacing if spacing > 0 else 0) + "│"

        # Build the complete box structure
        top_border = {
            'message': get_top_border(inventory_width),
            'selected': False,
        }
        header = {
            'message': get_header(inventory_width),
            'selected': False,
        }
        separator = {
            'message': get_separator(inventory_width),
            'selected': False,
        }
        bottom_border = {
            'message': get_bottom_border(inventory_width),
            'selected': False,
        }
        
        inventory_print_rows.insert(0, top_border)
        inventory_print_rows.insert(1, header)
        inventory_print_rows.insert(2, separator)
        inventory_print_rows.append(bottom_border)

        row_position = 1
        for row in inventory_print_rows:
            message = f"  {row['message']}"
            is_dim = True
            is_bold = False

            if row['selected']:
                message = f"> {row['message']}"
                is_bold = True
                is_dim = False
            
            if 'can_upgrade' in row and row['can_upgrade']:
                message = print_color_text_with_accent(self.term, message, 0, row_position, 'white', 'light_green', 10, len(message), is_dim, is_bold, buffer=buffer)
            else:
                message = print_color_text(self.term, message, 0, row_position, 'white', is_dim, is_bold, buffer=buffer)
            row_position += 1

    def _draw_instructions_box(self, star_exists: bool = False, can_unlock: bool = False, buffer: list = None):
        if not self.show_instructions:
            return

        def get_top_border(width: int):
            return "┌" + "─" * (width - 2) + "┐"

        def get_header(width: int):
            header_text = "Instructions"
            padding = width - len(header_text) - 2
            left_padding = padding // 2
            right_padding = padding - left_padding
            return "│" + " " * left_padding + header_text + " " * right_padding + "│"

        def get_separator(width: int):
            return "├" + "─" * (width - 2) + "┤"

        def get_bottom_border(width: int):
            return "└" + "─" * (width - 2) + "┘"

        # Define all instruction items
        instructions = [
            ("q", "Quit game"),
            ("s", "Save game"),
            ("m", "Get money"),
            ("a", "Collect star"),
            ("u", "Unlock currency"),
            ("c", "Sell all items"),
            ("i", "Toggle instructions"),
            ("↑/↓", "Navigate inventory"),
            ("Enter", "Upgrade item"),
        ]

        # Calculate box width
        box_width = 25
        for key, desc in instructions:
            line_length = len(f"{key:8} {desc}")
            if line_length > box_width - 4:
                box_width = line_length + 4

        # Build instruction rows
        instruction_rows = []
        for key, desc in instructions:
            instruction_rows.append({
                'message': f"{key:8} {desc}",
                'selected': False,
            })

        # Add padding to instruction rows
        for row in instruction_rows:
            spacing = box_width - len(row['message']) - 4
            row['message'] = "│" + " " * 2 + row['message'] + " " * (spacing if spacing > 0 else 0) + "│"

        # Build the complete box structure
        top_border = {
            'message': get_top_border(box_width),
            'selected': False,
        }
        header = {
            'message': get_header(box_width),
            'selected': False,
        }
        separator = {
            'message': get_separator(box_width),
            'selected': False,
        }
        bottom_border = {
            'message': get_bottom_border(box_width),
            'selected': False,
        }

        instruction_rows.insert(0, top_border)
        instruction_rows.insert(1, header)
        instruction_rows.insert(2, separator)
        instruction_rows.append(bottom_border)

        # Position on the right side of the screen
        start_x = self.term.width - box_width - 2
        row_position = 1

        for row in instruction_rows:
            message = row['message']
            print_color_text(self.term, message, start_x, row_position, 'white', dim=True, buffer=buffer)
            row_position += 1

    def _draw_particles(self, particles: dict, buffer: list = None):
        particles_to_remove = []

        for pid, particle in particles.items():
            particle.update()
            
            if particle.is_expired():
                particles_to_remove.append(pid)
                continue
            
            particle.draw(self.term, buffer=buffer)
        
        for pid in particles_to_remove:
            del particles[pid]

        return particles

    def _draw_star(self, star_x: int, star_y: int, buffer: list = None):
        print_color_text(self.term, '★', star_x, star_y, 'gold', bold=True, buffer=buffer)

    def run(self):
        user = None    

        if not self.game_memory:
            user = User()
            self.game_memory = GameMemory()
            self.game_memory.write('user', user)
        else:
            user = self.game_memory.read('user')
            if user is None:
                user = User()
                self.game_memory.write('user', user)

        selected_item = 1

        money_particles = {}
        money_particle_id = 0
        
        spawn_timer = 0
        money_timer = []
        manual_add_timer = user.get_current_currency().get_add_rate()

        star_exists = False
        star_x = 0
        star_y = 0
        star_spawn_timer = 0

        star_next_spawn_time = random.randint(1800, 3600)

        for item in user.get_inventory().get_items():
            if item.get_type() == 'currency':
                money_timer.append({
                    'item': item.get_item().get_type(),
                    'timer': 0
                })
        
        print(self.term.enter_fullscreen)
        print(self.term.hidden_cursor)
        
        try:
            frame = 0
            with self.term.cbreak():  # Input without Enter key
                while True:
                    # Create output buffer for this frame
                    frame_buffer = []
                    
                    # Clear screen
                    frame_buffer.append(self.term.home + self.term.clear)
                    
                    # Draw chest
                    chest_x, chest_y = self._draw_chest(buffer=frame_buffer)
                    
                    # Update spawn timer
                    spawn_timer += 1
                    if spawn_timer >= user.get_current_currency().get_add_rate():
                        spawn_timer = 0
                        # Spawn new particle
                        money_particles[money_particle_id] = Particle(
                            x=chest_x,
                            y=chest_y,
                            currency=user.get_current_currency()
                        )
                        money_particle_id += 1
                    
                    # Update manual add cooldown timer
                    manual_add_timer += 1
                    
                    if not star_exists:
                        star_spawn_timer += 1
                        if star_spawn_timer >= star_next_spawn_time:
                            # avoid edges
                            star_x = random.randint(5, self.term.width - 5)
                            star_y = random.randint(5, self.term.height - 5)
                            star_exists = True
                            star_spawn_timer = 0
                    
                    if star_exists:
                        self._draw_star(star_x, star_y, buffer=frame_buffer)
                    
                    money_particles = self._draw_particles(money_particles, buffer=frame_buffer)

                    for timer in money_timer:
                        timer['timer'] += 1

                    # Increase the item amount for the currency items
                    for item in user.get_inventory().get_items():
                        for timer in money_timer:
                            item_type = item.get_item().get_type()
                            if timer['item'] == item_type:
                                if timer['timer'] >= item.get_item().get_add_rate():
                                    user.update_item_amount(item_type, item.get_item().get_add_amount())
                                    timer['timer'] = 0

                    self._draw_user_inventory(user.get_inventory().get_items(), selected_item, user.get_money(), buffer=frame_buffer)

                    # Display money
                    current_money = f"You have {user.get_money_str()} coins"

                    print_color_text(self.term, current_money, self.term.width // 2 - len(current_money) // 2, self.term.height // 2 + 2, 'white', bold=True, buffer=frame_buffer)

                    next_unlockable_currency = get_next_unlockable_currency(user.get_current_currency())
                    next_unlockable_currency_cost = 0
                    can_unlock = False
                    if next_unlockable_currency:
                        next_unlockable_currency_cost = next_unlockable_currency.get_unlock_cost()
                        next_unlock_currency_name = next_unlockable_currency.get_type().capitalize()
                        can_unlock = user.get_money() >= next_unlockable_currency_cost
                        if can_unlock:
                            next_unlock_message = f"Press 'u' to unlock {next_unlock_currency_name}"
                            
                            print_color_text(self.term, next_unlock_message, self.term.width // 2 - len(next_unlock_message) // 2 , self.term.height // 2 + 3, 'yellow', bold=True, buffer=frame_buffer)
                        
                    else:
                        next_upgrade_message = "There are no more upgrades available"
                        print_color_text(self.term, next_upgrade_message, self.term.width // 2 - len(next_upgrade_message) // 2 , self.term.height // 2 + 3, 'red', dim=True, buffer=frame_buffer)
                    
                    # Draw instructions box on the right side
                    self._draw_instructions_box(star_exists=star_exists, can_unlock=can_unlock, buffer=frame_buffer)
                    
                    # Flush all buffered output at once
                    for line in frame_buffer:
                        print(line, end='', flush=False)
                    sys.stdout.flush()
                    move_cursor_off_screen(self.term)
                    
                    frame += 1

                    # Check for input
                    key = self.term.inkey(timeout=1/60)  # 60 fps
                    if key and key.lower() == 'm':
                        # Ignore cooldown if debug is on
                        if self.debug or manual_add_timer >= user.get_current_currency().get_add_rate():
                            add_amount = user.get_current_currency().get_add_amount()
                            user.add_money(add_amount)
                            money_particles[money_particle_id] = Particle(
                                x=chest_x,
                                y=chest_y,
                                max_age=60,
                                text=f"+ {add_amount:,.0f}",
                                text_color='light_green'
                            )
                            money_particle_id += 1

                            self.game_memory.write('user', user)
                            
                            # Reset cooldown timer (only if not in debug mode)
                            if not self.debug:
                                manual_add_timer = 0

                    elif key and key.lower() == 's':
                        self.game_memory.write('user', user)
                        self.game_memory.save()

                    elif key and key.lower() == 'q':
                        break
                    elif key and key.lower() == 'i':
                        self.show_instructions = not self.show_instructions
                    elif key and key.lower() == 'c':
                        total_sold = user.sell_all_currency_inventory_items()
                        if total_sold > 0:
                            total_str = f"+ {total_sold:,.0f}" if total_sold >= 1 else f"+ {total_sold:,.2f}"
                            money_particles[money_particle_id] = Particle(
                                x=chest_x,
                                y=chest_y,
                                max_age=60,
                                text=total_str,
                                text_color='light_green'
                            )
                            money_particle_id += 1
                    elif key and key.lower() == 'a':
                        if star_exists:
                            reward = user.get_current_currency().get_add_amount() * 50
                            user.add_money(reward)
                            user.increment_stars_collected()
                            star_exists = False
                            star_spawn_timer = 0
                            star_next_spawn_time = random.randint(1800, 3600)
                            
                            reward_str = f"+ {reward:,.0f}" if reward >= 1 else f"+ {reward:,.2f}"
                            money_particles[money_particle_id] = Particle(
                                x=star_x,
                                y=star_y,
                                max_age=60,
                                text=reward_str,
                                text_color='gold'
                            )
                            money_particle_id += 1
                            
                            self.game_memory.write('user', user)
                        
                    elif key and can_unlock and key.lower() == 'u':
                        user.subtract_money(next_unlockable_currency_cost)
                        user.unlock_new_currency(next_unlockable_currency)
                        money_timer.append({
                            'item': next_unlockable_currency.get_type(),
                            'timer': 0
                        })
                        self.game_memory.write('user', user)

                    elif hasattr(key, 'name') and key.name == 'KEY_UP':
                        if selected_item > 1:
                            selected_item -= 1
                    elif hasattr(key, 'name') and key.name == 'KEY_DOWN':
                        if selected_item < len(user.get_inventory().get_items()):
                            selected_item = min(selected_item + 1, len(user.get_inventory().get_items()))

                    elif key and (key == '\r' or key == '\n' or (hasattr(key, 'code') and key.code == self.term.KEY_ENTER)):
                        selected_item_item = user.get_inventory().get_items()[selected_item - 1]
                        if selected_item_item.get_type() == 'currency':
                            can_upgrade = selected_item_item.get_item().get_upgrade_cost() <= user.get_money() and selected_item_item.get_item().get_current_level() < selected_item_item.get_item().get_max_level()
                            if can_upgrade:
                                user.subtract_money(selected_item_item.get_item().get_upgrade_cost())
                                selected_item_item.get_item().upgrade_add_amount()
                                self.game_memory.write('user', user)
                        
        finally:
            print(self.term.exit_fullscreen)
            print(self.term.normal_cursor)