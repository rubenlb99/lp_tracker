from multiprocessing import Queue
from typing import Dict
import time

from .FantomWallet import *
from .SpookySwap import *
from .SpiritSwap import *
from ..WebProviders import get_provider
from ..Chains import Chains

def get_user_info(address: str, queue: Queue) -> Dict:
    start_time = time.time()
    print("empieza fantom")

    FANTOM_PROVIDER = get_provider(Chains.FANTOM.value)

    fantom_wallet = FantomWallet(FANTOM_PROVIDER).getUserLiquidity(address)
    spookyV2 = SpookySwapV2(FANTOM_PROVIDER).getUserLiquidity(address)
    spookyV3 = SpookySwapV3(FANTOM_PROVIDER).getUserLiquidity(address)
    spirit = SpiritSwap(FANTOM_PROVIDER).getUserLiquidity(address)

    print("--- FANTOM TOOK %s seconds ---" % (time.time() - start_time))

    queue.put(
        {
            Chains.FANTOM.value: {
                'fantom_wallet': fantom_wallet,
                'spooky_v2': spookyV2,
                'spooky_v3': spookyV3,
                'spirit': spirit
            }
        }
    )

if __name__ == '__main__':
    print(get_user_info('0x3C6696a2347329517EC65b971e1dc5EF1bf2556e'))

