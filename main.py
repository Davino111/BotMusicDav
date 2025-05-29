from pyrogram import Client , filters
import yt_dlp

api_id = 21043223
api_hash = "2ba87ea69f719d7ca08b93d06d2aace9"
api_token = "7830632057:AAFV33mXvKbmw78KKnzpri9A1UWng_J4m88"

app = Client("music_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("play") & filters.private)
async def play_song(client, message):
    if len(message.command) < 2:
        await message.reply("Kirimkan perintah seperti: /play judul lagu")
        return

    query = message.text.split(" ", 1)[1]
    url = f"ytsearch:{query}"

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "outtmpl": "song.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info["title"]

    await message.reply_audio("song.mp3", title=title)

app.run()