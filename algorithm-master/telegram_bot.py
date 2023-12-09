import telebot
import config
from telebot import *
from write_db import *
from peewee import *

bot = telebot.TeleBot(config.TOKEN)
#photoSed = open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb')
#photoHappy = open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb')

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,f"Добро пожаловать, {message.from_user.first_name}!".format(message.from_user, bot.get_me()),
                     parse_mode='html')
    create_user(message.from_user.id,message.from_user.first_name)
    bot.send_message(message.chat.id, f"Пожалуйста, {message.from_user.first_name}, скажи, из какой ты группы?",
                     parse_mode='html')
    name_group = message.text
    print(message.text)
    bot.register_next_step_handler(message,update_name_group_user,name_group)



@bot.message_handler(content_types=['text'])
def get_name_group_user(message):


    if message.text == 'Меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_Schedule = types.KeyboardButton("Расписание на день недели")
        item_quit_my_friend = types.KeyboardButton("Уйду ли я с другом\подругой?")
        markup.add(item_Schedule, item_quit_my_friend)
        bot.send_message(message.chat.id, "Прекрасно, что желаешь узнать?",
                         parse_mode='html', reply_markup=markup)
    if message.chat.type == 'private':
        if message.text == 'Расписание на день недели':

            murkup_parity = types.ReplyKeyboardMarkup(resize_keyboard=True)
            percent_two_is_true = types.KeyboardButton('Первая')
            percent_two_is_false = types.KeyboardButton('Вторая')
            menu = types.KeyboardButton('Меню')
            murkup_parity.add(percent_two_is_true, percent_two_is_false,menu)
            bot.send_message(message.chat.id,
                             'Пожалуйства выбери неделю (P.S. первая - верхняя'
                             ' неделя в файле excel)', parse_mode='html', reply_markup=murkup_parity)
        elif message.text == 'Первая':
            murkup_day_week_chet = types.InlineKeyboardMarkup(row_width=2)
            mon = types.InlineKeyboardButton("Пн", callback_data='mon_chet')
            tue = types.InlineKeyboardButton("Вт", callback_data='tue_chet')
            wed = types.InlineKeyboardButton("Ср", callback_data='wed_chet')
            thu = types.InlineKeyboardButton("Чт", callback_data='thu_chet')
            fri = types.InlineKeyboardButton("Пт", callback_data='fri_chet')
            sat = types.InlineKeyboardButton("Сб", callback_data='sat_chet')
            murkup_day_week_chet.add(mon, tue, wed, thu, fri, sat)
            bot.send_message(message.chat.id, "Прекрасно, пожалуйста, выбери день недели(●'◡'●)",
                             parse_mode='html', reply_markup=murkup_day_week_chet)
        elif message.text == 'Вторая':
            murkup_day_week_ne_chet = types.InlineKeyboardMarkup(row_width=2)
            mon = types.InlineKeyboardButton("Пн", callback_data='mon_ne_chet')
            tue = types.InlineKeyboardButton("Вт", callback_data='tue_ne_chet')
            wed = types.InlineKeyboardButton("Ср", callback_data='wed_ne_chet')
            thu = types.InlineKeyboardButton("Чт", callback_data='thu_ne_chet')
            fri = types.InlineKeyboardButton("Пт", callback_data='fri_ne_chet')
            sat = types.InlineKeyboardButton("Сб", callback_data='sat_ne_chet')
            murkup_day_week_ne_chet.add(mon, tue, wed, thu, fri, sat)
            bot.send_message(message.chat.id, "Прекрасно, пожалуйста, выбери день недели(●'◡'●)",
                             parse_mode='html', reply_markup=murkup_day_week_ne_chet)
        elif message.text == 'Уйду ли я с другом\подругой?':
            bot.send_message(message.chat.id, "Прекрасно, пожалуйста, скажи, из какой группы твой друг\подруга?\n"
                                              "╰(*°▽°*)╯",
                             parse_mode='html')
            bot.register_next_step_handler(message,quit_name_group)
    else:
        bot.send_message(message.chat.id,
                         f"Пожалуйста, не шути со мной {message.from_user.first_name} {message.from_user.last_name}",
                         parse_mode='html')

def update_name_group_user(message,name_group):
    if chek_group_user(message.text, message.from_user.id) == True:
        murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_menu = types.KeyboardButton('Меню')
        murkup_quit_home_menu.add(quit_menu)
        bot.send_message(message.chat.id, 'Отлично, давай перейдем в Меню', parse_mode='html', reply_markup=murkup_quit_home_menu)

    else:
        bot.send_message(message.chat.id, "К привеликому сожалению, я не нашел в своей базе, подобной группы,"
                                          " пожалуйста, проверь, не допустил ли ты очепятку?",
                         parse_mode='html')
