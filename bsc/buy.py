import time
from bsc import base, bsc, balance
import base64
import logging


def buy_token(token_address: str, bnb_qty: float):
    logging.info("buy_token: token_address: %s, bnb_qty: %s" % (token_address, bnb_qty))
    if not check_sufficient_balance(bnb_qty):
        return "insufficient balance - %s" % bnb_qty
    try:
        web3 = bsc.get_web3()
        contract = bsc.get_contract(web3)
        nonce = web3.eth.getTransactionCount(base.user_address)
        # build the transaction
        tx = contract.functions.swapExactETHForTokens(
            0,
            [base.bnb_address.strip(), token_address.strip()],  # path
            base.user_address.strip(),  # to
            int(time.time()) + 1000  # deadline
        ).buildTransaction({
            'chainId': 56,
            'gas': 200000,
            'value': web3.toWei(bnb_qty, "ether"),
            'gasPrice': web3.toWei('5', 'gwei'),
            'nonce': nonce,
        })
        user_key = get_string(base.key)
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=user_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        logging.debug("buy_token: tx_receipt: %s" % tx_receipt)
        logging.info("buy_token: tx_hash: %s" % tx_hash.hex())
        return "transaction successful - %s" % web3.toHex(tx_hash)
    except Exception as e:
        print(e)
        return "error buying token %s", e


def check_sufficient_balance(bnb_qty):
    logging.info("check_sufficient_balance: bnb_qty: %s" % bnb_qty)
    bnb_balance = balance.get_balance()
    if bnb_balance < bnb_qty:
        logging.error("insufficient balance %s, requested %s" % (bnb_balance, bnb_qty))
        return False
    return True


def get_string(encoded_string: str) -> str:
    return base64.b64decode(encoded_string).rstrip().decode("utf-8")
