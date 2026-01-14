import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID") # Keep as string for now, convert to int when used
ADMIN_ROLE_NAME = "Admin" # The name of the role that can use the /announce command

ALLOWED_ANNOUNCE_CHANNELS_RAW = os.getenv("ALLOWED_ANNOUNCE_CHANNELS", "")
ALLOWED_ANNOUNCE_CHANNELS_IDS = [int(x.strip()) for x in ALLOWED_ANNOUNCE_CHANNELS_RAW.split(',') if x.strip().isdigit()]