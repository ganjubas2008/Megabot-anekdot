import telebot
import config
from telebot import types
import parsing
import random
from jokeclass import Joke

import db

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def welcome(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton("расскажи хороший анекдот")
    b2 = types.KeyboardButton("расскажи обычный анекдот")
    
    markup.add(b1, b2)
    
    bot.send_message(message.chat.id, "здравствуйте", reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def response(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    
    if (message.text == "расскажи хороший анекдот"):
        text = "kek"#utils.get_good(random.randint(1, 30))
        item1 = types.InlineKeyboardButton("👍", callback_data='like')
        item2 = types.InlineKeyboardButton("👎", callback_data='dislike')
        markup.add(item1, item2)
        
        bot.send_message(message.chat.id, text, reply_markup=markup)
        
    elif (message.text == "расскажи обычный анекдот"):
        joke = parsing.get_any(random.randint(1, 1100))
        item1 = types.InlineKeyboardButton("👍", callback_data=f'like{joke.id}')
        item2 = types.InlineKeyboardButton("👎", callback_data=f'dislike{joke.id}')
        markup.add(item1, item2)
        bot.send_message(message.chat.id, str(joke), reply_markup=markup)
        
    else:
        bot.send_message(message.chat.id, "неправильная команда")
        
        
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            id = 0
            delta = (0, 0)
            if call.data[:4] == 'like':
                id = int(call.data[4:])
                delta = (1, 0)
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
                
            elif call.data[:7] == 'dislike':
                bot.send_message(call.message.chat.id, 'Бывает 😢')
                id = int(call.data[7:])
                delta = (0, 1)
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                    text="не нравится - уходи")
                
 
            # Remove inline buttons and update likes counter
            db.update(id=id, delta=delta)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(db.get(id)),
                    reply_markup=None)
 
            
 
    except Exception as e:
        print(repr(e))
    

bot.polling(none_stop=True)
