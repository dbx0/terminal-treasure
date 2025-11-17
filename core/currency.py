class Currency: 
    def __init__(self, type: str, order: int, add_amount: float, symbol: str, color: str, add_rate: int, unlock_cost: int, upgrade_cost: int, multiplier_rate: int):
        self.type = type
        self.order = order
        self.add_amount = add_amount
        self.symbol = symbol
        self.color = color
        self.add_rate = add_rate
        self.unlock_cost = unlock_cost
        self.upgrade_cost = upgrade_cost
        self.multiplier_rate = multiplier_rate
        
    def get_type(self) -> str:
        return self.type
    
    def get_order(self) -> int:
        return self.order
    
    def get_add_amount(self) -> float:
        return self.add_amount

    def get_symbol(self) -> str:
        return self.symbol
    
    def get_color(self) -> str:
        return self.color

    def get_add_rate(self) -> int:
        return self.add_rate

    def get_upgrade_cost(self) -> int:
        return self.upgrade_cost
    
    def get_unlock_cost(self) -> int:
        return self.unlock_cost

    def upgrade_add_amount(self):
        self.add_amount += self.add_amount * self.multiplier_rate
        self.upgrade_cost += self.upgrade_cost * self.multiplier_rate

    def get_multiplier_rate(self) -> int:
        return self.multiplier_rate

    def to_dict(self) -> dict:
        return {
            'type': self.type,
            'order': self.order,
            'add_amount': self.add_amount,
            'symbol': self.symbol,
            'color': self.color,
            'add_rate': self.add_rate,
            'unlock_cost': self.unlock_cost,
            'upgrade_cost': self.upgrade_cost,
            'multiplier_rate': self.multiplier_rate
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            type=data['type'],
            order=data['order'],
            add_amount=data['add_amount'],
            symbol=data['symbol'],
            color=data['color'],
            add_rate=data['add_rate'],
            unlock_cost=data['unlock_cost'],
            upgrade_cost=data['upgrade_cost'],
            multiplier_rate=data['multiplier_rate']
        )
