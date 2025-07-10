from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from plugins import all_plugins  # Ensure plugins/__init__.py imports all needed handlers

app = Client("autofilterbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
