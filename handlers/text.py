from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from storage.buffers import user_message_buffer, user_done_messages


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return

    user_id = update.effective_user.id

    user_message_buffer.setdefault(user_id, []).append({"type": "text", "text": text})

    keyboard = [[InlineKeyboardButton("Done", callback_data="done")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    msg = await update.message.reply_text(
        "Message added. Press 'Done' when finished.",
        reply_markup=reply_markup
    )

    user_done_messages.setdefault(user_id, []).append((msg.chat_id, msg.message_id))
