from core.currency import Currency
from core.utils import get_currency_by_order

class InventoryItem:
    def __init__(self, item: object, amount: int, type: str):
        self.item = item
        self.amount = amount
        self.type = type

    def get_item(self) -> object:
        return self.item

    def get_amount(self) -> int:
        return self.amount

    def add_amount(self, amount: int):
        self.amount += amount

    def subtract_amount(self, amount: int):
        self.amount -= amount

    def get_type(self) -> str:
        return self.type

    def to_dict(self) -> dict:
        result = {
            'type': self.get_type(),
            'amount': self.amount
        }
        # If the item is a Currency, save its data
        if self.item and isinstance(self.item, Currency):
            result['currency'] = self.item.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: dict):
        item = None
        # If currency data exists, reconstruct the Currency object
        if 'currency' in data:
            item = Currency.from_dict(data['currency'])
        
        return cls(
            item=item,
            amount=data['amount'],
            type=data['type']
        )

class User:

    def __init__(self):
        self.money = 0
        self.inventory = [InventoryItem(get_currency_by_order(1), 0, 'currency')]
        self.current_currency = self.inventory[-1].get_item()

    def get_money(self) -> int:
        return self.money

    def get_money_str(self) -> str:
        if self.money < 1:
            return f"{self.money:,.2f}"
        
        return f"{self.money:,.0f}"

    def get_current_currency(self) -> Currency:
        return self.current_currency

    def get_inventory(self) -> list[InventoryItem]:
        return self.inventory

    def set_current_currency(self, currency: Currency):
        self.inventory.append(InventoryItem(currency, 0, 'currency'))
        self.current_currency = currency

    def add_new_item(self, item: object):
        self.inventory.append(InventoryItem(item, 0, item.get_type()))
        self.current_currency = item

    def unlock_new_currency(self, currency: Currency):
        self.inventory.append(InventoryItem(currency, 0, 'currency'))
        self.current_currency = currency

    def update_item_amount(self, item_type: str, amount: int):
        for item in self.inventory:
            if item.get_item().get_type() == item_type:
                item.add_amount(amount)
                break

    def sell_currency_inventory_item(self, item: InventoryItem):
        self.add_money(item.get_amount() * item.get_item().get_add_amount() if item.get_item() else 0)
        item.subtract_amount(item.get_amount())

    def sell_all_currency_inventory_items(self):
        total_sold = 0
        for item in self.inventory:
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

    def to_dict(self) -> dict:
        return {
            'money': self.money,
            'inventory': [item.to_dict() for item in self.inventory],
            'current_currency': self.current_currency.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        user = cls()
        user.money = data['money']
        user.inventory = [InventoryItem.from_dict(item) for item in data['inventory']]
        user.current_currency = Currency.from_dict(data['current_currency'])
        return user
