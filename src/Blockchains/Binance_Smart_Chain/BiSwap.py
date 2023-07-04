from typing import Dict
from web3 import Web3
import os
from .utils import getContractAbiBSC

farm = "0xDbc1A13490deeF9c3C12b44FE77b503c1B061739"

class BiSwap:
    
    def __init__(self, web3: Web3):
        # Check if connected correctly
        if (not web3.isConnected()):
            raise ConnectionError('Error connecting to binance smart chain rpc')

        self.web3 = web3

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abi_path = "abi/BiSwapAbi.txt"
        with open(os.path.join(script_dir, abi_path), 'r') as f:
            contract_abi = f.readline()
        
        self.contract_instance = web3.eth.contract(address=Web3.toChecksumAddress(farm), abi=contract_abi)
        self.holder_pool_contract = self.web3.eth.contract(address=Web3.toChecksumAddress('0xa4b20183039b2F9881621C3A03732fBF0bfdff10'), abi=getContractAbiBSC(Web3.toChecksumAddress('0xa4b20183039b2F9881621C3A03732fBF0bfdff10')))
        self.auto_pool_contract = self.web3.eth.contract(address=Web3.toChecksumAddress('0x97A16ff6Fd63A46bf973671762a39f3780Cda73D'), abi=getContractAbiBSC(Web3.toChecksumAddress('0x97A16ff6Fd63A46bf973671762a39f3780Cda73D')))
        
        
        
    def getUserLiquidity(self, address: str) -> Dict:
        user_liquidity = {
            'user_liquidity': []
        }
        reward_token = self._rewardToken()
        length = self._poolLength()


        for i in range(0, length):
            amount, reward_debt = self._userInfo(i, address)
            if (amount != 0):
                lp_token = self._poolInfo(i)[0]
                pool = {
                    'is_lp': 0 if i==0 else 1,
                    'amount': amount,
                    'reward_debt': reward_debt,
                    'token_address': lp_token,
                    'reward_token': reward_token
                }
                
                user_liquidity['user_liquidity'].append(pool)
        
        holder_amount_shares = self.holder_pool_contract.functions.userInfo(address).call()
        
        if(holder_amount_shares[0]!=0):
            holder_total_shares = self.holder_pool_contract.functions.totalShares().call()
            holder_balance_of = self.holder_pool_contract.functions.balanceOf().call()
            
            holder_amount = holder_amount_shares[0]/holder_total_shares*holder_balance_of
            
            pool = {
                        'is_lp': 0,
                        'amount': holder_amount,
                        'reward_debt': -1,
                        'token_address': reward_token,
                        'reward_token': reward_token
            }

            user_liquidity['user_liquidity'].append(pool)
                
        auto_amount_shares = self.auto_pool_contract.functions.userInfo(address).call()
        
        if(auto_amount_shares[0]!=0):
            auto_total_shares = self.auto_pool_contract.functions.totalShares().call()
            auto_balance_of = self.auto_pool_contract.functions.balanceOf().call()
            
            auto_amount = auto_amount_shares[0]/auto_total_shares*auto_balance_of
                    
            pool = {
                        'is_lp': 0,
                        'amount': auto_amount,
                        'reward_debt': -1,
                        'token_address': reward_token,
                        'reward_token': reward_token
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

    def _pendingRewards(self, pid: int, address: str) -> int:
        # Pending cake rewards for a user in a pool
        return self.contract_instance.functions.pendingBSW(pid, address).call()

    def _rewardToken(self) -> str:
        # Cake token address
        # HARD CODED TO SAVE ONE REQUEST
        return '0x965f527d9159dce6288a2219db51fc6eef120dd1'