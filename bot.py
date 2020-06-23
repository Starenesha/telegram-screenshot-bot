import telebot
import imgkit
import re
from config import TOKEN
import time

bot = telebot.TeleBot(TOKEN)
task = bot.get_me()
pattern = '((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)'

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hi! Give me site address and I will return you a screenshot of the page.")

@bot.message_handler(regexp='.*?')
def answer_messages(message):
    url = re.match(pattern, message.text).group(0)
    filename = time.time()

    try:
        img = imgkit.from_url(url, f'screens/{filename}.jpg')
        with open(f'screens/{filename}.jpg', 'rb') as file:
            bot.send_photo(message.chat.id, file, caption='Your screenshot:', reply_to_message_id=message.message_id)
    except Exception:
        bot.send_message(message.chat.id, "Something goes wrong, please check your site url")

if __name__ == '__main__':
    bot.polling(none_stop=True)
