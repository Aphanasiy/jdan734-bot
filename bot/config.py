import asyncio
import json
import logging
from datetime import datetime
from os import environ

import aiosqlite
import coloredlogs
from aiogram import Bot, Dispatcher

from .lib.filters import NoRunningJobFilter

try:
    with open("config.json") as file:
        config = json.loads(file.read())
except FileNotFoundError:
    config = {}

RSS_FEEDS = [
    # Katz channel
    {
        "chatid": -1001176998310,
        "channelid": "UCUGfDbfRIx51kJGGHIFo8Rw",
        "url": "https://www.youtube.com/feeds/videos.xml?channel_id="
               "UCUGfDbfRIx51kJGGHIFo8Rw"
    },

    {
        "chatid": -1001335444502,
        "channelid": "UCBNlINWfd08qgDkUTaUY4_w",
        "url": "https://www.youtube.com/feeds/videos.xml?channel_id="
               "UCBNlINWfd08qgDkUTaUY4_w"
    }
]

DELAY = 30
DATABASE_PATH = "jdandb.db"
IMAGE_PATH = "bot/cache/{image}.jpg"
START_TIME = datetime.now()

ENABLE_RSS = environ.get("RSS") or config.get("rss") or False
TOKEN = environ.get("TOKEN") or config.get("token")
STATUS = environ.get("STATUS") or config.get("status") or "unknown"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install(fmt="%(asctime)s %(levelname)s %(message)s",
                    level="INFO",
                    logger=logger)

logging.getLogger("schedule").addFilter(NoRunningJobFilter())

async def connect_db():
    return await aiosqlite.connect(DATABASE_PATH)


conn = asyncio.run(connect_db())

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
