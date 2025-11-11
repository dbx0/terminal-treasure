from blessed import Terminal
from core.currency import Currency
from core.utils import print_color_text

class Particle:
    def __init__(self, x: int, y: int, currency: Currency = None, max_age: int = None, 
                 symbol: str = None, color: str = None, text: str = None, text_color: str = None):
        self.x = x
        self.y = y
        self.age = 0
        self.text = text
        self.text_color = text_color
        
        if currency:
            self.currency = currency
            self.max_age = currency.get_add_rate()
            self.symbol = currency.get_symbol()
            self.color = currency.get_color()
            self.text_color = text_color or currency.get_color()
        else:
            self.currency = None
            self.max_age = max_age or 60
            self.symbol = symbol or ''
            self.color = color or 'white'
            self.text_color = text_color or color or 'white'
    
    def update(self):
        self.age += 1
        if self.age % 3 == 0:
            self.y -= 1
    
    def is_expired(self) -> bool:
        return self.age > self.max_age or self.y < 0
    
    def get_fade_ratio(self) -> float:
        return 1 - (self.age / self.max_age)
    
    def draw(self, term: Terminal, buffer: list = None):
        fade_ratio = self.get_fade_ratio()

        if self.text:
            if fade_ratio > 0.66:
                print_color_text(term, self.text, self.x + 2, self.y, self.text_color, bold=True, buffer=buffer)
            elif fade_ratio > 0.33:
                print_color_text(term, self.text, self.x + 2, self.y, self.text_color, buffer=buffer)
            else:
                print_color_text(term, self.text, self.x + 2, self.y, self.text_color, dim=True, buffer=buffer)
        else:
            if fade_ratio > 0.66:
                print_color_text(term, self.symbol, self.x + 2, self.y, self.color, bold=True, buffer=buffer)
            elif fade_ratio > 0.33:
                print_color_text(term, self.symbol, self.x + 2, self.y, self.color, buffer=buffer)
            else:
                print_color_text(term, self.symbol, self.x + 2, self.y, self.color, dim=True, buffer=buffer)
