import telebot
import os
from flask import Flask
from threading import Thread

# Initialize the bot with your token
TOKEN = '8770037807:AAHev676tFnj9pJwZXy7ZzBLg9ietNOJZ4M' # O'zingizning tokeringizni shu yerga yozing
bot = telebot.TeleBot(TOKEN)

# Render uchun kichik veb-server yaratamiz
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot muvaffaqiyatli ishlamoqda!"

def run_web():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "Videoni qabul qildim, yuklab olyapman...")
    
    # Download the video
    video_file = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(video_file.file_path)

    # Save the video to a temporary file
    video_path = 'temp_video.mp4'
    with open(video_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # TODO: Add subtitle translation logic here
    bot.reply_to(message, "Video saqlandi! Subtitr ustida ishlayapman...")
    
    # After translation, send the subtitles back to the user
    # bot.send_message(message.chat.id, translated_subtitles)

if __name__ == '__main__':
    # Flask serverni alohida fonda (thread) ishga tushiramiz
    t = Thread(target=run_web)
    t.start()
    
    # Botni ishga tushiramiz
    print("Bot ishga tushdi...")
    bot.polling(non_stop=True)
    
