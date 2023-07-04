from typing import Dict, List
from .Token import Token

class LpInfo:
    def __init__(self, address: str, tokens_info: List[Token], price: int = None):
        self.address = address
        self.tokens_info = tokens_info
        self.price = price

    def getAddress(self) -> str:
        return self.address
    
    def getTokensInfo(self) -> List[Token]:
        return self.tokens_info

    def getPrice(self) -> float:
        return self.price

    def setPrice(self, price):
        self.price = price


    def toJson(self, lp_tokens) -> Dict:
        response_obj = {}
        tokens = self.getTokensInfo()
        for i, token in enumerate(tokens):
            token_json = token.toJson()
            token_json['amount'] = (token.getPercentage() * lp_tokens * self.getPrice()) / token.getPrice()
            response_obj['token' + str(i)] = token_json

            """response_obj['token' + str(i)] = {
                'amount': (token.getPercentage() * lp_tokens * self.getPrice()) / token.getPrice(),
                'price': token.getPrice(),
                'symbol': token.getSymbol(),
                'address': token.getTokenAddress()
            }"""
        
        return {'lp_info': {'tokens': response_obj}}