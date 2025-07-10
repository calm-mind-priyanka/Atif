from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from utils import get_file_results, fetch_imdb_details
from settings import get_user_settings
import asyncio

async def is_user_subscribed(client, user_id, channels):
    for channel in channels:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            return False, channel
        except ChatAdminRequired:
            continue
    return True, None

def parse_time(t):
    t = t.lower()
    if t.endswith("s"):
        return int(t[:-1])
    elif t.endswith("m"):
        return int(t[:-1]) * 60
    elif t.endswith("h"):
        return int(t[:-1]) * 3600
    return 0

@Client.on_message(filters.text & filters.group & ~filters.edited)
async def search_files(client, message: Message):
    query = message.text
    user_id = message.from_user.id
    settings = get_user_settings(user_id)

    # Force join check
    force_channels = settings.get("force_channels", [])
    if force_channels:
        is_sub, channel = await is_user_subscribed(client, user_id, force_channels)
        if not is_sub:
            return await message.reply(
                "🚫 You must join our channel to use this bot.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{channel}")]]
                )
            )

    # IMDB info if enabled
    if settings.get("imdb", False):
        imdb = fetch_imdb_details(query)
        if imdb:
            caption = (
                f"🎬 **{imdb['title']}** ({imdb['year']})\n"
                f"⭐ IMDB: {imdb['rating']}\n"
                f"🎭 Genre: {imdb['genre']}\n"
                f"📖 {imdb['plot']}"
            )
            await message.reply_photo(photo=imdb['poster'], caption=caption)

    # Search file results
    results = await get_file_results(query)
    if not results:
        return await message.reply("❌ No results found.")

    buttons = []
    for index, file in enumerate(results[:settings.get("max_results", 5)]):
        buttons.append([
            InlineKeyboardButton(f"{file['file_name']}", callback_data=f"file_{index}")
        ])

    extra_buttons = [
        [InlineKeyboardButton("🔁 Quality", callback_data="quality"),
         InlineKeyboardButton("🎞 Language", callback_data="language"),
         InlineKeyboardButton("📺 Season", callback_data="season")]
    ]

    result_msg = await message.reply_text(
        f"🔍 Results for: **{query}**",
        reply_markup=InlineKeyboardMarkup(buttons + extra_buttons)
    )

    # ✅ AUTO DELETE if enabled
    if settings.get("auto_delete"):
        delay = parse_time(settings.get("delete_time", "2m"))
        await asyncio.sleep(delay)
        try:
            await result_msg.delete()
        except:
            pass
