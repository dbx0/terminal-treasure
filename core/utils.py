from blessed import Terminal
from core.currency import Currency
from core.config import COLORS_RGB, CURRENCIES_CONFIG
import os
import json
import sys

def get_config_currencies():
    return [Currency(**currency) for currency in CURRENCIES_CONFIG]

def draw_ascii_art(term: Terminal, ascii_art: str, x: int, y:int, center: bool, buffer: list = None):

    ascii_matrix = [[char for char in row]for row in ascii_art.split('\n')]

    if center:
        x = x - len(ascii_matrix[0]) // 2
        y = y - len(ascii_matrix) 

    output = []
    for i, row in enumerate(ascii_matrix, 1):
        ascii_x = x
        ascii_y = y + i
        line = term.move_xy(ascii_x, ascii_y) + ''.join(row)
        output.append(line)
    
    if buffer is not None:
        buffer.extend(output)
    else:
        for line in output:
            print(line, end='', flush=False)
        sys.stdout.flush()
    
    return x, y

def print_color_text(term: Terminal, text: str, x: int, y: int, color_name: str, dim: bool = False, bold: bool = False, buffer: list = None):

    color_rgb = COLORS_RGB[color_name]
    color = term.color_rgb(*color_rgb)
    formatted_text = text
    if dim:
        # windows suck
        try:
            formatted_text = term.dim(formatted_text)
        except Exception:
            pass
    if bold:
        formatted_text = term.bold(formatted_text)
    
    output = term.move_xy(x, y) + color(formatted_text) + term.normal
    
    if buffer is not None:
        buffer.append(output)
    else:
        print(output, end='', flush=False)
        sys.stdout.flush()

def get_currency_by_order(order: int) -> Currency:
    currencies = get_config_currencies()
    return next((currency for currency in currencies if currency.get_order() == order), None)

def get_next_upgrade_currency(current_currency: Currency) -> Currency:
    #get next number in the order list
    next_order = current_currency.get_order() + 1
    next_currency = next((currency for currency in get_config_currencies() if currency.get_order() == next_order), None)
    if next_currency:
        return next_currency
    
    return None

def get_project_directory():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_memory_file_path():
    return os.path.join(get_project_directory(), 'save', 'memory.json')

def check_save_file_is_valid(save_file: str):
    if not os.path.exists(save_file):
        return False

    with open(save_file, 'r') as f:
        try:
            json.load(f)
        except json.JSONDecodeError:
            return False
    
    return True

def check_memory_file():
    memory_file = get_memory_file_path()
    if not os.path.exists(memory_file):
        return False
    
    if not check_save_file_is_valid(memory_file):
        return False
    
    return True

