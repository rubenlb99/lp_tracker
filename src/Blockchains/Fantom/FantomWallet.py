from typing import Dict
from web3 import Web3
from .utils import getTokenDecimals, getContractAbiFTM, getTokenSymbol

address = '0xFC00FACE00000000000000000000000000000000'

class FantomWallet:

    def __init__(self, web3: Web3):
        # Check if connected correctly
        if (not web3.isConnected()):
            raise ConnectionError('Error connecting to fantom rpc')

        contract_abi = getContractAbiFTM(address)
        self.contract_instance = web3.eth.contract(address=address, abi=contract_abi)
        self.web3 = web3
    
    
    def getUserLiquidity(self, address: str) -> Dict:
        pool_length = self._poolLength()
        tokens = 0
        reward_debt = 0

        for i in range(0, pool_length):
            if ((amount := self._getStake(i, address)) != 0):
                tokens += amount
                reward_debt += self._pendingRewards(address, i)

        user_liquidity = {'user_liquidity': []}
        if (tokens > 0):
            user_liquidity['user_liquidity'].append(
                    {
                        'is_lp': 0, 
                        'amount': tokens,
                        'token_address': self._getTokenAddress(),
                        'reward_debt': reward_debt,
                        'reward_token': self._getTokenAddress(),
                        'token_info': self._getTokenInfo(self._getTokenAddress())
                    }
                )

        return user_liquidity

    def _getTokenAddress(self) -> str:
        # Returns FTM address. This is the staking and rewards token
        return '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'

    # ------------------  TOKEN FUNCTIONS  --------------------- #
    def _getTokenInfo(self, address):
        return {'address': address, 'symbol': getTokenSymbol(self.web3, address), 'decimals': getTokenDecimals(self.web3, address)}


    # ------------------  CONTRACT FUNCTIONS  --------------------- #

    def _getStake(self, pid: int, address: str) -> int:
        # Returns amount of fantom staked in validator
        return self.contract_instance.functions.getStake(address, pid).call()

    def _poolLength(self) -> int:
        # Returns number of nodes available to stake
        return self.contract_instance.functions.lastValidatorID().call()
    
    def _pendingRewards(self, address: str, pid: int) -> int:
        # Pending rewards of a user in a node
        return self.contract_instance.functions.pendingRewards(address, pid).call()

