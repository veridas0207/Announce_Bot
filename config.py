import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID_RAW = os.getenv("GUILD_ID")
if not GUILD_ID_RAW:
    raise ValueError("GUILD_ID is not set in the .env file.")
try:
    GUILD_ID = int(GUILD_ID_RAW)
except ValueError:
    raise ValueError("GUILD_ID must be a valid integer.")

ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME", "Admin").lower() # The name of the role that can use the /announce command (case-insensitive)

ALLOWED_ANNOUNCE_CHANNELS_RAW = os.getenv("ALLOWED_ANNOUNCE_CHANNELS", "")
ALLOWED_ANNOUNCE_CHANNELS_IDS = [int(x.strip()) for x in ALLOWED_ANNOUNCE_CHANNELS_RAW.split(',') if x.strip().isdigit()]