#inline_button кнопки, реакция на вызовы по callback_data
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'mon_chet':
                schedule_day_week_db = []
                print("done")
                schedule_day_week_db = schedule_day_week('ПОНЕДЕЛЬНИК', '1', call.from_user.id)
                time_begin_lesson = ['8:30','10:10','11:50','13:40','15:20','17:00']
                time_end_lesson = ['10:00','11:40','13:20','15:10','16:50','18:30']
                para = ""
                para += "<u>📎 Понедельник:</u>\n"
                chek = True
                murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
                quit_menu = types.KeyboardButton('Меню')
                murkup_quit_home_menu.add(quit_menu)
                for i in range(len(schedule_day_week_db)):
                    for y in range(len(schedule_day_week_db[i])):
                        if schedule_day_week_db[i][y] != "Окно":
                            chek = True
                            break
                        else:
                            chek = False
                            break
                    if chek == True:
                        para += f" <b> ⏰ Начало пары в {time_begin_lesson[i]}</b>  \n"
                    for y in range(len(schedule_day_week_db[i])):
                        if schedule_day_week_db[i][y] != "Окно":
                            para += f"        {schedule_day_week_db[i][y]}  \n"
                        else:
                            continue
                bot.send_message(call.message.chat.id, para + "\n", parse_mode='html', reply_markup=murkup_quit_home_menu)
            elif call.data == 'tue_chet':
                schedule_day_week_db = []
                print("done")
                schedule_day_week_db = schedule_day_week('ВТОРНИК', '1', call.from_user.id)
                time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
                time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
                para = ""
                para += "<u>📎 Вторник:</u>\n"
                chek = True
                murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
                quit_menu = types.KeyboardButton('Меню')
                murkup_quit_home_menu.add(quit_menu)
                for i in range(len(schedule_day_week_db)):
                    for y in range(len(schedule_day_week_db[i])):
                        if schedule_day_week_db[i][y] != "Окно":
                            chek = True
                            break
                        else:
                            chek = False
                            break
                    if chek == True:
                        para += f" <b> ⏰ Начало пары в {time_begin_lesson[i]}</b>  \n"
                    for y in range(len(schedule_day_week_db[i])):
                        if schedule_day_week_db[i][y] != "Окно":
                            para += f"        {schedule_day_week_db[i][y]}  \n"
                        else:
                            continue
                bot.send_message(call.message.chat.id, para + "\n", parse_mode='html',
                                 reply_markup=murkup_quit_home_menu)
            #Среда
            elif call.data == 'wed_chet':
                 schedule_day_week_db = []
                 schedule_day_week_db = schedule_day_week('СРЕДА', '1', call.from_user.id)
                 time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
                 time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
                 para = ""
                 para += "<u>📎 Среда:</u>\n"
                 chek = True
                 murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 quit_menu = types.KeyboardButton('Меню')
                 murkup_quit_home_menu.add(quit_menu)
                 for i in range(len(schedule_day_week_db)):
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             chek = True
                             break
                         else:
                             chek = False
                             break
                     if chek == True:
                         para += f" <b> ⏰ Начало пары в {time_begin_lesson[i]}</b>  \n"
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             para += f"        {schedule_day_week_db[i][y]}  \n"
                         else:
                             continue
                 bot.send_message(call.message.chat.id, para + "\n", parse_mode='html',reply_markup=murkup_quit_home_menu)
            #Четверг
            elif call.data == 'thu_chet':
                 schedule_day_week_db = []
                 schedule_day_week_db = schedule_day_week('ЧЕТВЕРГ', '1', call.from_user.id)
                 time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
                 time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
                 para = ""
                 para += "<u>📎 Четверг:</u>\n"
                 chek = True
                 murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 quit_menu = types.KeyboardButton('Меню')
                 murkup_quit_home_menu.add(quit_menu)
                 for i in range(len(schedule_day_week_db)):
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             chek = True
                             break
                         else:
                             chek = False
                             break
                     if chek == True:
                         para += f" <b> ⏰ Начало пары в {time_begin_lesson[i]}</b>  \n"
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             para += f"        {schedule_day_week_db[i][y]}  \n"
                         else:
                             continue
                 bot.send_message(call.message.chat.id, para + "\n", parse_mode='html',reply_markup=murkup_quit_home_menu)
            #Пятница
            elif call.data == 'fri_chet':
                 schedule_day_week_db = []
                 schedule_day_week_db = schedule_day_week('ПЯТНИЦА', '1', call.from_user.id)
                 time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
                 time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
                 para = ""
                 para += "<u>📎 Пятница:</u>\n"
                 chek = True
                 murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 quit_menu = types.KeyboardButton('Меню')
                 murkup_quit_home_menu.add(quit_menu)
                 for i in range(len(schedule_day_week_db)):
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             chek = True
                             break
                         else:
                             chek = False
                             break
                     if chek == True:
                         para += f" <b> ⏰ Начало пары в {time_begin_lesson[i]}</b>  \n"
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             para += f"        {schedule_day_week_db[i][y]}  \n"
                         else:
                             continue
                 bot.send_message(call.message.chat.id, para + "\n", parse_mode='html',reply_markup=murkup_quit_home_menu)
            #Суббота
            elif call.data == 'sat_chet':
                 schedule_day_week_db = []
                 schedule_day_week_db = schedule_day_week('СУББОТА', '1', call.from_user.id)
                 time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']

                 para = ""
                 para += "<u>📎 Суббота:</u>\n"
                 chek = True
                 murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 quit_menu = types.KeyboardButton('Меню')
                 murkup_quit_home_menu.add(quit_menu)
                 for i in range(len(schedule_day_week_db)):
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             chek = True
                             break
                         else:
                             chek = False
                             break
                     if chek == True:
                         para += f" <b> ⏰ Начало пары в {time_begin_lesson[i]}</b>  \n"
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             para += f"        {schedule_day_week_db[i][y]}  \n"
                         else:
                             continue
                 bot.send_message(call.message.chat.id, para + "\n", parse_mode='html',reply_markup=murkup_quit_home_menu)
            elif call.data == 'mon_ne_chet':
                 schedule_day_week_db = []
                 schedule_day_week_db = schedule_day_week('ПОНЕДЕЛЬНИК', '2', call.from_user.id)
                 time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
                 time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
                 para = ""
                 para += "<u>📎 Понедельник:</u>\n"
                 chek = True
                 murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 quit_menu = types.KeyboardButton('Меню')
                 murkup_quit_home_menu.add(quit_menu)
                 for i in range(len(schedule_day_week_db)):
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             chek = True
                             break
                         else:
                             chek = False
                             break
                     if chek == True:
                         para += f" <b> ⏰ Начало пары в {time_begin_lesson[i]}</b>  \n"
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             para += f"        {schedule_day_week_db[i][y]}  \n"
                         else:
                             continue
                 bot.send_message(call.message.chat.id, para + "\n", parse_mode='html',reply_markup=murkup_quit_home_menu)
            #Вторник
            elif call.data == 'tue_ne_chet':
                 schedule_day_week_db = []
                 schedule_day_week_db = schedule_day_week('ВТОРНИК', '2', call.from_user.id)
                 time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
                 time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
                 para = ""
                 para += "<u>📎 Вторник:</u>\n"
                 chek = True
                 murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 quit_menu = types.KeyboardButton('Меню')
                 murkup_quit_home_menu.add(quit_menu)
                 for i in range(len(schedule_day_week_db)):
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             chek = True
                             break
                         else:
                             chek = False
                             break
                     if chek == True:
                         para += f" <b> ⏰ Начало пары в {time_begin_lesson[i]}</b>  \n"
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             para += f"        {schedule_day_week_db[i][y]}  \n"
                         else:
                             continue
                 bot.send_message(call.message.chat.id, para + "\n", parse_mode='html',reply_markup=murkup_quit_home_menu)
            #Среда
            elif call.data == 'wed_ne_chet':
                 schedule_day_week_db = []
                 schedule_day_week_db = schedule_day_week('СРЕДА', '2', call.from_user.id)
                 time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
                 time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
                 para = ""
                 para += "<u>📎 Среда:</u>\n"
                 chek = True
                 murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 quit_menu = types.KeyboardButton('Меню')
                 murkup_quit_home_menu.add(quit_menu)
                 for i in range(len(schedule_day_week_db)):
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             chek = True
                             break
                         else:
                             chek = False
                             break
                     if chek == True:
                         para += f" <b> ⏰ Начало пары в {time_begin_lesson[i]}</b>  \n"
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             para += f"        {schedule_day_week_db[i][y]}  \n"
                         else:
                             continue
                 bot.send_message(call.message.chat.id, para + "\n", parse_mode='html',reply_markup=murkup_quit_home_menu)
            #Четверг
            elif call.data == 'thu_ne_chet':
                 schedule_day_week_db = []
                 schedule_day_week_db = schedule_day_week('ЧЕТВЕРГ', '2', call.from_user.id)
                 time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
                 time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
                 para = ""
                 para += "<u>📎 Четверг:</u>\n"
                 chek = True
                 murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 quit_menu = types.KeyboardButton('Меню')
                 murkup_quit_home_menu.add(quit_menu)
                 for i in range(len(schedule_day_week_db)):
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             chek = True
                             break
                         else:
                             chek = False
                             break
                     if chek == True:
                         para += f" <b> ⏰ Начало пары в {time_begin_lesson[i]}</b>  \n"
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             para += f"        {schedule_day_week_db[i][y]}  \n"
                         else:
                             continue
                 bot.send_message(call.message.chat.id, para + "\n", parse_mode='html',reply_markup=murkup_quit_home_menu)
            #Пятница
            elif call.data == 'fri_ne_chet':
                 schedule_day_week_db = []
                 schedule_day_week_db = schedule_day_week('ПЯТНИЦА', '2', call.from_user.id)
                 time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
                 time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
                 para = ""
                 para += "<u>📎 Пятница:</u>\n"
                 chek = True
                 murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 quit_menu = types.KeyboardButton('Меню')
                 murkup_quit_home_menu.add(quit_menu)
                 for i in range(len(schedule_day_week_db)):
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             chek = True
                             break
                         else:
                             chek = False
                             break
                     if chek == True:
                         para += f" <b> ⏰ Начало пары в {time_begin_lesson[i]}</b>  \n"
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             para += f"        {schedule_day_week_db[i][y]}  \n"
                         else:
                             continue
                 bot.send_message(call.message.chat.id, para + "\n", parse_mode='html',reply_markup=murkup_quit_home_menu)
            elif call.data == 'sat_ne_chet':
                 schedule_day_week_db = []
                 schedule_day_week_db = schedule_day_week('СУББОТА', '2', call.from_user.id)
                 time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
                 time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
                 para = ""
                 para += "<u>📎 Суббота:</u>\n"
                 chek = True
                 murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 quit_menu = types.KeyboardButton('Меню')
                 murkup_quit_home_menu.add(quit_menu)
                 for i in range(len(schedule_day_week_db)):
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             chek = True
                             break
                         else:
                             chek = False
                             break
                     if chek == True:
                         para += f" <b> ⏰ Начало пары в {time_begin_lesson[i]}</b>  \n"
                     for y in range(len(schedule_day_week_db[i])):
                         if schedule_day_week_db[i][y] != "Окно":
                             para += f"        {schedule_day_week_db[i][y]}  \n"
                         else:
                             continue
                 bot.send_message(call.message.chat.id, para + "\n", parse_mode='html',reply_markup=murkup_quit_home_menu)
    except Exception as e:
        print(repr(e))
