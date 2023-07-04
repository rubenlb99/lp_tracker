from typing import Dict
from web3 import Web3
from .utils import getContractAbiFTM, getTokenDecimals, getTokenSymbol


contract_address = '0x9083EA3756BDE6Ee6f27a6e996806FBD37F6F093'

class SpiritSwap:
    def __init__(self, web3: Web3):
        # Check if connected correctly
        if (not web3.isConnected()):
            raise ConnectionError('Error connecting to fantom rpc')

        
        contract_abi = getContractAbiFTM(contract_address)
        self.contract_instance = web3.eth.contract(address=contract_address, abi=contract_abi)
        self.web3 = web3


    def getUserLiquidity(self, address: str) -> Dict:
        poolLength = self._poolLength()
        reward_token = self._rewardToken()

        user_liquidity = {'user_liquidity': []}
        for i in range(0, poolLength):
            amount, reward_debt = self._userInfo(i, address)
            if (amount != 0):
                lp_token = self._poolInfo(i)[0]
                #lpTokens = float(Web3.fromWei(amount, 'ether'))
                pool = {
                    'is_lp': 1,
                    'amount': amount,
                    'reward_debt': reward_debt,
                    'token_address': lp_token,
                    'reward_token': reward_token,
                    'lp_info': self._getLpInfo(lp_token)
                }
                user_liquidity['user_liquidity'].append(pool)
        
        return user_liquidity


    # ------------------  CONTRACT FUNCTIONS  --------------------- #
    def _poolInfo(self, pid: int) -> list:
        # [lpToken address, allocPoint uint256, lastRewardBlock uint256, accSpiritPerShare uint256, depositFeeBP uint16]
        return self.contract_instance.functions.poolInfo(pid).call()

    def _userInfo(self, pid: int, address: str) -> list:
        #  [amount (lpTokens) uint256, rewardDebt uint256]
        return self.contract_instance.functions.userInfo(pid, address).call()

    def _poolLength(self) -> int:
        # Number of pools under this contract
        return self.contract_instance.functions.poolLength().call()

    def _rewardToken(self) -> str:
        # Spirit token address
        # HARD CODED TO SAVE ONE REQUEST
        return Web3.toChecksumAddress('0x5cc61a78f164885776aa610fb0fe1257df78e59b')

    # ------------------  LP TOKEN FUNCTIONS  --------------------- #
    def _getLpInfo(self, lp_address: str):
        contract = self.web3.eth.contract(address=lp_address, abi=getContractAbiFTM(lp_address))
        # Token0 contract
        token_0 = contract.functions.token0().call()
        # Token1 contract
        token_1 = contract.functions.token1().call()      

        # We obtain the supply of token0 and token1 in the lp
        reserves_token0, reserves_token1, *_ = contract.functions.getReserves().call()

         # We obtain the total supply of the lp token
        total_supply = contract.functions.totalSupply().call()

        token0_symbol = getTokenSymbol(self.web3, token_0)
        token1_symbol = getTokenSymbol(self.web3, token_1)
        
        token0_decimals = getTokenDecimals(self.web3, token_0)
        token1_decimals = getTokenDecimals(self.web3, token_1)

        return {
            'tokens': 
                    [
                        {'address': token_0, 'reserves': reserves_token0, 'symbol': token0_symbol, 'decimals': token0_decimals}, 
                        {'address': token_1, 'reserves': reserves_token1, 'symbol': token1_symbol, 'decimals': token1_decimals}
                    ],
            'total_supply': total_supply
        }