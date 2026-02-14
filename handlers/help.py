from telegram import Update
from telegram.ext import ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "How to create hyperlinks:\n"
        "- Use the quoted format: \"text\"(link) or 'text'(link).\n"
        "  Examples: \"visit\"(google.com) or 'visit'(https://example.com)\n"
        "- Links may omit the scheme; the bot will add https:// if missing.\n"
        "- For multi-message posts: send multiple messages, then press the inline 'Done' button.\n"
        "- For images: put the page title on the first non-empty line of the caption.\n"
        "- Only quoted hyperlink form is supported."
    )
    await update.message.reply_text(help_text)
