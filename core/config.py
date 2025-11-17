CURRENCIES_CONFIG = [
    {
        'type': 'nickels',
        'order': 1,
        'add_amount': 1,
        'symbol': 'o',
        'color': 'yellow',
        'add_rate': 60, # 60 means 1 second
        'unlock_cost': 100,
        'upgrade_cost': 100,
        'multiplier_rate': 0.20
    },
    {
        'type': 'gold bars',
        'order': 2,
        'add_amount': 5,
        'symbol': '■',
        'color': 'gold',
        'add_rate': 50,
        'unlock_cost': 10000,
        'upgrade_cost': 10000,
        'multiplier_rate': 0.10
    },
    {
        'type': 'diamonds',
        'order': 3,
        'add_amount': 100,
        'symbol': '♦',
        'color': 'light_blue',
        'add_rate': 40,
        'unlock_cost': 1000000,
        'upgrade_cost': 1000000,
        'multiplier_rate': 0.05
    },
    {
        'type': 'platinum',
        'order': 4,
        'add_amount': 500,
        'symbol': '♦',
        'color': 'white',
        'add_rate': 30,
        'unlock_cost': 100000000,
        'upgrade_cost': 100000000,
        'multiplier_rate': 0.02
    },
    {
        'type': 'emeralds',
        'order': 5,
        'add_amount': 1000,
        'symbol': '♦',
        'color': 'green',
        'add_rate': 20,      
        'unlock_cost': 10000000000,
        'upgrade_cost': 10000000000,
        'multiplier_rate': 0.01
    },
    {
        'type': 'rubies',
        'order': 6,
        'add_amount': 5000,
        'symbol': '♦',
        'color': 'red',
        'add_rate': 10,
        'unlock_cost': 1000000000000,
        'upgrade_cost': 1000000000000,
        'multiplier_rate': 0.005
    },
    {
        'type': 'sapphires',
        'order': 7,
        'add_amount': 100000,
        'symbol': '♦',
        'color': 'blue',
        'add_rate': 5,
        'unlock_cost': 100000000000000,
        'upgrade_cost': 100000000000000,
        'multiplier_rate': 0.002
    },
    {
        'type': 'amethysts',
        'order': 8,
        'add_amount': 500000,
        'symbol': '♦',
        'color': 'purple',
        'add_rate': 2,
        'unlock_cost': 10000000000000000,
        'upgrade_cost': 10000000000000000,
        'multiplier_rate': 0.001
    }
]

COLORS_RGB = {
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'light_red': (255, 182, 193),
    'green': (0, 255, 0),
    'light_green': (144, 238, 144),
    'yellow': (255, 255, 0),
    'light_yellow': (255, 255, 224),
    'blue': (0, 0, 255),
    'light_blue': (173, 216, 230),
    'magenta': (255, 0, 255),
    'light_magenta': (255, 182, 193),
    'cyan': (0, 255, 255),
    'light_cyan': (175, 238, 238),
    'white': (255, 255, 255),
    'light_white': (245, 245, 245),
    'gold': (255, 215, 0),
    'purple': (128, 0, 128),
    'brown': (165, 42, 42),
    'light_brown': (255, 228, 196)
}