import time
from pprint import pprint
from typing import Dict, Any

from binance.client import Client
from binance.exceptions import BinanceAPIException
from loguru import logger

from constants import *


if not TESTNET:
    client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)
else:
    client = Client(
        api_key=BINANCE_TESTNET_API_KEY,
        api_secret=BINANCE_TESTNET_API_SECRET,
        testnet=True
    )

def is_tradeable(symbol: str) -> bool:
    """
    Check if the token is listed and tradeable on Binance.
    """
    try:
        exchange_info = client.get_symbol_info(symbol)
        if exchange_info is not None and exchange_info.get('status') == 'TRADING':
            logger.info(f"status: {exchange_info.get('status')}")
            return True
        return False
    except Exception as e:
        logger.error(repr(e))
        return False

def place_sell_order(symbol: str, qty: float) -> Dict[str, Any]:
    """
    Place a sell order for the given token symbol.
    """
    while True:
        if not is_tradeable(symbol):
            logger.info(
                f'Instrument {symbol} not yet tradeable. '
                f'Retrying in {RETRY_DELAY} seconds...'
            )
            time.sleep(RETRY_DELAY)
            continue
        try:
            response = client.order_market_sell(
                symbol=symbol,
                quantity=qty
            )
            logger.info(f'Sell order placed: {response}')
            return response
        except BinanceAPIException as e:
            if 'insufficient balance' in e.message.lower():
                qty = qty - (qty * 0.02)  # Reduce quantity by 2% and retry
                logger.error(
                    f'Error placing sell order due to insufficient balance, '
                    f'retrying with reduced quantity: {qty}'
                )
            else:
                logger.error(f'Error placing sell order: {repr(e)}')
                break
            logger.error(f'Error placing sell order: {repr(e)}')
        except Exception as e:
            logger.error(f'Error placing sell order: {repr(e)}')

if __name__ == '__main__':
    try:
        if not TESTNET:
            sell_response = place_sell_order(symbol=SYMBOL, qty=QUANTITY)
            logger.info(f'Order response: {sell_response}')
        else:
            response = client.order_market_buy(
                symbol='DOGEUSDT',
                quantity=19960
            )
            pprint(f'response: {response}')
    except Exception as e:
        logger.error(repr(e))
