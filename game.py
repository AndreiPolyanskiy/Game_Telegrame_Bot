from operator import le
import telebot
from telebot import types
import random
import string


token = '5338274010:AAGGCP_tfS_R6zzmN8j7QHMtMNe-1B3Wst4'
bot = telebot.TeleBot(token)

word_bot = ''

def enter_word(message):    
    bot.send_message(message.chat.id,"Введите свой вариант")
    bot.register_next_step_handler(message, comparison) 

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Новая игра!')
    markup.add(button1)
    bot.send_message(message.chat.id,"Привет ✌️. \n"
                                     "Давай ка сыграем в игру <<Быки и коровы>>.\n"
                                     "Правила очень просты:\n"
                                     "- Бот загадывает слово из определенного колличества букв\n"
                                     "- Твоя задача угадать это слово\n"
                                     "- Если в твоем слове присутствует буква, которая есть в загаданном слове - это 1 корова.\n"
                                     "- А если ты угадал еще и позицию - это 1 бык.\n"
                                     "Начнем игру! Удачи!))".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bots(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Сгенерировать слово')
    markup.add(button1)
    bot.send_message(message.chat.id,"Сгенерируйте слово".format(message.from_user), reply_markup=markup)

    if message.text == 'Сгенерировать слово':
        bot.send_message(message.chat.id,"Укажите колличество букв:")
        bot.register_next_step_handler(message, word_generator)


def word_generator(message):
    global word_bot
    len_word = int(message.text)
    
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(len_word))
    
    word_bot = list(rand_string)
    bot.send_message(message.chat.id,"Слово сгенерированно")
    enter_word(message)


@bot.message_handler(content_types=['text'])
def comparison(message):
    global word_bot
    word_user = list(message.text)

    count_bik = 0
    count_korova = 0

    if len(word_user)!=len(word_bot):
        bot.send_message(message.chat.id, f"В этом слове {len(word_bot)} буквы. Введите слово еще раз.")
        enter_word(message)
    else:
        for i in range(len(word_bot)):
            for j in range(len(word_user)):
                if word_bot[i] == word_user[j] and i == j:
                    count_bik +=1
                
                elif word_bot[i] == word_user[j]:
                    count_korova +=1
        if count_bik != len(word_bot):
            bot.send_message(message.chat.id, "Увы, не угадал. \n"
                                             f"<<Быки>> = {count_bik} \n"
                                             f"<<Коровы>> = {count_korova}")
            bot.send_message(message.chat.id, "Попробуйте еще раз")
            enter_word(message)                                 
        else:
            bot.send_message(message.chat.id, "Ура!!! Вы УГАДАЛИ слово!!!")     
                                     
    
bot.polling(none_stop=True)


    