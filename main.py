import asyncio

from bot import start_bot
from config import get_token, get_wallet_key
from database import create_tables

if __name__ == "__main__":
    create_tables()
    token = get_token()
    wallet_key = get_wallet_key()
    asyncio.run(start_bot(token))
