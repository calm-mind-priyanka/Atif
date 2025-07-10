from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils import get_file_results
from settings import get_user_settings

@Client.on_message(filters.text & filters.group & ~filters.edited)
async def search_files(client, message: Message):
    query = message.text
    user_id = message.from_user.id
    settings = get_user_settings(user_id)
    results = await get_file_results(query)

    if not results:
        return await message.reply("❌ No results found.")

    buttons = []
    for index, file in enumerate(results[:settings["max_results"]]):
        buttons.append([
            InlineKeyboardButton(f"{file['file_name']}", callback_data=f"file_{index}")
        ])

    extra_buttons = [
        [InlineKeyboardButton("🔁 Quality", callback_data="quality"),
         InlineKeyboardButton("🎞 Language", callback_data="language"),
         InlineKeyboardButton("📺 Season", callback_data="season")]
    ]

    await message.reply_text(
        f"🔍 Results for: **{query}**",
        reply_markup=InlineKeyboardMarkup(buttons + extra_buttons)
    )
