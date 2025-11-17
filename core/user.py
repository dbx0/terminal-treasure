from core.currency import Currency
from core.utils import get_currency_by_order
from core.inventory import InventoryItem, Inventory

class User:

    def __init__(self):
        self.money = 0
        self.inventory = Inventory()
        self.current_currency = get_currency_by_order(1)
        self.inventory.add_item(InventoryItem(self.current_currency, 0, 'currency'))
        self.stars_collected = 0


    def get_money(self) -> int:
        return self.money

    def get_money_str(self) -> str:
        if self.money < 1:
            return f"{self.money:,.2f}"
        
        return f"{self.money:,.0f}"

    def get_current_currency(self) -> Currency:
        return self.current_currency

    def get_inventory(self) -> Inventory:
        return self.inventory

    def set_current_currency(self, currency: Currency):
        self.inventory.add_item(InventoryItem(currency, 0, 'currency'))
        self.current_currency = currency

    def add_new_item(self, item: object):
        self.inventory.add_item(InventoryItem(item, 0, item.get_type()))
        self.current_currency = item

    def unlock_new_currency(self, currency: Currency):
        self.inventory.add_item(InventoryItem(currency, 0, 'currency'))
        self.current_currency = currency

    def update_item_amount(self, item_type: str, amount: int):
        item = self.inventory.find_item_by_type(item_type)
        if item:
            item.add_amount(amount)
            return

    def sell_currency_inventory_item(self, item: InventoryItem):
        self.add_money(item.get_amount() * item.get_item().get_add_amount() if item.get_item() else 0)
        item.subtract_amount(item.get_amount())

    def sell_all_currency_inventory_items(self):
        total_sold = 0
        for item in self.inventory.get_items():
            if item.get_type() == 'currency':
                amount_before = item.get_amount()
                self.sell_currency_inventory_item(item) 
                total_sold += amount_before * item.get_item().get_add_amount() if item.get_item() else 0
        return total_sold

    def add_money(self, amount: int):
        self.money += amount

    def subtract_money(self, amount: int):
        self.money -= amount

    def set_money(self, amount: int):
        self.money = amount

    def get_stars_collected(self) -> int:
        return self.stars_collected

    def increment_stars_collected(self):
        self.stars_collected += 1

    def to_dict(self) -> dict:
        return {
            'money': self.money,
            'inventory': [item.to_dict() for item in self.inventory.get_items()],
            'current_currency': self.current_currency.to_dict(),
            'stars_collected': self.stars_collected
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        user = cls()
        user.money = data['money']
        user.inventory = Inventory()
        for item in data['inventory']:
            user.inventory.add_item(InventoryItem.from_dict(item))
        user.current_currency = Currency.from_dict(data['current_currency'])
        user.stars_collected = data.get('stars_collected', 0)
        return user
