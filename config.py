import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

BOT_TOKEN = os.getenv("BOT_TOKEN")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

if not BOT_TOKEN:
    raise ValueError(" BOT_TOKEN is missing or .env not loading")

if not IMGBB_API_KEY:
    print(" IMGBB_API_KEY is missing (image uploads will fail)")
