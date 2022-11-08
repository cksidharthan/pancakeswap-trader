from web3 import Web3
from web3.eth import Contract
from bsc import base


def get_contract(web: Web3) -> Contract:
    return web.eth.contract(address=base.pancakeswap_router_address, abi=base.pancakeswap_abi)


def get_web3():
    web3 = Web3(Web3.HTTPProvider(base.bsc_node_url))
    try:
        web3.isConnected()
    except Exception as e:
        print("error creating web3 connection", e)
        return False
    return web3
