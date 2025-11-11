from core.currency import Currency

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

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item: InventoryItem):
        self.items.append(item)

    def remove_item(self, item: InventoryItem):
        self.items.remove(item)

    def get_items(self) -> list[InventoryItem]:
        return self.items

    def to_dict(self) -> dict:
        return {
            'items': [item.to_dict() for item in self.get_items()]
        }

    @classmethod
    def from_dict(cls, data: dict):
        inventory = cls()
        for item in data['items']:
            inventory.add_item(InventoryItem.from_dict(item))
        return inventory