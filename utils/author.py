from telegram import Update


def get_author_info(update: Update):
    user = update.effective_user

    author_name = user.full_name if user else "Unknown User"
    author_url = ""

    if user and user.username:
        author_url = f"https://t.me/{user.username}"

    return author_name, author_url