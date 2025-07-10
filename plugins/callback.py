from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils import get_file_results
from settings import get_user_settings

@Client.on_callback_query(filters.regex(r"^file_\d+"))
async def send_file(client, query: CallbackQuery):
    user_id = query.from_user.id
    index = int(query.data.split("_")[1])
    settings = get_user_settings(user_id)
    results = await get_file_results(query.message.text.replace("🔍 Results for: **", "").replace("**", ""))

    if index >= len(results):
        return await query.answer("Invalid file index.", show_alert=True)

    file = results[index]
    caption = settings["caption"] or f"🏷 {file['file_name']}\n📢 Requested by: {query.from_user.mention}"

    await client.send_document(
        chat_id=query.message.chat.id,
        document=file["file_id"],
        caption=caption
    )

    await query.answer("✅ File Sent!", show_alert=False)


@Client.on_callback_query(filters.regex("^(quality|language|season)$"))
async def handle_options(client, query: CallbackQuery):
    option = query.data
    text = f"🔽 Choose {option.capitalize()}:"
    values = {
        "quality": ["240p", "360p", "480p", "720p", "1080p", "BluRay", "HDRip", "WebDL", "PreDVD"],
        "language": ["Hindi", "English", "Tamil", "Telugu", "Bengali", "Dual Audio"],
        "season": [f"Season {i}" for i in range(1, 16)]
    }

    buttons = [[InlineKeyboardButton(v, callback_data=f"{option}_{v}")] for v in values[option]]
    buttons.append([InlineKeyboardButton("<< Back", callback_data="back_to_result")])

    await query.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex("^back_to_result$"))
async def back_to_results(client, query: CallbackQuery):
    await query.message.edit("🔍 Back to previous results.")


@Client.on_callback_query(filters.regex("^(quality|language|season)_"))
async def filter_by_option(client, query: CallbackQuery):
    category, value = query.data.split("_", 1)
    await query.answer(f"Selected {category.capitalize()}: {value}", show_alert=True)
