from enum import Enum
import os

from web3 import Web3
from .Chains import Chains

class WebProviders(Enum):
    FANTOM = Web3(Web3.WebsocketProvider(os.environ.get(Chains.FANTOM.value)))
    BINANCE =  Web3(Web3.HTTPProvider(os.environ.get(Chains.BINANCE.value)))



def get_provider(chain: str):
    if (Chains.FANTOM.value == chain):
        return WebProviders.FANTOM.value
    elif (Chains.BINANCE.value == chain):
        return WebProviders.BINANCE.value