from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    try:
        bot_username = (await client.get_me()).username
    except:
        bot_username = "this_bot"

    btn = [
        [InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("🔥 Trending", callback_data="trending"),
         InlineKeyboardButton("⚡ Upgrade", callback_data="upgrade")],
        [InlineKeyboardButton("💸 Start Earning", callback_data="earning")]
    ]

    await message.reply_text(
        f"👋 Hello **{message.from_user.first_name}**, good to see you!\n\n"
        "I'm a fast and fully customizable auto-filter bot 🤖 with advanced features.\n"
        "➕ Add me to your group and start earning unlimited money! 💸",
        reply_markup=InlineKeyboardMarkup(btn)
    )
