import os
import requests

from keys import POLYGON_SCAN_API_KEY

def getContractAbiPolygon(address) -> str or None:
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    filename = os.path.join(script_dir, 'abi/' + address)
    if (os.path.isfile(filename)):
        with open(filename, 'r') as f:
            abi = f.readline()
        return abi

    ABI_ENDPOINT = 'https://api.polygonscan.com/api?module=contract&action=getabi&address=' + address + '&apikey=' + POLYGON_SCAN_API_KEY
    response = requests.get(ABI_ENDPOINT)
    response_json = response.json()
    abi_json = response_json['result']

    with open(filename, 'w') as f:
        f.write(abi_json)
    
    return abi_json