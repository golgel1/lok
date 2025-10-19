import telebot
import os
import uuid
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

BOT_TOKEN = os.getenv("8298765213:AAGEYdfSYhyvPWtJusFw1J_aMeSTb4-cQI4")
bot = telebot.TeleBot(BOT_TOKEN)

os.makedirs("downloads", exist_ok=True)

def add_bouncing_text(input_path, output_path, text="@LOKALANN"):
    clip = VideoFileClip(input_path)
    fontsize = max(clip.h // 12, 40)
    txt = TextClip(text, fontsize=fontsize, color='white',
                   stroke_color='black', stroke_width=2,
                   font='Arial-Bold', method='caption')
    txt = txt.set_duration(clip.duration - 3)

    def move(t):
        t += 3
        x = (clip.w/2) + (clip.w/3) * (0.7 * (t % 2 - 1))
        y = (clip.h/2) + (clip.h/3) * (0.7 * (1 - (t % 2)))
        return (int(x), int(y))

    txt = txt.set_position(move).set_start(3)
    final = CompositeVideoClip([clip, txt])
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=2)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    chat_id = message.chat.id
    bot.reply_to(message, "🎥 Proses video... teks muncul detik ke-3 dan muter-muter 🔄")

    try:
        file_info = bot.get_file(message.video.file_id)
        downloaded = bot.download_file(file_info.file_path)
        uid = uuid.uuid4().hex[:6]
        inp = f"downloads/in_{uid}.mp4"
        out = f"downloads/out_{uid}.mp4"

        with open(inp, "wb") as f:
            f.write(downloaded)

        add_bouncing_text(inp, out, "@LOKALANN")

        with open(out, "rb") as v:
            bot.send_video(chat_id, v, caption="✅ Selesai!")

    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Error: {e}")
    finally:
        for p in (inp, out):
            if os.path.exists(p): os.remove(p)

bot.infinity_polling()
