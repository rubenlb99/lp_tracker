import requests
from web3 import Web3
import os.path

from keys import FTM_SCAN_API_KEY


def getContractAbiFTM(address: str) -> str or None:
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    filename = os.path.join(script_dir, 'abi/' + address)
    if (os.path.isfile(filename)):
        with open(filename, 'r') as f:
            abi = f.readline()
        return abi

    ABI_ENDPOINT = 'https://api.ftmscan.com/api?module=contract&action=getabi&address=' + address + '&apikey=' + FTM_SCAN_API_KEY
    response = requests.get(ABI_ENDPOINT)
    response_json = response.json()
    abi_json = response_json['result']

    with open(filename, 'w') as f:
        f.write(abi_json)
    
    return abi_json

def getTokenDecimals(web3: Web3, token_address: str) -> int or None:
        # We obtain the decimals in each token to place the comma
        # TODO: These function may raise an exception (in a try catch block)
        # TODO: Because contract is in a proxy (e.g. 0xb86AbCb37C3A4B64f74f59301AFF131a1BEcC787)
        # TODO: So functions are not callable
        try:
            return web3.eth.contract(address=token_address, abi=getContractAbiFTM(token_address)).functions.decimals().call()
        except Exception:
            # Contract may be readed as proxy
            ##token_decimals = self.web3.eth.contract(address=token_address, abi=self._getProxyAbi(token_address, token_abi)).functions.decimals().call()
            ##return token_decimals
            return None

def getTokenSymbol(web3: Web3, token_address: str) -> int:
    token_instance = web3.eth.contract(address=token_address, abi=getContractAbiFTM(token_address))
    return token_instance.functions.symbol().call()

def getProxyAbiFTM(web3: Web3, address: str, abi: str) -> str or None:
    contract = web3.eth.contract(address=address, abi=abi)
    proxy_contract = contract.functions.implementation().call()
    return getContractAbiFTM(proxy_contract)
