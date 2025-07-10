from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils import get_file_results
from settings import get_user_settings
import asyncio

@Client.on_callback_query(filters.regex(r"^file_\d+"))
async def send_file(client, query: CallbackQuery):
    user_id = query.from_user.id
    index = int(query.data.split("_")[1])
    settings = get_user_settings(user_id)
    results = await get_file_results(query.message.text.replace("🔍 Results for: **", "").replace("**", ""))

    if index >= len(results):
        return await query.answer("Invalid file index.", show_alert=True)

    file = results[index]

    # ✅ Support for custom caption with placeholders
    custom_caption = settings.get("caption")
    if custom_caption:
        try:
            caption = custom_caption.format(
                file_name=file["file_name"],
                mention=query.from_user.mention,
                user_id=query.from_user.id
            )
        except Exception:
            caption = f"🏷 {file['file_name']}\n📢 Requested by: {query.from_user.mention}"
    else:
        caption = f"🏷 {file['file_name']}\n📢 Requested by: {query.from_user.mention}"

    file_mode = settings.get("file_mode", {}).get("type", "verify")

    if file_mode == "verify":
        await query.answer("⏳ Verifying… Please wait", show_alert=True)
        verify_time = int(settings.get("file_mode", {}).get("verify_time", 3))
        await asyncio.sleep(verify_time)
        await client.send_document(
            chat_id=query.message.chat.id,
            document=file["file_id"],
            caption=caption
        )

    elif file_mode == "shortlink":
        short_url = settings.get("shortlinks", {}).get("1") or "https://short.link/example"
        await query.message.reply(f"🔗 Get your file via: {short_url}")
        return await query.answer("🔗 Shortlink sent", show_alert=True)

    else:
        await client.send_document(
            chat_id=query.message.chat.id,
            document=file["file_id"],
            caption=caption
        )

    # ✅ Tutorial links (if any)
    tutorial_links = settings.get("tutorial_links", {})
    msgs = []

    if tutorial_links.get("first"):
        msgs.append(f"▶️ Tutorial 1: {tutorial_links['first']}")
    if tutorial_links.get("second"):
        msgs.append(f"▶️ Tutorial 2: {tutorial_links['second']}")

    if msgs:
        await query.message.reply("\n".join(msgs))

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
