import os

from dotenv import load_dotenv

load_dotenv(override=True)


BYBIT_API_KEY = os.getenv('BYBIT_API_KEY')
BYBIT_API_SECRET = os.getenv('BYBIT_API_SECRET')

BYBIT_DEMO_API_KEY = os.getenv('BYBIT_DEMO_API_KEY')
BYBIT_DEMO_API_SECRET = os.getenv('BYBIT_DEMO_API_SECRET')

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

BINANCE_TESTNET_API_KEY = os.getenv('BINANCE_TESTNET_API_KEY')
BINANCE_TESTNET_API_SECRET = os.getenv('BINANCE_TESTNET_API_SECRET')

DEMO=False
TESTNET=True

SYMBOL = os.getenv('SYMBOL')
QUANTITY = os.getenv('QUANTITY')

RETRY_DELAY = 1  # seconds between retries
