import os
from .Chains import Chains

class Config():
    os.environ[Chains.FANTOM.value] = 'wss://fantom-mainnet.public.blastapi.io/'
    os.environ[Chains.BINANCE.value] = 'https://bsc-dataseed.binance.org/'