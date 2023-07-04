from typing import Dict
from web3 import Web3
import requests
import math

from .Fantom.utils import *
from .Binance_Smart_Chain.utils import *
from model.Token import Token
from model.LpInfo import LpInfo
from .Chains import Chains
from keys import MORALIS_API_KEY


class PriceCalculator:

    def __init__(self, chain: str):
        # Web3 instance and chain name
        chains = [member.value for member in Chains]
        if (chain not in chains):
            raise Exception('Chain provided to PriceCalculator not supported')
        self.chain = chain

    def getLpInfo(self, pool_info: Dict) -> LpInfo:
        lp_info = pool_info['lp_info']
        n_token = len(lp_info['tokens'])

        tokens_value = 0
        tokens_info: list[Token] = []
        for i in range(n_token):
            token_address = lp_info['tokens'][i]['address']
            token_symbol = lp_info['tokens'][i]['symbol']
            reserves_token = lp_info['tokens'][i]['reserves']
            token_decimals = lp_info['tokens'][i]['decimals']
            token_price = self.getTokenPrice(token_address)

            total_supply_token = float(reserves_token / math.pow(10, token_decimals))
            tokens_value += token_price * total_supply_token
            
            new_token = Token(token_address, token_symbol, supply=total_supply_token, decimals=token_decimals, price=token_price)
            tokens_info.append(new_token)
        
        total_supply = float(Web3.fromWei(lp_info['total_supply'], 'ether'))
        lp_price = tokens_value / total_supply
        
        for token in tokens_info:
            percentage_token = token.getPrice() * token.getSupply() / (total_supply * lp_price)
            token.setPercentage(percentage_token)

        lp_info = LpInfo(pool_info['token_address'], tokens_info)
        lp_info.setPrice(lp_price)
        
        # We erase the blockchain info from the dictionary
        del pool_info['lp_info']

        return lp_info


    def getTokenInfo(self, token_info: Dict) -> Token:
        address = token_info['token_info']['address']
        token_price = self.getTokenPrice(address)
        symbol = token_info['token_info']['symbol']
        decimals = token_info['token_info']['decimals']
        del token_info['token_info']
        return Token(address, symbol, decimals, price=token_price)


    def getTokenPrice(self, token_address: str) -> float:
        price_request = 'https://deep-index.moralis.io/api/v2/erc20/' + token_address + '/price?chain=' + self.chain
        headers = {
            'x-api-key': MORALIS_API_KEY
        }
        response = requests.get(price_request, headers=headers)
        resp = response.json()
        token_priceUSD = resp['usdPrice']
        return token_priceUSD
