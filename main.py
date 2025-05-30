import os
from pyrogram import Client, filters
from pymongo import MongoClient
import yt_dlp
from dotenv import load_dotenv

# Load env
load_dotenv()

# Inisialisasi variabel
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# Koneksi ke MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["music_bot"]
log_collection = db["logs"]

# Inisialisasi bot
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply("Halo! Kirimkan /play <judul lagu> untuk mendownload lagu dari YouTube!")

@app.on_message(filters.command("play") & filters.private)
async def play_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Kirim: /play <judul lagu>")

    query = message.text.split(" ", 1)[1]
    search_url = f"ytsearch:{query}"

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "outtmpl": "song.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True
    }

    await message.reply(f"🔍 Mencari dan mendownload lagu `{query}`...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_url, download=True)
            title = info["title"]

        await message.reply_audio("song.mp3", title=title)
        log_collection.insert_one({"user_id": message.from_user.id, "query": query, "title": title})

    except Exception as e:
        await message.reply("⚠️ Terjadi kesalahan saat mendownload lagu.")
        print(e)

app.run()
