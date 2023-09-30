import asyncio

from bot import start_bot
from config import get_token, get_wallet_key

if __name__ == "__main__":
    token = get_token()
    wallet_key = get_wallet_key()
    asyncio.run(start_bot(token))
