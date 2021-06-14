import telebot
import my_token
import json
from telebot import types



bot = telebot.TeleBot(my_token.token)



@bot.message_handler(commands=['start'])
def first_step(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton('Типо того'), types.KeyboardButton('Не уверен(а)'))
    msg = bot.send_message(message.chat.id,"Ну привет " + message.from_user.first_name+" "+ message.from_user.last_name + ", опять ногти?", reply_markup=markup)
    bot.register_next_step_handler(msg, user_answer)
   

def user_answer(message):
    if message.text == 'Типо того':
        bot.send_message(message.chat.id, 'В какой день вам удобно будет прийти?')
        bot.register_next_step_handler(message, second_step)
    elif message.text == 'Не уверен(а)':
        bot.send_message(message.chat.id, 'ясно)) ' + message.from_user.first_name)
    types.ReplyKeyboardRemove(selective=False)

def second_step(message):
    pass
        


bot.polling(none_stop=True)

