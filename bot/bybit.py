import time
from pprint import pprint
from typing import Dict, Any

from loguru import logger
from pybit.unified_trading import HTTP

from constants import *

if not DEMO:
    http_client = HTTP(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET)
else:
    http_client = HTTP(
        api_key=BYBIT_DEMO_API_KEY,
        api_secret=BYBIT_DEMO_API_SECRET,
        demo=DEMO
    )


def is_tradeable(symbol: str) -> bool:
    """
    Check if the token is listed and tradeable on Bybit.
    """
    try:
        inst_info = http_client.get_instruments_info(
            category='spot', symbol=symbol
        )
        # pprint(inst_info)
        result = inst_info.get('result', {})
        result_list = result.get('list', [])
        for item in result_list:
            status = item.get('status')
            if symbol == item.get('symbol') and status == 'Trading':
                logger.info(f'status: {status}')
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
            response = http_client.place_order(
                category='spot',
                symbol=symbol,
                side='Sell',
                order_type='Market',
                qty=qty,
                time_in_force='GoodTillCancelled'
            )
            logger.info(f'Sell order placed: {response}')
            return response
        except Exception as e:
            e_str = str(e).lower()
            if (
                'Insufficient balance' in e_str or 'limit exceeded' in e_str
            ):
                qty = qty - (qty * 0.02)
                if qty <= 0:
                    logger.error(
                        'Adjusted quantity is too low to place an order.'
                    )
                    break
            logger.error(f'Error placing sell order: {repr(e)}')


if __name__ == '__main__':
    try:
        if not DEMO:
            sell_response = (
                place_sell_order(symbol=SYMBOL, qty=QUANTITY)
            )
            logger.info(f'Order response: {sell_response}')
        else:
            # logger.info(http_client.request_demo_trading_funds())
            response = http_client.place_order(
                category='spot',
                symbol='DOGEUSDT',
                side='Sell',
                order_type='Market',
                qty=19960000,
                time_in_force='GoodTillCancelled'
            )
            pprint(f'response: {response}')
    except Exception as e:
        logger.error(repr(e))
