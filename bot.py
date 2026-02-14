import requests
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from config import BOT_TOKEN
from handlers.start import start
from handlers.help import help_command
from handlers.cancel import cancel_command
from handlers.text import handle_text
from handlers.photo import handle_photo
from handlers.done import done_callback


def set_bot_commands():
    try:
        commands = [
            {"command": "start", "description": "Start bot"},
            {"command": "help", "description": "How to hyperlink"},
            {"command": "cancel", "description": "Cancel and clear buffer"},
        ]

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands",
            json={"commands": commands},
            timeout=5
        )
    except Exception:
        pass


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("cancel", cancel_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.add_handler(CallbackQueryHandler(done_callback, pattern="done"))

    set_bot_commands()

    print("✅ Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
