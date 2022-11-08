import os
import platform
from fastapi import FastAPI
from dotenv import load_dotenv
from bsc import balance, buy
import logging

if platform.system() != "Darwin":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='trade.log',
    )
else:
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

bsc_node_url = os.getenv("BSC_NODE_URL")
pancakeswap_router_address = os.getenv("PANCAKESWAP_ROUTER_ADDRESS")


app = FastAPI()

# load the environment variables
load_dotenv("config.env")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/buy")
def buy_token(token_address: str, amount: float):
    return {"message": buy.buy_token(token_address, bnb_qty=amount)}


@app.get("/balance")
def get_balance():
    return {"balance": balance.get_balance()}
