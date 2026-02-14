from telegram import Update
from telegram.ext import ContextTypes

from storage.buffers import user_message_buffer, user_done_messages, user_last_post_link


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    user_message_buffer[user_id] = []

    for (chat_id, msg_id) in user_done_messages.get(user_id, []):
        try:
            await context.bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="Cancelled.")
        except Exception:
            pass

    user_done_messages[user_id] = []
    user_last_post_link.pop(user_id, None)

    await update.message.reply_text("Cancelled and cleared buffered messages.")
