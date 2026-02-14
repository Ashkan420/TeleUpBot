import os
import uuid

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import IMGBB_API_KEY
from storage.buffers import user_message_buffer, user_done_messages
from services.imgbb_service import upload_image_to_imgbb


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        caption = update.message.caption if update.message.caption else ""

        file = await photo.get_file()

        file_ext = os.path.splitext(file.file_path)[1] if file.file_path else ".jpg"
        file_path = f"temp_{uuid.uuid4().hex}{file_ext}"

        await file.download_to_drive(file_path)

        try:
            image_url = upload_image_to_imgbb(file_path, IMGBB_API_KEY)
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

        user_id = update.effective_user.id
        user_message_buffer.setdefault(user_id, []).append(
            {"type": "image", "url": image_url, "caption": caption}
        )

        keyboard = [[InlineKeyboardButton("Done", callback_data="done")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        msg = await update.message.reply_text(
            "Image added to buffer. Press 'Done' when finished.",
            reply_markup=reply_markup
        )

        user_done_messages.setdefault(user_id, []).append((msg.chat_id, msg.message_id))

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
