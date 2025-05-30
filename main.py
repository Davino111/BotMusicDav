import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.exceptions import GroupCallNotFoundError
from yt_dlp import YoutubeDL
from os import system

API_ID = 123456  # Ganti dengan API ID kamu
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytg = PyTgCalls(app)

ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "outtmpl": "song.%(ext)s",
    "quiet": True
}

@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    chat_id = message.chat.id

    if len(message.command) < 2:
        return await message.reply("Kirim: /play <judul lagu>")

    query = message.text.split(" ", 1)[1]
    await message.reply(f"🔍 Mencari `{query}`...")

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
        title = info["title"]
        await message.reply(f"🎶 Memutar: {title}")

    # Join voice chat dan play lagu
    try:
        await pytg.join_group_call(
            chat_id,
            InputAudioStream(
                "song.m4a"
            )
        )
    except GroupCallNotFoundError:
        await message.reply("❌ Voice chat belum dimulai di grup ini!")

@pytg.on_stream_end()
async def on_stream_end(_, update: StreamAudioEnded):
    await pytg.leave_group_call(update.chat_id)

@app.on_message(filters.command("stop") & filters.group)
async def stop(_, message):
    await pytg.leave_group_call(message.chat.id)
    await message.reply("⏹️ Musik dihentikan.")

# Jalankan bot
pytg.start()
app.run()
