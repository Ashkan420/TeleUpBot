from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Clear any previous buffer and done messages for this user
    from storage.buffers import user_message_buffer, user_done_messages, user_last_post_link
    user_id = update.effective_user.id
    user_message_buffer[user_id] = []
    user_done_messages[user_id] = []
    user_last_post_link.pop(user_id, None)
    await update.message.reply_text(
        "Send me text or an image with caption.\n"
        "I will upload it to telegra.ph and send you the link."
    )