#ну привет, уйду не уйду с другом

def quit_name_group(message):
    if chek_group_user_friend(message.text) == True:


        murkup_parity_quit = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_parity_chet = types.KeyboardButton('Первая')
        quit_parity_non = types.KeyboardButton('Вторая')
        name_frined_group = message.text
        murkup_parity_quit.add(quit_parity_chet, quit_parity_non)
        bot.send_message(message.from_user.id, 'Пожалуйста, выбери неделю', parse_mode='html',
                         reply_markup=murkup_parity_quit)
        bot.register_next_step_handler(message,quit_chet,name_frined_group)

    else:
        bot.send_message(message.chat.id,
                         "К сожалению, группы твоего (по-)друга(-и) не существует, проверь пожалуйста"
                         "вдруг была какая-то очепятка╰(*°▽°*)╯", parse_mode='html', reply_markup=murkup_parity_quit)


def quit_chet(message,name_group):
        if message.text == 'Первая':
            murkup_day_week_ne_chet = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mon = types.KeyboardButton("Пн-1")
            tue = types.KeyboardButton("Вт-1")
            wed = types.KeyboardButton("Ср-1")
            thu = types.KeyboardButton("Чт-1")
            fri = types.KeyboardButton("Пт-1")
            sat = types.KeyboardButton("Сб-1")
            murkup_day_week_ne_chet.add(mon, tue, wed, thu, fri, sat)
            bot.send_message(message.chat.id, "Прекрасно, пожалуйста, выбери день недели(●'◡'●)",
                             parse_mode='html', reply_markup=murkup_day_week_ne_chet)
            bot.register_next_step_handler(message,quit_rezult,name_group)
        if message.text == 'Вторая':
            murkup_day_week_ne_chet = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mon = types.KeyboardButton("Пн-2")
            tue = types.KeyboardButton("Вт-2")
            wed = types.KeyboardButton("Ср-2")
            thu = types.KeyboardButton("Чт-2")
            fri = types.KeyboardButton("Пт-2")
            sat = types.KeyboardButton("Сб-2")
            murkup_day_week_ne_chet.add(mon, tue, wed, thu, fri, sat)
            bot.send_message(message.chat.id, "Прекрасно, пожалуйста, выбери день недели(●'◡'●)",
                             parse_mode='html', reply_markup=murkup_day_week_ne_chet)
            bot.register_next_step_handler(message, quit_rezult, name_group)
