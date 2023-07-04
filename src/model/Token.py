from typing import Dict


class Token:
    def __init__(self, address: str, symbol: str, decimals: int, supply: float = None, percentage: float = None, price: float = None):
        self.address = address
        self.symbol = symbol
        self.price = price
        self.percentage = percentage
        self.supply = supply
        self.decimals = decimals

    def getTokenAddress(self) -> str:
        return self.address

    def getSymbol(self) -> str:
        return self.symbol

    def getPrice(self) -> float or None:
        return self.price
    
    def getPercentage(self) -> float:
        return self.percentage

    def getSupply(self) -> float:
        return self.supply
    
    def getDecimals(self) -> int:
        return self.decimals
    
    def setPrice(self, price):
        self.price = price
    
    def setPercentage(self, percentage):
        self.percentage = percentage

    def toJson(self) -> Dict:
        return {
            'symbol': self.getSymbol(),
            'price': self.getPrice(),
            'address': self.getTokenAddress()
        }