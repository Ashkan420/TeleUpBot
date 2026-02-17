from telegram import Update

MY_CHANNEL_URL = "https://t.me/bichniga"

def get_author_info(update: Update):
    user = update.effective_user

    # Use the user's full name or fallback
    author_name = user.full_name if user else "Unknown User"
    #author_url = ""

    #if user and user.username:
        #author_url = f"https://t.me/{user.username}"
    author_url = MY_CHANNEL_URL

    # Usernames that should be replaced
    spoof_users = ["Brotherash210"]

    # If sender is in spoof list, replace with channel identity
    if user and user.username in spoof_users:
        author_name = "ครнкคภ"
        author_url = MY_CHANNEL_URL

    return author_name, author_url