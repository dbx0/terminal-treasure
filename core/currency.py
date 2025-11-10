class Currency: 
    def __init__(self, type: str, order: int, add_amount: float, symbol: str, color: str, add_rate: int, upgrade_cost: int):
        self.type = type
        self.order = order
        self.add_amount = add_amount
        self.symbol = symbol
        self.color = color
        self.add_rate = add_rate
        self.upgrade_cost = upgrade_cost
        
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

    def to_dict(self) -> dict:
        return {
            'type': self.type,
            'order': self.order,
            'add_amount': self.add_amount,
            'symbol': self.symbol,
            'color': self.color,
            'add_rate': self.add_rate,
            'upgrade_cost': self.upgrade_cost
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
            upgrade_cost=data['upgrade_cost']
        )
