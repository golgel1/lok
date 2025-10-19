import telebot, os, subprocess

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8298765213:AAHZExKWGGrCSJNFzjvPYDT4wkH8gjoewo0"
bot = telebot.TeleBot(BOT_TOKEN)

os.makedirs("downloads", exist_ok=True)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    chat_id = message.chat.id
    bot.reply_to(message, "🎬 Proses video... teks akan muncul detik ke-3 dan bergerak 🔄")

    try:
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        input_path = "downloads/in.mp4"
        output_path = "downloads/out.mp4"

        with open(input_path, "wb") as f:
            f.write(downloaded_file)

        # teks @LOKALANN muncul detik ke-3, gerak melingkar
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-vf",
            "drawtext=fontfile=/system/fonts/Roboto-Regular.ttf:"
            "text='@LOKALANN':"
            "fontsize=30:fontcolor=white:borderw=2:"
            "x=(w/2)+100*sin(2*PI*t/2):y=(h/2)+100*cos(2*PI*t/2):"
            "enable='gte(t,3)'",
            "-codec:a", "copy",
            output_path,
            "-y"
        ]

        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        with open(output_path, "rb") as vid:
            bot.send_video(chat_id, vid, caption="✅ Selesai ditambah teks @LOKALANN!")

        os.remove(input_path)
        os.remove(output_path)

    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Error: {e}")

print("✅ Bot aktif. Tunggu pesan video di Telegram...")
bot.infinity_polling()
