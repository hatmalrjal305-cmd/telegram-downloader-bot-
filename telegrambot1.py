import os
import uuid
import yt_dlp
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8011738076:AAE2tONAiRCRXDknLwepK7qq8f5Lfiiq84E"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ارسل رابط الفيديو وسأقوم بتحميله.")


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    # حل روابط تيك توك المختصرة
    if "vt.tiktok.com" in url:
        try:
            r = requests.get(url, allow_redirects=True, timeout=10)
            url = r.url
        except:
            pass

    unique_id = str(uuid.uuid4())

    ydl_opts = {
        "format": "best",
        "outtmpl": f"{unique_id}.%(ext)s",
        "noplaylist": True,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if os.path.exists(filename):

            with open(filename, "rb") as video_file:
                await update.message.reply_video(video=video_file)

            os.remove(filename)

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("فشل تحميل الفيديو ❌")


def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()