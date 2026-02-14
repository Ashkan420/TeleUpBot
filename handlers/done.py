import re
from telegram import Update
from telegram.ext import ContextTypes

from storage.buffers import user_message_buffer, user_done_messages, user_last_post_link
from utils.author import get_author_info
from services.hyperlink_service import convert_hyperlinks
from services.telegraph_service import create_telegraph_page


async def done_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    if user_id not in user_message_buffer or not user_message_buffer[user_id]:
        last = user_last_post_link.get(user_id)
        if last:
            await query.edit_message_text(f"✅ Uploaded!\n\n🔗 {last}")
            return
        await query.edit_message_text("No messages to post.")
        return

    author_name, author_url = get_author_info(update)
    buf = user_message_buffer[user_id]

    # Find first non-empty line across buffered items to use as title
    title_line = None
    title_source_index = None

    for idx, item in enumerate(buf):
        text_source = item.get("text") if item.get("type") == "text" else item.get("caption", "")
        if not text_source:
            continue

        for ln in text_source.splitlines():
            if ln.strip():
                title_line = ln.strip()
                title_source_index = idx
                break

        if title_line:
            break

    title = title_line[:255] if title_line else "Telegram Post"

    html_parts = []

    for idx, item in enumerate(buf):
        skip_title_item = (title_source_index is not None and idx == title_source_index)

        if item.get("type") == "text":
            txt = item.get("text", "")

            if skip_title_item and title_line:
                lines_txt = txt.splitlines()
                i = 0
                while i < len(lines_txt) and not lines_txt[i].strip():
                    i += 1
                if i < len(lines_txt):
                    del lines_txt[i]
                txt = "\n".join(lines_txt)

            conv = convert_hyperlinks(txt)

            if conv.strip():
                html_parts.append(f"<p>{conv.replace(chr(10), '<br>')}</p>")

        elif item.get("type") == "image":
            url = item.get("url")
            caption = item.get("caption", "")

            if skip_title_item and title_line and caption:
                lines_cap = caption.splitlines()
                j = 0
                while j < len(lines_cap) and not lines_cap[j].strip():
                    j += 1
                if j < len(lines_cap):
                    del lines_cap[j]
                caption = "\n".join(lines_cap)

            img_html = f'<img src="{url}"/>'

            if caption and caption.strip():
                cap_conv = convert_hyperlinks(caption)
                img_html += f"<p>{cap_conv.replace(chr(10), '<br>')}</p>"

            html_parts.append(img_html)

    html_to_send = "".join(html_parts)

    if title_line:
        try:
            esc = re.escape(title_line)
            html_to_send = re.sub(rf'<p>\s*{esc}\s*</p>', '', html_to_send)
            html_to_send = re.sub(rf'<p>\s*{esc}\s*(?:<br\s*/?>)+', '<p>', html_to_send)
        except re.error:
            pass

    if not html_to_send.strip():
        html_to_send = "<p> </p>"

    try:
        link = create_telegraph_page(
            title=title,
            author_name=author_name,
            author_url=author_url,
            html_content=html_to_send
        )
    except Exception as e:
        await query.edit_message_text(f"❌ Error creating Telegraph page: {e}")
        return

    for (chat_id, msg_id) in user_done_messages.get(user_id, []):
        try:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=f"✅ Uploaded!\n\n🔗 {link}"
            )
        except Exception:
            pass

    user_last_post_link[user_id] = link
    user_message_buffer[user_id] = []
    user_done_messages[user_id] = []
