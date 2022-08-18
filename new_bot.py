import random
import types
import telebot
from telebot import types

token = '5519767065:AAEBesboVCaAwBApEvsa-5k_zReTu_nePQM'
bot = telebot.TeleBot(token)

bank = 100
flag = 1 

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Игра против человека')
    button2 = types.KeyboardButton('Игра против компьютера')
    markup.add(button1, button2)
    bot.send_message(message.chat.id,"Привет ✌️. \n"
                                     "Я игра в которой тебе нужно будет собирать конфетки!\n"
                                     "Выбери режим игры который тебе больше нравится".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def game(message):
    if (message.text == 'Игра против человека'):
        bot.send_message(message.chat.id,"Игра против человека.\n"
                                         "Каждый игрок по очереди берет конфеты со стола.\n"
                                         f"Всего конфет {bank}.\n"
                                         "За один раз можно взять не более 10 конфет.\n"
                                         "Кто сделает последний ход, победил.\n"
                                         "Да победит сильнейший!")
        pvp(message)
    
    if (message.text == 'Игра против компьютера'):
        bot.send_message(message.chat.id,"Игра против компьютера.\n"
                                         "Игрок и компьютер по очереди берут конфеты со стола.\n"
                                         f"Всего конфет {bank}.\n"
                                         "За один раз можно взять не более 10 конфет.\n"
                                         "Кто сделает последний ход, победил."
                                         "Посмотрим как человек справися с компьютером!")
        pvc(message)

@bot.message_handler(content_types=['text'])
def pvp(message):
    global bank
        
    if bank > 0:
        bot.send_message(message.chat.id,"Введите колличество конфет, которое хотите забрать")
        bot.register_next_step_handler(message, diff)
           
    else:
        bot.send_message(message.chat.id,"Игра окончена!\n"
                                         "Игрок сделавший последний ход, выйграл.\n"  
                                         "Поздравляю!!!!")

def pvc(message):
    global bank
    global flag   
    if bank > 0:
        if flag == 1:
            bot.send_message(message.chat.id,"Ход игрока.\n"
                                             "Введите колличество конфет, которое хотите забрать")
            bot.register_next_step_handler(message, diff2)
        else:
            bot.send_message(message.chat.id,"Ход компьютера.")
            comp(message)
           
    else:
        bot.send_message(message.chat.id,"Игра окончена!")
        if flag == 1: bot.send_message(message.chat.id,"Победа игрока")
        else: bot.send_message(message.chat.id,"Победа компьютера")
           
def diff(message):
    global bank
    stap = int(message.text)
    if stap > 10:
        bot.send_message(message.chat.id,f"Разрешается взять не более 10 конфет")
        pvp(message)
    else:
        bank = bank - stap
        bot.send_message(message.chat.id,f"Осталось {bank} конфет.\n"
                                          "Передай телефон другому игроку.")
        pvp(message)
    return bank

def diff2(message):
    global bank
    global flag
    stap = int(message.text) 
    if stap > 10:
        bot.send_message(message.chat.id,f"Разрешается взять не более 10 конфет")
        pvc(message)
    else:
        bank = bank - stap
        bot.send_message(message.chat.id,f"Осталось {bank} конфет.\n"
                                          "Далее ход компьютера.")
        flag = 2
        pvc(message)
    return bank

def comp(message):
    global bank
    global flag
    number = int(random.randint(1, 10))
    bank -= number
    bot.send_message(message.chat.id, "Компьютер сделал свой ход.\n"
                                      f"Он взял {number} конфет.\n"
                                      f"Осталось {bank} конфет.")
    flag = 1                                  
    pvc(message)
    return bank


bot.polling(none_stop=True)