def quit_rezult(message, name_group):
    #первая НЕДЕЛЯ
    if message.text == 'Пн-1':
        hour_group_user_last_hour = times_db('ПОНЕДЕЛЬНИК', '1', message.from_user.id)
        hour_group_friend_last_hour = times_db_friend('ПОНЕДЕЛЬНИК', '1', name_group)
        hour_group_user_first_hour = times_db_first('ПОНЕДЕЛЬНИК', '1', message.from_user.id)
        hour_group_friend_first_hour = times_db_friend_first('ПОНЕДЕЛЬНИК', '1', name_group)
        murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_menu = types.KeyboardButton('Меню')
        murkup_quit_home_menu.add(quit_menu)
        hour_user_items = []
        time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
        time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        #last_user
        for i in range(0, len(hour_group_user_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_last_hour.append(time_end_lesson[hour_user_items[i]])
        #begin_user
        hour_user_items =[]
        for i in range(0, len(hour_group_user_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_first_hour = []
        for i in range(0,len(hour_user_items)):
            hour_group_user_first_hour.append(time_begin_lesson[hour_user_items[i]])
        hour_user_items = []
        # last_friend
        for i in range(0, len(hour_group_friend_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_friend
        hour_user_items = []
        for i in range(0, len(hour_group_friend_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_first_hour.append(time_begin_lesson[hour_user_items[i]])
        if len(hour_group_user_last_hour) == 0 and len(hour_group_friend_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты не учишься в этот день,'
                                              f' а твой друг закончит в '
                                              f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu) ############################################
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) == 0:
            bot.send_message(message.chat.id, f'Сегодня ни ты, ни твой друг не учитесь!\n'
                                              f'🎉🎉🎉🎉🎉', parse_mode='html',
                             reply_markup=murkup_quit_home_menu)
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты закончишь в '
                                              f'<b><u>{hour_group_user_last_hour[-1]}</u></b>,'
                                              f' а твой друг сегодня не учится.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'),
                             reply_markup=murkup_quit_home_menu)  ###################################
        elif len(hour_group_friend_last_hour) > 0 and len(hour_group_user_last_hour) > 0:
            if hour_group_user_last_hour[-1] == hour_group_friend_last_hour[-1]:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но и пойти на'
                                                      f' уроки вы сможете вместе, ведь начнете вы в '
                                                      f'<b><u>{hour_group_friend_first_hour[0]}</u></b>, а закончите в '
                                                      f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ##########
                else:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но пойти на'
                                                      f' уроки вместе не сможете. Вы закончите в'
                                                      f' <b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
            else:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id,
                                     f'К сожалению, вы не сможете уйти вместе с другом.'
                                     f' Но пойти на уроки вместе можете, ведь начинаете вы в '
                                     f'<b><u>{hour_group_friend_first_hour[0]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ############
                else:
                    bot.send_message(message.chat.id, f'К сожалению, вы не сможете уйти вместе и пойти вместе с другом.',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ##########
    elif message.text == 'Вт-1':
        hour_group_user_last_hour = []
        hour_group_friend_last_hour = []
        hour_group_user_first_hour = []
        hour_group_friend_first_hour = []
        hour_group_user_last_hour = times_db('ВТОРНИК', '1', message.from_user.id)
        hour_group_friend_last_hour = times_db_friend('ВТОРНИК', '1', name_group)
        hour_group_user_first_hour = times_db_first('ВТОРНИК', '1', message.from_user.id)
        hour_group_friend_first_hour = times_db_friend_first('ВТОРНИК', '1', name_group)
        murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_menu = types.KeyboardButton('Меню')
        murkup_quit_home_menu.add(quit_menu)
        hour_user_items = []
        time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
        time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        # last_user
        for i in range(0, len(hour_group_user_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_user
        hour_user_items = []
        for i in range(0, len(hour_group_user_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_first_hour.append(time_begin_lesson[hour_user_items[i]])
        hour_user_items = []
        # last_friend
        for i in range(0, len(hour_group_friend_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_friend
        hour_user_items = []
        for i in range(0, len(hour_group_friend_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_first_hour.append(time_begin_lesson[hour_user_items[i]])
        if len(hour_group_user_last_hour) == 0 and len(hour_group_friend_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты не учишься в этот день,'
                                              f' а твой друг закончит в '
                                              f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) == 0:
            bot.send_message(message.chat.id, f'Сегодня ни ты, ни твой друг не учитесь!\n'
                                              f'🎉🎉🎉🎉🎉', parse_mode='html',
                             reply_markup=murkup_quit_home_menu)
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты закончишь в '
                                              f'<b><u>{hour_group_user_last_hour[-1]}</u></b>,'
                                              f' а твой друг сегодня не учится.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) > 0 and len(hour_group_user_last_hour) > 0:
            if hour_group_user_last_hour[-1] == hour_group_friend_last_hour[-1]:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но и пойти на'
                                                      f' уроки вы сможете вместе, ведь начнете в '
                                                      f'<b><u>{hour_group_friend_first_hour[0]}</u></b>, а закончите в '
                                                      f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но пойти на'
                                                      f' уроки вместе не сможете. Вы закончите в'
                                                      f' <b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
            else:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id,
                                     f'К сожалению, вы не сможете уйти вместе с другом.'
                                     f' Но пойти на уроки вместе можете, ведь начинаете вы в '
                                     f'<b><u>{hour_group_friend_first_hour[0]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'К сожалению, вы не сможете уйти вместе и пойти вместе с другом.',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
    elif message.text == 'Ср-1':
        hour_group_user_last_hour = []
        hour_group_friend_last_hour = []
        hour_group_user_first_hour = []
        hour_group_friend_first_hour = []
        hour_group_user_last_hour = times_db('СРЕДА', '1', message.from_user.id)
        hour_group_friend_last_hour = times_db_friend('СРЕДА', '1', name_group)
        hour_group_user_first_hour = times_db_first('СРЕДА', '1', message.from_user.id)
        hour_group_friend_first_hour = times_db_friend_first('СРЕДА', '1', name_group)
        murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_menu = types.KeyboardButton('Меню')
        murkup_quit_home_menu.add(quit_menu)
        hour_user_items = []
        time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
        time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        # last_user
        for i in range(0, len(hour_group_user_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_user
        hour_user_items = []
        for i in range(0, len(hour_group_user_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_first_hour.append(time_begin_lesson[hour_user_items[i]])
        hour_user_items = []
        # last_friend
        for i in range(0, len(hour_group_friend_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_friend
        hour_user_items = []
        for i in range(0, len(hour_group_friend_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_first_hour.append(time_begin_lesson[hour_user_items[i]])
        if len(hour_group_user_last_hour) == 0 and len(hour_group_friend_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты не учишься в этот день,'
                                              f' а твой друг закончит в '
                                              f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) == 0:
            bot.send_message(message.chat.id, f'Сегодня ни ты, ни твой друг не учитесь!\n'
                                              f'🎉🎉🎉🎉🎉', parse_mode='html',
                             reply_markup=murkup_quit_home_menu)
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты закончишь в '
                                              f'<b><u>{hour_group_user_last_hour[-1]}</u></b>,'
                                              f' а твой друг сегодня не учится.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) > 0 and len(hour_group_user_last_hour) > 0:
            if hour_group_user_last_hour[-1] == hour_group_friend_last_hour[-1]:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но и пойти на'
                                                      f' уроки, вы сможете вместе, ведь начинаете вы в '
                                                      f'<b><u>{hour_group_friend_first_hour[0]}</u></b>, а закончите в '
                                                      f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но пойти на'
                                                      f' уроки вместе не сможете. Вы закончите в'
                                                      f' <b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
            else:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id,
                                     f'К сожалению, вы не сможете уйти вместе с другом.'
                                     f' Но пойти на уроки вместе можете, ведь начинаете вы в '
                                     f'<b><u>{hour_group_friend_first_hour[0]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'К сожалению, вы не сможете уйти вместе и пойти вместе с другом.',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
    elif message.text == 'Чт-1':
        hour_group_user_last_hour = []
        hour_group_friend_last_hour = []
        hour_group_user_first_hour = []
        hour_group_friend_first_hour = []
        hour_group_user_last_hour = times_db('ЧЕТВЕРГ', '1', message.from_user.id)
        hour_group_friend_last_hour = times_db_friend('ЧЕТВЕРГ', '1', name_group)
        hour_group_user_first_hour = times_db_first('ЧЕТВЕРГ', '1', message.from_user.id)
        hour_group_friend_first_hour = times_db_friend_first('ЧЕТВЕРГ', '1', name_group)
        murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_menu = types.KeyboardButton('Меню')
        murkup_quit_home_menu.add(quit_menu)
        hour_user_items = []
        time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
        time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        # last_user
        for i in range(0, len(hour_group_user_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_user
        hour_user_items = []
        for i in range(0, len(hour_group_user_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_first_hour.append(time_begin_lesson[hour_user_items[i]])
        hour_user_items = []
        # last_friend
        for i in range(0, len(hour_group_friend_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_friend
        hour_user_items = []
        for i in range(0, len(hour_group_friend_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_first_hour.append(time_begin_lesson[hour_user_items[i]])
        if len(hour_group_user_last_hour) == 0 and len(hour_group_friend_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты не учишься в этот день,'
                                              f' а твой друг закончит в '
                                              f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) == 0:
            bot.send_message(message.chat.id, f'Сегодня ни ты, ни твой друг не учитесь!\n'
                                              f'🎉🎉🎉🎉🎉', parse_mode='html',
                             reply_markup=murkup_quit_home_menu)
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты закончишь в '
                                              f'<b><u>{hour_group_user_last_hour[-1]}</u></b>,'
                                              f' а твой друг сегодня не учится.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) > 0 and len(hour_group_user_last_hour) > 0:
            if hour_group_user_last_hour[-1] == hour_group_friend_last_hour[-1]:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но и пойти на'
                                                      f' уроки вы сможете вместе, ведь начинаете вы в '
                                                      f'<b><u>{hour_group_friend_first_hour[0]}</u></b>, а закончите в '
                                                      f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но пойти на'
                                                      f' уроки вместе не сможете. Вы закончите в'
                                                      f' <b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
            else:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id,
                                     f'К сожалению, вы не сможете уйти вместе с другом.'
                                     f' Но пойти на уроки вместе можете, ведь начинаете вы в '
                                     f'<b><u>{hour_group_friend_first_hour[0]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'К сожалению, вы не сможете уйти вместе и пойти вместе с другом.',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
    elif message.text == 'Пт-1':
        hour_group_user_last_hour = []
        hour_group_friend_last_hour = []
        hour_group_user_first_hour = []
        hour_group_friend_first_hour = []
        hour_group_user_last_hour = times_db('ПЯТНИЦА', '1', message.from_user.id)
        hour_group_friend_last_hour = times_db_friend('ПЯТНИЦА', '1', name_group)
        hour_group_user_first_hour = times_db_first('ПЯТНИЦА', '1', message.from_user.id)
        hour_group_friend_first_hour = times_db_friend_first('ПЯТНИЦА', '1', name_group)
        murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_menu = types.KeyboardButton('Меню')
        murkup_quit_home_menu.add(quit_menu)
        hour_user_items = []
        time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
        time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        # last_user
        for i in range(0, len(hour_group_user_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_user
        hour_user_items = []
        for i in range(0, len(hour_group_user_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_first_hour.append(time_begin_lesson[hour_user_items[i]])
        hour_user_items = []
        # last_friend
        for i in range(0, len(hour_group_friend_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_friend
        hour_user_items = []
        for i in range(0, len(hour_group_friend_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_first_hour.append(time_begin_lesson[hour_user_items[i]])
        if len(hour_group_user_last_hour) == 0 and len(hour_group_friend_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты не учишься в этот день,'
                                              f' а твой друг закончит в '
                                              f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) == 0:
            bot.send_message(message.chat.id, f'Сегодня ни ты, ни твой друг не учитесь!\n'
                                              f'🎉🎉🎉🎉🎉', parse_mode='html',
                             reply_markup=murkup_quit_home_menu)
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты закончишь в '
                                              f'<b><u>{hour_group_user_last_hour[-1]}</u></b>,'
                                              f' а твой друг сегодня не учится.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) > 0 and len(hour_group_user_last_hour) > 0:
            if hour_group_user_last_hour[-1] == hour_group_friend_last_hour[-1]:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но и пойти на'
                                                      f' уроки вы сможете вместе, ведь начинаете в '
                                                      f'<b><u>{hour_group_friend_first_hour[0]}</u></b>, а закончите в '
                                                      f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но пойти на'
                                                      f' уроки вместе не сможете. Вы закончите в'
                                                      f' <b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
            else:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id,
                                     f'К сожалению, вы не сможете уйти вместе с другом.'
                                     f' Но пойти на уроки вместе можете, ведь начинаете вы в '
                                     f'<b><u>{hour_group_friend_first_hour[0]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id,
                                     f'К сожалению, вы не сможете уйти вместе и пойти вместе с другом.',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
    elif message.text == 'Сб-1':
        hour_group_user_last_hour = []
        hour_group_friend_last_hour = []
        hour_group_user_first_hour = []
        hour_group_friend_first_hour = []
        hour_group_user_last_hour = times_db('СУББОТА', '1', message.from_user.id)
        hour_group_friend_last_hour = times_db_friend('СУББОТА', '1', name_group)
        hour_group_user_first_hour = times_db_first('СУББОТА', '1', message.from_user.id)
        hour_group_friend_first_hour = times_db_friend_first('СУББОТА', '1', name_group)
        murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_menu = types.KeyboardButton('Меню')
        murkup_quit_home_menu.add(quit_menu)
        hour_user_items = []
        time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
        time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        # last_user
        for i in range(0, len(hour_group_user_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_user
        hour_user_items = []
        for i in range(0, len(hour_group_user_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_first_hour.append(time_begin_lesson[hour_user_items[i]])
        hour_user_items = []
        # last_friend
        for i in range(0, len(hour_group_friend_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_friend
        hour_user_items = []
        for i in range(0, len(hour_group_friend_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_first_hour.append(time_begin_lesson[hour_user_items[i]])
        if len(hour_group_user_last_hour) == 0 and len(hour_group_friend_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты не учишься в этот день,'
                                              f' а твой друг закончит в '
                                              f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) == 0:
            bot.send_message(message.chat.id, f'Сегодня ни ты, ни твой друг не учитесь!\n'
                                              f'🎉🎉🎉🎉🎉', parse_mode='html',
                             reply_markup=murkup_quit_home_menu)
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты закончишь в '
                                              f'<b><u>{hour_group_user_last_hour[-1]}</u></b>,'
                                              f' а твой друг сегодня не учится.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) > 0 and len(hour_group_user_last_hour) > 0:
            if hour_group_user_last_hour[-1] == hour_group_friend_last_hour[-1]:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но и пойти на'
                                                      f' уроки вы сможете вместе, ведь начинаете вы в '
                                                      f'<b><u>{hour_group_friend_first_hour[0]}</u></b>, а закончите в '
                                                      f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но пойти на'
                                                      f' уроки вместе не сможете. Вы закончите в'
                                                      f' <b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
            else:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id,
                                     f'К сожалению, вы не сможете уйти вместе с другом.'
                                     f' Но пойти на уроки вместе можете, ведь начинаете вы в '
                                     f'<b><u>{hour_group_friend_first_hour[0]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'К сожалению, вы не сможете уйти вместе и пойти вместе с другом.',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########


    #вторая НЕДЕЛЯ
    elif message.text == 'Пн-2':
        hour_group_user_last_hour = []
        hour_group_friend_last_hour = []
        hour_group_user_first_hour = []
        hour_group_friend_first_hour = []
        hour_group_user_last_hour = times_db('ПОНЕДЕЛЬНИК', '2', message.from_user.id)
        hour_group_friend_last_hour = times_db_friend('ПОНЕДЕЛЬНИК', '2', name_group)
        hour_group_user_first_hour = times_db_first('ПОНЕДЕЛЬНИК', '2', message.from_user.id)
        hour_group_friend_first_hour = times_db_friend_first('ПОНЕДЕЛЬНИК', '2', name_group)
        murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_menu = types.KeyboardButton('Меню')
        murkup_quit_home_menu.add(quit_menu)
        hour_user_items = []
        time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
        time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        # last_user
        for i in range(0, len(hour_group_user_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_user
        hour_user_items = []
        for i in range(0, len(hour_group_user_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_first_hour.append(time_begin_lesson[hour_user_items[i]])
        hour_user_items = []
        # last_friend
        for i in range(0, len(hour_group_friend_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_friend
        hour_user_items = []
        for i in range(0, len(hour_group_friend_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_first_hour.append(time_begin_lesson[hour_user_items[i]])
        if len(hour_group_user_last_hour) == 0 and len(hour_group_friend_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты не учишься в этот день,'
                                              f' а твой друг закончит в '
                                              f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) == 0:
            bot.send_message(message.chat.id, f'Сегодня ни ты, ни твой друг не учитесь!\n'
                                              f'🎉🎉🎉🎉🎉', parse_mode='html',
                             reply_markup=murkup_quit_home_menu)
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты закончишь в '
                                              f'<b><u>{hour_group_user_last_hour[-1]}</u></b>,'
                                              f' а твой друг сегодня не учится.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) > 0 and len(hour_group_user_last_hour) > 0:
            if hour_group_user_last_hour[-1] == hour_group_friend_last_hour[-1]:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но и пойти на'
                                                      f' уроки вы сможете вместе, ведь начнете вы в '
                                                      f'<b><u>{hour_group_friend_first_hour[0]}</u></b>, а закончите в '
                                                      f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но пойти на'
                                                      f' уроки вместе не сможете. Вы закончите в'
                                                      f' <b><u>{hour_group_friend_last_hour[-1]}</u></b>',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
            else:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id,
                                     f'К сожалению, вы не сможете уйти вместе с другом.'
                                     f' Но пойти на уроки вместе можете, ведь начинаете вы в '
                                     f'<b><u>{hour_group_friend_first_hour[0]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'К сожалению, вы не сможете уйти вместе и пойти вместе с другом.',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
    elif message.text == 'Вт-2':
        hour_group_user_last_hour = []
        hour_group_friend_last_hour = []
        hour_group_user_first_hour = []
        hour_group_friend_first_hour = []
        hour_group_user_last_hour = times_db('ВТОРНИК', '2', message.from_user.id)
        hour_group_friend_last_hour = times_db_friend('ВТОРНИК', '2', name_group)
        hour_group_user_first_hour = times_db_first('ВТОРНИК', '2', message.from_user.id)
        hour_group_friend_first_hour = times_db_friend_first('ВТОРНИК', '2', name_group)
        murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_menu = types.KeyboardButton('Меню')
        murkup_quit_home_menu.add(quit_menu)
        hour_user_items = []
        time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
        time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        # last_user
        for i in range(0, len(hour_group_user_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_user
        hour_user_items = []
        for i in range(0, len(hour_group_user_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_first_hour.append(time_begin_lesson[hour_user_items[i]])
        hour_user_items = []
        # last_friend
        for i in range(0, len(hour_group_friend_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_friend
        hour_user_items = []
        for i in range(0, len(hour_group_friend_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_first_hour.append(time_begin_lesson[hour_user_items[i]])
        if len(hour_group_user_last_hour) == 0 and len(hour_group_friend_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты не учишься в этот день,'
                                              f' а твой друг закончит в '
                                              f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) == 0:
            bot.send_message(message.chat.id, f'Сегодня ни ты, ни твой друг не учитесь!\n'
                                              f'🎉🎉🎉🎉🎉', parse_mode='html',
                             reply_markup=murkup_quit_home_menu)
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты закончишь в '
                                              f'<b><u>{hour_group_user_last_hour[-1]}</u></b>,'
                                              f' а твой друг сегодня не учится.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) > 0 and len(hour_group_user_last_hour) > 0:
            if hour_group_user_last_hour[-1] == hour_group_friend_last_hour[-1]:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но и пойти на'
                                                      f' уроки вы сможете вместе, ведь начинаете вы в '
                                                      f'<b><u>{hour_group_friend_first_hour[0]}</u></b>, а закончите в '
                                                      f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но пойти на'
                                                      f' уроки вместе не сможете. Вы закончите в'
                                                      f' <b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
            else:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id,
                                     f'К сожалению, вы не сможете уйти вместе с другом.'
                                     f' Но пойти на уроки вместе можете, ведь начинаете вы в '
                                     f'<b><u>{hour_group_friend_first_hour[0]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'К сожалению, вы не сможете уйти вместе и пойти вместе с другом.',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
    elif message.text == 'Ср-2':
        hour_group_user_last_hour = []
        hour_group_friend_last_hour = []
        hour_group_user_first_hour = []
        hour_group_friend_first_hour = []
        hour_group_user_last_hour = times_db('СРЕДА', '2', message.from_user.id)
        hour_group_friend_last_hour = times_db_friend('СРЕДА', '2', name_group)
        hour_group_user_first_hour = times_db_first('СРЕДА', '2', message.from_user.id)
        hour_group_friend_first_hour = times_db_friend_first('СРЕДА', '2', name_group)
        murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_menu = types.KeyboardButton('Меню')
        murkup_quit_home_menu.add(quit_menu)
        hour_user_items = []
        time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
        time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        # last_user
        for i in range(0, len(hour_group_user_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_user
        hour_user_items = []
        for i in range(0, len(hour_group_user_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_first_hour.append(time_begin_lesson[hour_user_items[i]])
        hour_user_items = []
        # last_friend
        for i in range(0, len(hour_group_friend_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_friend
        hour_user_items = []
        for i in range(0, len(hour_group_friend_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_first_hour.append(time_begin_lesson[hour_user_items[i]])
        if len(hour_group_user_last_hour) == 0 and len(hour_group_friend_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты не учишься в этот день,'
                                              f' а твой друг закончит в '
                                              f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) == 0:
            bot.send_message(message.chat.id, f'Сегодня ни ты, ни твой друг не учитесь!\n'
                                              f'🎉🎉🎉🎉🎉', parse_mode='html',
                             reply_markup=murkup_quit_home_menu)
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты закончишь в '
                                              f'<b><u>{hour_group_user_last_hour[-1]}</u></b>,'
                                              f' а твой друг сегодня не учится.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) > 0 and len(hour_group_user_last_hour) > 0:
            if hour_group_user_last_hour[-1] == hour_group_friend_last_hour[-1]:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но и пойти на'
                                                      f' уроки вы сможете вместе, ведь начинаете вы в '
                                                      f'<b><u>{hour_group_friend_first_hour[0]}</u></b>, а закончите в '
                                                      f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но пойти на'
                                                      f' уроки вместе не сможете. Вы закончите в'
                                                      f' <b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
            else:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id,
                                     f'К сожалению, вы не сможете уйти вместе с другом.'
                                     f' Но пойти на уроки вместе можете, ведь начинаете вы в '
                                     f'<b><u>{hour_group_friend_first_hour[0]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'К сожалению, вы не сможете уйти вместе и пойти вместе с другом.',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
    elif message.text == 'Чт-2':
        hour_group_user_last_hour = []
        hour_group_friend_last_hour = []
        hour_group_user_first_hour = []
        hour_group_friend_first_hour = []
        hour_group_user_last_hour = times_db('ЧЕТВЕРГ', '2', message.from_user.id)
        hour_group_friend_last_hour = times_db_friend('ЧЕТВЕРГ', '2', name_group)
        hour_group_user_first_hour = times_db_first('ЧЕТВЕРГ', '2', message.from_user.id)
        hour_group_friend_first_hour = times_db_friend_first('ЧЕТВЕРГ', '2', name_group)
        murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_menu = types.KeyboardButton('Меню')
        murkup_quit_home_menu.add(quit_menu)
        hour_user_items = []
        time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
        time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        # last_user
        for i in range(0, len(hour_group_user_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_user
        hour_user_items = []
        for i in range(0, len(hour_group_user_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_first_hour.append(time_begin_lesson[hour_user_items[i]])
        hour_user_items = []
        # last_friend
        for i in range(0, len(hour_group_friend_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_friend
        hour_user_items = []
        for i in range(0, len(hour_group_friend_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_first_hour.append(time_begin_lesson[hour_user_items[i]])
        if len(hour_group_user_last_hour) == 0 and len(hour_group_friend_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты не учишься в этот день,'
                                              f' а твой друг закончит в '
                                              f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) == 0:
            bot.send_message(message.chat.id, f'Сегодня ни ты, ни твой друг не учитесь!\n'
                                              f'🎉🎉🎉🎉🎉', parse_mode='html',
                             reply_markup=murkup_quit_home_menu)
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты закончишь в '
                                              f'<b><u>{hour_group_user_last_hour[-1]}</u></b>,'
                                              f' а твой друг сегодня не учится.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) > 0 and len(hour_group_user_last_hour) > 0:
            if hour_group_user_last_hour[-1] == hour_group_friend_last_hour[-1]:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но и пойти на'
                                                      f' уроки вы сможете вместе, ведь начинаете вы в '
                                                      f'<b><u>{hour_group_friend_first_hour[0]}</u></b>, а закончите в '
                                                      f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но пойти на'
                                                      f' уроки вместе не сможете. Вы закончите в'
                                                      f' <b><u>{hour_group_friend_last_hour[-1]}</u></b>.😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
            else:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id,
                                     f'К сожалению, вы не сможете уйти вместе с другом.'
                                     f' Но пойти на уроки вместе можете, ведь начинаете вы в '
                                     f'<b><u>{hour_group_friend_first_hour[0]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'К сожалению, вы не сможете уйти вместе и пойти вместе с другом.',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
    elif message.text == 'Пт-2':
        hour_group_user_last_hour = []
        hour_group_friend_last_hour = []
        hour_group_user_first_hour = []
        hour_group_friend_first_hour = []
        hour_group_user_last_hour = times_db('ПЯТНИЦА', '2', message.from_user.id)
        hour_group_friend_last_hour = times_db_friend('ПЯТНИЦА', '2', name_group)
        hour_group_user_first_hour = times_db_first('ПЯТНИЦА', '2', message.from_user.id)
        hour_group_friend_first_hour = times_db_friend_first('ПЯТНИЦА', '2', name_group)
        murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_menu = types.KeyboardButton('Меню')
        murkup_quit_home_menu.add(quit_menu)
        hour_user_items = []
        time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
        time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        # last_user
        for i in range(0, len(hour_group_user_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_user
        hour_user_items = []
        for i in range(0, len(hour_group_user_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_first_hour.append(time_begin_lesson[hour_user_items[i]])
        hour_user_items = []
        # last_friend
        for i in range(0, len(hour_group_friend_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_friend
        hour_user_items = []
        for i in range(0, len(hour_group_friend_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_first_hour.append(time_begin_lesson[hour_user_items[i]])
        if len(hour_group_user_last_hour) == 0 and len(hour_group_friend_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты не учишься в этот день,'
                                              f' а твой друг закончит в '
                                              f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) == 0:
            bot.send_message(message.chat.id, f'Сегодня ни ты, ни твой друг не учитесь!\n'
                                              f'🎉🎉🎉🎉🎉', parse_mode='html',
                             reply_markup=murkup_quit_home_menu)
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты закончишь в '
                                              f'<b><u>{hour_group_user_last_hour[-1]}</u></b>,'
                                              f' а твой друг сегодня не учится.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) > 0 and len(hour_group_user_last_hour) > 0:
            if hour_group_user_last_hour[-1] == hour_group_friend_last_hour[-1]:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но и пойти на'
                                                      f' уроки вы сможете вместе, ведь начинаете вы в '
                                                      f'<b><u>{hour_group_friend_first_hour[0]}</u></b>, а закончите в '
                                                      f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но пойти на'
                                                      f' уроки вместе не сможете. Вы закончите в'
                                                      f' <b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
            else:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id,
                                     f'К сожалению, вы не сможете уйти вместе с другом.'
                                     f' Но пойти на уроки вместе можете, ведь начинаете вы в '
                                     f'<b><u>{hour_group_friend_first_hour[0]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'К сожалению, вы не сможете уйти вместе и пойти вместе с другом.',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
    elif message.text == 'Сб-2':
        hour_group_user_last_hour = []
        hour_group_friend_last_hour = []
        hour_group_user_first_hour = []
        hour_group_friend_first_hour = []
        hour_group_user_last_hour = times_db('СУББОТА', '2', message.from_user.id)
        hour_group_friend_last_hour = times_db_friend('СУББОТА', '2', name_group)
        hour_group_user_first_hour = times_db_first('СУББОТА', '2', message.from_user.id)
        hour_group_friend_first_hour = times_db_friend_first('СУББОТА', '2', name_group)
        murkup_quit_home_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        quit_menu = types.KeyboardButton('Меню')
        murkup_quit_home_menu.add(quit_menu)
        hour_user_items = []
        time_begin_lesson = ['8:30', '10:10', '11:50', '13:40', '15:20', '17:00']
        time_end_lesson = ['10:00', '11:40', '13:20', '15:10', '16:50', '18:30']
        hour = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']
        # last_user
        for i in range(0, len(hour_group_user_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_user
        hour_user_items = []
        for i in range(0, len(hour_group_user_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_user_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_user_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_user_first_hour.append(time_begin_lesson[hour_user_items[i]])
        hour_user_items = []
        # last_friend
        for i in range(0, len(hour_group_friend_last_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_last_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_last_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_last_hour.append(time_end_lesson[hour_user_items[i]])
        # begin_friend
        hour_user_items = []
        for i in range(0, len(hour_group_friend_first_hour)):
            for y in range(0, len(hour)):
                if hour_group_friend_first_hour[i] == hour[y]:
                    hour_user_items.append(hour.index(hour[y]))
        hour_group_friend_first_hour = []
        for i in range(0, len(hour_user_items)):
            hour_group_friend_first_hour.append(time_begin_lesson[hour_user_items[i]])
        if len(hour_group_user_last_hour) == 0 and len(hour_group_friend_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты не учишься в этот день,'
                                              f' а твой друг закончит в '
                                              f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) == 0:
            bot.send_message(message.chat.id, f'Сегодня ни ты, ни твой друг не учитесь!\n'
                                              f'🎉🎉🎉🎉🎉', parse_mode='html',
                             reply_markup=murkup_quit_home_menu)
        elif len(hour_group_friend_last_hour) == 0 and len(hour_group_user_last_hour) > 0:
            bot.send_message(message.chat.id, f'К сожалению, вы не уйдете вместе, ты закончишь в '
                                              f'<b><u>{hour_group_user_last_hour[-1]}</u></b>,'
                                              f' а твой друг сегодня не учится.\n'
                                              f'Не грустите, может в другой раз😎', parse_mode='html')
            bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
        elif len(hour_group_friend_last_hour) > 0 and len(hour_group_user_last_hour) > 0:
            if hour_group_user_last_hour[-1] == hour_group_friend_last_hour[-1]:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но и пойти на'
                                                      f' уроки вы сможете вместе, ведь начинаете вы в '
                                                      f'<b><u>{hour_group_friend_first_hour[0]}</u></b>, а закончите в '
                                                      f'<b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'Да, вы сможете уйти вместе с другом. Но пойти на'
                                                      f' уроки вместе не сможете. Вы закончите в'
                                                      f' <b><u>{hour_group_friend_last_hour[-1]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/happy.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
            else:
                if hour_group_user_first_hour[0] == hour_group_friend_first_hour[0]:
                    bot.send_message(message.chat.id,
                                     f'К сожалению, вы не сможете уйти вместе с другом.'
                                     f' Но пойти на уроки вместе можете, ведь начинаете вы в '
                                     f'<b><u>{hour_group_friend_first_hour[0]}</u></b>😎',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########
                else:
                    bot.send_message(message.chat.id, f'К сожалению, вы не сможете уйти вместе и пойти вместе с другом.',
                                     parse_mode='html')
                    bot.send_photo(message.chat.id, photo=open('C:/Users/Anastasia/Desktop/algorithm-master/sed.jpg', 'rb'), reply_markup=murkup_quit_home_menu)  ########





    # elif call.data == 'wed_chet_friend':
    #
    # elif call.data == 'thu_chet_friend':
    #
    # elif call.data == 'fri_chet_friend':
    #
    # elif call.data == 'sat_chet_friend':
# RUN
bot.polling(none_stop=True)