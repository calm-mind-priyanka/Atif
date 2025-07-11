from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from settings import get_group_settings, update_group_settings
from pyrogram.errors import UserNotParticipant

# /settings command in group
@Client.on_message(filters.command("settings") & filters.group)
async def settings_command_group(client, message: Message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in ["administrator", "creator"]:
        return await message.reply("🚫 Only group admins can access settings.")
    await settings_menu(client, message, message.chat.title, message.chat.id)

# Settings menu layout
async def settings_menu(client, message_or_query, group_title, group_id):
    text = f"""👑 GROUP - {group_title}  
🆔 ID - {group_id}  

SELECT ONE OF THE SETTINGS THAT YOU WANT TO CHANGE ACCORDING TO YOUR GROUP…"""
    btn = [
        [InlineKeyboardButton("👥 FORCE CHANNEL", callback_data=f"force_channel:{group_id}"),
         InlineKeyboardButton("ℹ️ MAX RESULTS", callback_data=f"max_results:{group_id}")],
        [InlineKeyboardButton("🈵 IMDB", callback_data=f"imdb:{group_id}"),
         InlineKeyboardButton("🔍 SPELL CHECK", callback_data=f"spell_check:{group_id}")],
        [InlineKeyboardButton("🗑️ AUTO DELETE", callback_data=f"auto_delete:{group_id}"),
         InlineKeyboardButton("📚 RESULT MODE", callback_data=f"result_mode:{group_id}")],
        [InlineKeyboardButton("🗂 FILES MODE", callback_data=f"file_mode:{group_id}"),
         InlineKeyboardButton("📝 FILE CAPTION", callback_data=f"caption:{group_id}")],
        [InlineKeyboardButton("🥁 TUTORIAL LINK", callback_data=f"tutorial_link:{group_id}"),
         InlineKeyboardButton("🖇 SET SHORTLINK", callback_data=f"set_shortlink:{group_id}")],
        [InlineKeyboardButton("✅ FILE SECURE", callback_data=f"file_secure:{group_id}")],
        [InlineKeyboardButton("‼️ CLOSE SETTINGS MENU ‼️", callback_data=f"close:{group_id}")]
    ]
    if isinstance(message_or_query, Message):
        await message_or_query.reply(text, reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message_or_query.message.edit(text, reply_markup=InlineKeyboardMarkup(btn))

# Handles all callback settings
@Client.on_callback_query()
async def handle_callbacks(client, query: CallbackQuery):
    data = query.data
    if ":" not in data:
        return await query.answer("❌ Invalid callback")
    action, group_id = data.split(":")
    group_id = int(group_id)

    try:
        member = await client.get_chat_member(group_id, query.from_user.id)
        if member.status not in ["administrator", "creator"]:
            return await query.answer("🚫 Admins only!", show_alert=True)
    except:
        return await query.answer("⚠️ Can't verify admin status!", show_alert=True)

    settings = get_group_settings(group_id)

    def back_btn():
        return InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data=f"back_main:{group_id}")]])

    if action == "back_main":
        return await settings_menu(client, query, query.message.chat.title, group_id)

    if action == "close":
        return await query.message.delete()

    if action == "force_channel":
        txt = "**Manage force subscribe channels.**"
        btn = [
            [InlineKeyboardButton("Set Channel", callback_data=f"set_force:{group_id}"),
             InlineKeyboardButton("Delete Channel", callback_data=f"del_force:{group_id}")],
            [InlineKeyboardButton("<< BACK", callback_data=f"back_main:{group_id}")]
        ]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if action == "set_force":
        settings["awaiting_input"] = {"type": "force"}
        update_group_settings(group_id, settings)
        return await query.message.edit("Send Channel IDs separated by space.\n/cancel", reply_markup=back_btn())

    if action == "del_force":
        settings["force_channels"] = []
        update_group_settings(group_id, settings)
        return await query.message.edit("✅ Channels deleted.", reply_markup=back_btn())

    if action == "max_results":
        settings["awaiting_input"] = {"type": "max"}
        update_group_settings(group_id, settings)
        return await query.message.edit("Send max results number.\n/cancel", reply_markup=back_btn())

    if action == "imdb":
        settings["imdb"] = not settings.get("imdb", False)
        update_group_settings(group_id, settings)
        txt = f"**IMDB Poster - {'ON ✅' if settings['imdb'] else 'OFF ❌'}**"
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Toggle", callback_data=f"imdb:{group_id}")],
            [InlineKeyboardButton("<< BACK", callback_data=f"back_main:{group_id}")]
        ]))

    if action == "spell_check":
        settings["spell_check"] = not settings.get("spell_check", True)
        update_group_settings(group_id, settings)
        txt = f"**Spell Check - {'ON ✅' if settings['spell_check'] else 'OFF ❌'}**"
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Toggle", callback_data=f"spell_check:{group_id}")],
            [InlineKeyboardButton("<< BACK", callback_data=f"back_main:{group_id}")]
        ]))

    if action == "auto_delete":
        settings["auto_delete"] = not settings.get("auto_delete", False)
        update_group_settings(group_id, settings)
        txt = f"**Auto Delete - {'ON ✅' if settings['auto_delete'] else 'OFF ❌'}**\nDelete Time: {settings.get('delete_time', '2m')}"
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Set Time", callback_data=f"set_delete_time:{group_id}")],
            [InlineKeyboardButton("<< BACK", callback_data=f"back_main:{group_id}")]
        ]))

    if action == "set_delete_time":
        settings["awaiting_input"] = {"type": "delete_time"}
        update_group_settings(group_id, settings)
        return await query.message.edit("Send time like `15m` or `2h`\n/cancel", reply_markup=back_btn())

    # You can continue adding more options for caption, file_mode, etc.

# Cancel any input state
@Client.on_message(filters.command(["cancel"]) & filters.group)
async def cancel_input(client, message: Message):
    group_id = message.chat.id
    settings = get_group_settings(group_id)
    settings["awaiting_input"] = None
    update_group_settings(group_id, settings)
    await message.reply("❌ Cancelled process", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data=f"back_main:{group_id}")]]))

# Handle input from user after setting state
@Client.on_message(filters.text & filters.group)
async def group_text_input(client, message: Message):
    group_id = message.chat.id
    user = await client.get_chat_member(group_id, message.from_user.id)
    if user.status not in ["administrator", "creator"]:
        return
    settings = get_group_settings(group_id)
    state = settings.get("awaiting_input")
    if not state:
        return

    text = message.text.strip()
    if state["type"] == "force":
        settings["force_channels"] = text.split()
        await message.reply("✅ CHANNELS SAVED")
    elif state["type"] == "max" and text.isdigit():
        settings["max_results"] = int(text)
        await message.reply("✅ MAX RESULTS SAVED")
    elif state["type"] == "delete_time":
        settings["delete_time"] = text
        await message.reply("✅ DELETE TIME SAVED")

    # Reset awaiting_input
    settings["awaiting_input"] = None
    update_group_settings(group_id, settings)
