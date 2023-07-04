import json
from web3 import Web3
import os
import requests
from typing import List
from utils import *


GRAPHQL_URI = 'https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v3-polygon'

class UniSwapPool:
    def __init__(self, address):
        self.address = address


class UniSwap:
    def __init__(self, provider):
        self.web3 = Web3(Web3.WebsocketProvider(provider))
        # Check if connected correctly
        if (not self.web3.isConnected()):
            raise ConnectionError('Error connecting to polygon rpc')


    def getLiquidityPools(self) -> List[UniSwapPool] or None:
        try:
            farms = run_query('query topPools { pools( first: {top}  orderBy: totalValueLockedUSD  orderDirection: desc  subgraphError: allow ) { id }}'.format(30), 200, {})
        except Exception:
            return None

        uni_pools = []
        for farm in farms['data']['pools']:
            uni_pools.append(UniSwapPool(farm['id']))
        
        return uni_pools
    
    def getUserLiquidityInPool(self, user_address, farm_address) -> UniSwapPool:
        contract_abi = getContractAbiPolygon(farm_address)
        self.contract_instance = self.web3.eth.contract(address=farm_address, abi=contract_abi)

        # TODO: INTERACT WITH UNISWAP POOL SMART CONTRACT


def run_query(query, statusCode, headers) -> json or Exception:
    # Method tu run queries to the graphql api of Uniswap
    request = requests.post(GRAPHQL_URI, json={'query': query}, headers=headers)
    if request.status_code == statusCode:
        return request.json()
    else:
        raise Exception(f"Unexpected status code returned: {request.status_code}")


"query pools {\n  pools(\n    where: {id_in: []} block: {number: 31889565}    orderBy: totalValueLockedUSD    orderDirection: desc\n    subgraphError: allow\n  ) {\n    id\n    feeTier\n    liquidity\n    sqrtPrice\n    tick\n    token0 {\n      id\n      symbol\n      name\n      decimals\n      derivedETH\n      __typename\n    }\n    token1 {\n      id\n      symbol\n      name\n      decimals\n      derivedETH\n      __typename\n    }\n    token0Price\n    token1Price\n    volumeUSD\n    txCount\n    totalValueLockedToken0\n    totalValueLockedToken1\n    totalValueLockedUSD __typename\n  }\n}\n"