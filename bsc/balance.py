from bsc import bsc, base


def get_balance():
    web3 = bsc.get_web3()
    balance = web3.eth.getBalance(base.user_address)
    human_readable_balance = web3.fromWei(balance, "ether")
    return human_readable_balance
