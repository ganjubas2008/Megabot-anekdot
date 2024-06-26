import telebot
import config
from telebot import types
import parsing
import random
from jokeclass import Joke

import db
import os

bot = telebot.TeleBot(config.token)

if not os.path.exists("data"):
    os.mkdir("data")


@bot.message_handler(commands=["start"])
def welcome(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton("расскажи хороший анекдот")
    b2 = types.KeyboardButton("расскажи обычный анекдот")
    b3 = types.KeyboardButton("расскажи анекдот, у которого много 👍")
    b4 = types.KeyboardButton("расскажи анекдот, у которого много 👎")

    markup.add(b1, b2, b3, b4)

    bot.send_message(message.chat.id, "здравствуйте", reply_markup=markup)
    
@bot.message_handler(commands=["help"])
def welcome(message):

    bot.send_message(message.chat.id, """Мегабот - анекдот.
Для получения анекдота выберите опцию из отображённых на кнопках.
Если пропадут кнопки, можно снова написать боту /start .""")


@bot.message_handler(content_types=["text"])
def response(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    if message.text not in [
        "расскажи хороший анекдот",
        "расскажи обычный анекдот",
        "расскажи анекдот, у которого много 👍",
        "расскажи анекдот, у которого много 👎",
    ]:
        bot.send_message(message.chat.id, "неправильная команда")
        return

    joke = Joke()
    if message.text == "расскажи хороший анекдот":
        joke = parsing.get_good(random.randint(1, 30))

    elif message.text == "расскажи обычный анекдот":
        joke = parsing.get_any(random.randint(1, 1100))

    elif message.text == "расскажи анекдот, у которого много 👍":
        joke = db.get_best()

    elif message.text == "расскажи анекдот, у которого много 👎":
        joke = db.get_worst()

    item1 = types.InlineKeyboardButton("👍", callback_data=f"like{joke.id}")
    item2 = types.InlineKeyboardButton("👎", callback_data=f"dislike{joke.id}")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, str(joke), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            id = 0
            delta = (0, 0)
            if call.data[:4] == "like":
                id = int(call.data[4:])
                delta = (1, 0)
                bot.send_message(call.message.chat.id, "Вот и отличненько 😊")

            elif call.data[:7] == "dislike":
                bot.send_message(call.message.chat.id, "Бывает 😢")
                id = int(call.data[7:])
                delta = (0, 1)

            # Remove inline buttons and update likes counter
            db.update(id=id, delta=delta)
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=str(db.get(id)),
                reply_markup=None,
            )

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
