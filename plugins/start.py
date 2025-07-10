from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    btn = [
        [InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{client.me.username}?startgroup=true")],
        [InlineKeyboardButton("🔥 Trending", callback_data="trending"),
         InlineKeyboardButton("⚡ Upgrade", callback_data="upgrade")],
        [InlineKeyboardButton("💸 Start Earning", callback_data="earning")]
    ]
    await message.reply_text(
        "ʜᴇʏ Sandy ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ,\n\n"
        "ɪ'ᴍ ᴀ ꜰᴀꜱᴛ & ꜰᴜʟʟ ᴄᴜꜱᴛᴏᴍɪᴢᴀʙʟᴇ ᴀᴜᴛᴏ ꜰɪʟᴛᴇʀ ᴡɪᴛʜ ᴀᴅᴠᴀɴᴄᴇ ꜰᴇᴀᴛᴜʀᴇꜱ. "
        "ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴛᴏ ᴇᴀʀɴ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏɴᴇʏ...💸",
        reply_markup=InlineKeyboardMarkup(btn)
    )
