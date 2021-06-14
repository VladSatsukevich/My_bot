from datetime import date
import telebot
import my_token
import json
from telebot import types

day = ''
month = ''
time_set = ''


bot = telebot.TeleBot(my_token.token)

@bot.message_handler(commands=['start'])
def first_step(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton('Типо того'), types.KeyboardButton('Не уверен(а)'))
    msg = bot.send_message(message.chat.id,"Ну привет " + message.from_user.first_name+" "+ message.from_user.last_name + ", опять ногти?", reply_markup=markup)
    bot.register_next_step_handler(msg, user_answer)
@bot.message_handler(func=lambda m: True)

def user_answer(message):
    if message.text == 'Типо того':
        bot.send_message(message.chat.id, 'В какой день вам удобно будет прийти?\nВпишите от 1 до 31')
        bot.register_next_step_handler(message, second_step)
    elif message.text == 'Не уверен(а)':
        bot.send_message(message.chat.id, 'ясно)) ' + message.from_user.first_name)
    types.ReplyKeyboardRemove(selective=False)

def second_step(message):
    global day
    day = message.text
    bot.send_message(message.from_user.id, "Какой месяц предпочитаете?")
    bot.register_next_step_handler(message, third_step)

def third_step(message):
    global month
    month = message.text
    bot.send_message(message.from_user.id, "Укажите удобное для вас время\nВ формате: **:**")
    bot.register_next_step_handler(message, forth_step)

def forth_step(message):
    global time_set
    time_set = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Хочешь записаться на ' + str(time_set) + '?\nИ именно в этот день: ' + str(day) + ' ' + str(month) + '?'
    bot.send_message(message.from_user.id, text = question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Отлично, мы вас записали!")
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Попробуйте еще раз!\n")
        bot.register_next_step_handler(call.message, second_step)

bot.polling()

