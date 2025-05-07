import telebot
import sqlite3
from dotenv import load_dotenv
import os
from telebot import types
from heapq import nsmallest

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_API_KEY'))

user_state = {}

@bot.message_handler(commands=['start'])
def welcome(message):

    user_state[message.chat.id] = 'not_pressed'

    #ветка "start"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    eat = types.KeyboardButton("Где поесть? 🍜")
    time = types.KeyboardButton("Как провести время? 👀")
    pay = types.KeyboardButton("Платные предложения 💸")

    markup.add(eat, time, pay)

    bot.send_message(message.chat.id,
                     "Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный для навигации по городу.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

    sti = open('photo_bot/sticker.jpg', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, "Что Вас интересует?", reply_markup=markup)

@bot.message_handler(commands=['asianfood'])
def asianfood(message, id=1, previous_message=None):

    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query_asianfood = cursor.execute(f"SELECT COUNT(*) FROM `asianfood`")
    pages_count_asianfood = int(pages_count_query_asianfood.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left = id - 1 if id != 1 else pages_count_asianfood
    right = id + 1 if id != pages_count_asianfood else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `id_rate`, `description`, `img`, `link`, `id_average_cost`, `numphone` FROM `asianfood` WHERE `id` = '{id}';")
    name, street, id_rate, description, img, link, id_average_cost, numphone = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to asianfood | {left}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_asianfood)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to asianfood | {right}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона:\n{numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номера телефонов:\n{numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')
    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['fastfood'])
def fastfood(message, id=1, previous_message=None):

    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `fastfood`")
    pages_count_fastfood = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_fastfood = id - 1 if id != 1 else pages_count_fastfood
    right_fastfood = id + 1 if id != pages_count_fastfood else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `id_rate`, `description`, `img`, `link`, `id_average_cost` FROM `fastfood` WHERE `id` = '{id}';")
    name, street, id_rate, description, img, link, id_average_cost = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to fastfood | {left_fastfood}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_fastfood)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to fastfood |  {right_fastfood}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n\n"
        msg += f"{description}\n" if description != None else '_нет_\n'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n\n"
        msg += f"{description}\n" if description != None else '_нет_\n'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['canteen'])
def canteen(message, id=1, previous_message=None):

    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `canteen`")
    pages_count_canteen = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_canteen = id - 1 if id != 1 else pages_count_canteen
    right_canteen = id + 1 if id != pages_count_canteen else 1

    product_query = cursor.execute(
        f"SELECT `name`, `id_rate`, `id_average_cost`, `description`, `street`, `numphone`, `link`, `img` FROM `canteen` WHERE `id` = '{id}';")
    name, id_rate, id_average_cost, description, street, numphone, link, img = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to canteen | {left_canteen}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_canteen)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to canteen | {right_canteen}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}\n" if description != None else '_нет_\n'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}\n" if description != None else '_нет_\n'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['slavicfood'])
def slavicfood(message, id=1, previous_message=None):

    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `slavicfood`")
    pages_count_slavicfood = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_slavicfood = id - 1 if id != 1 else pages_count_slavicfood
    right_slavicfood = id + 1 if id != pages_count_slavicfood else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `id_rate`, `description`, `img`, `link`, `id_average_cost`, `numphone` FROM `slavicfood` WHERE `id` = '{id}';")
    name, street, id_rate, description, img, link, id_average_cost, numphone = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to slavicfood | {left_slavicfood}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_slavicfood)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to slavicfood | {right_slavicfood}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['seafood'])
def seafood(message, id=1, previous_message=None):

    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `seafood`")
    pages_count_seafood = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_seafood = id - 1 if id != 1 else pages_count_seafood
    right_seafood = id + 1 if id != pages_count_seafood else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `id_rate`, `description`, `img`, `link`, `id_average_cost`, `numphone` FROM `seafood` WHERE `id` = '{id}';")
    name, street, id_rate, description, img, link, id_average_cost, numphone = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to seafood | {left_seafood}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_seafood)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to seafood | {right_seafood}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_\n'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_\n'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['questroom'])
def questroom(message, id=1, previous_message=None):

    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `questroom`")
    pages_count_questroom = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_questroom = id - 1 if id != 1 else pages_count_questroom
    right_questroom = id + 1 if id != pages_count_questroom else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `id_rate`, `link`, `img`, `numphone`, `id_average_cost`, `description` FROM `questroom` WHERE `id` = '{id}';")
    name, street, id_rate, link, img, numphone, id_average_cost, description = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to questroom | {left_questroom}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_questroom)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to questroom | {right_questroom}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_\n'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_\n'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['nightclub'])
def nightclub(message, id=1, previous_message=None):

    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `nightclub`")
    pages_count_nightclub = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_nightclub = id - 1 if id != 1 else pages_count_nightclub
    right_nightclub = id + 1 if id != pages_count_nightclub else 1

    product_query = cursor.execute(
        f"SELECT `name`, `id_rate`, `description`, `average_cost`, `street`, `worktime`, `numphone`, `link`, `img` FROM `nightclub` WHERE `id` = '{id}';")
    name, id_rate, description, average_cost, street, worktime, numphone, link, img = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to nightclub | {left_nightclub}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_nightclub)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to nightclub | {right_nightclub}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"🕘 Время работы: {worktime}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"🕘 Время работы: {worktime}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['georgianfood'])
def georgianfood(message, id=1, previous_message=None):

    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `georgianfood`")
    pages_count_georgianfood = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_georgianfood = id - 1 if id != 1 else pages_count_georgianfood
    right_georgianfood = id + 1 if id != pages_count_georgianfood else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `id_rate`, `description`, `img`, `link`, `id_average_cost`, `numphone` FROM `georgianfood` WHERE `id` = '{id}';")
    name, street, id_rate, description, img, link, id_average_cost, numphone = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to georgianfood | {left_georgianfood}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_georgianfood)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to georgianfood | {right_georgianfood}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['italianfood'])
def italianfood(message, id=1, previous_message=None):

    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `italianfood`")
    pages_count_italianfood = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_italianfood = id - 1 if id != 1 else pages_count_italianfood
    right_italianfood = id + 1 if id != pages_count_italianfood else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `id_rate`, `description`, `img`, `link`, `numphone`, `id_average_cost` FROM `italianfood` WHERE `id` = '{id}';")
    name, street, id_rate, description, img, link, numphone, id_average_cost = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to italianfood | {left_italianfood}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_italianfood)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to italianfood | {right_italianfood}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['karaoke'])
def karaoke(message, id=1, previous_message=None):

    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `karaoke`")
    pages_count_karaoke = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_karaoke = id - 1 if id != 1 else pages_count_karaoke
    right_karaoke = id + 1 if id != pages_count_karaoke else 1

    product_query = cursor.execute(
        f"SELECT `name`, `id_rate`, `description`, `id_average_cost`, `worktime`, `street`, `numphone`, `link`, `img` FROM `karaoke` WHERE `id` = '{id}';")
    name, id_rate, description, id_average_cost, worktime, street, numphone, link, img = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to karaoke | {left_karaoke}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_karaoke)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to karaoke | {right_karaoke}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"🕘 Время работы: {worktime}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"🕘 Время работы: {worktime}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['anticafe'])
def anticafe(message, id=1, previous_message=None):

    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `anticafe_game`")
    pages_count_anticafe = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_anticafe = id - 1 if id != 1 else pages_count_anticafe
    right_anticafe = id + 1 if id != pages_count_anticafe else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `id_rate`, `description`, `img`, `link`, `numphone`, `id_average_cost` FROM `anticafe_game` WHERE `id` = '{id}';")
    name, street, id_rate, description, img, link, numphone, id_average_cost = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to anticafe | {left_anticafe}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_anticafe)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to anticafe | {right_anticafe}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"💵 Оплата: {id_average_cost}\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"💵 Оплата: {id_average_cost}\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['gameclub'])
def gameclub(message, id=1, previous_message=None):
    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `game_club`")
    pages_count_gameclub = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_gameclub = id - 1 if id != 1 else pages_count_gameclub
    right_gameclub = id + 1 if id != pages_count_gameclub else 1

    product_query = cursor.execute(
        f"SELECT `name`, `id_rate`, `link`, `numphone`, `workschedule`, `street`, `description`, `img`, `id_average_cost` FROM `game_club` WHERE `id` = '{id}';")
    name, id_rate, link, numphone, workschedule, street, description, img, id_average_cost = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to gameclub | {left_gameclub}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_gameclub)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to gameclub | {right_gameclub}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"💵 Оплата: {id_average_cost}\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"🕘 Время работы: {workschedule}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"💵 Оплата: {id_average_cost}\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"🕘 Время работы: {workschedule}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['paintball_karting'])
def paintball_karting(message, id=1, previous_message=None):
    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `paintball_karting`")
    pages_count_paintball_karting = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_paintball_karting = id - 1 if id != 1 else pages_count_paintball_karting
    right_paintball_karting = id + 1 if id != pages_count_paintball_karting else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `id_rate`, `img`, `link`, `numphone`, `id_average_cost`, `description` FROM `paintball_karting` WHERE `id` = '{id}';")
    name, street, id_rate, img, link, numphone, id_average_cost, description = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to paintball_karting | {left_paintball_karting}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_paintball_karting)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to paintball_karting | {right_paintball_karting}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"{id_average_cost}\n\n"
        msg += f"{description}"

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"{id_average_cost}\n\n"
        msg += f"{description}"

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['horseride'])
def horseride(message, id=1, previous_message=None):
    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `horseride`")
    pages_count_horseride = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_horseride = id - 1 if id != 1 else pages_count_horseride
    right_horseride = id + 1 if id != pages_count_horseride else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `id_rate`, `img`, `link`, `contacts`, `id_average_cost`, `description` FROM `horseride` WHERE `id` = '{id}';")
    name, street, id_rate, img, link, contacts, id_average_cost, description = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to horseride | {left_horseride}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_horseride)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to horseride | {right_horseride}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"⭐ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {contacts}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"💵 Средний чек: {id_average_cost}\n"
        msg += f"⭐ Рейтинг: {id_rate}\n"
        msg += f"☎️ Номер телефона: {contacts}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['lounge_bar'])
def lounge_bar(message, id=1, previous_message=None):
    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `lounge_bar`")
    pages_count_lounge_bar = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_lounge_bar = id - 1 if id != 1 else pages_count_lounge_bar
    right_lounge_bar = id + 1 if id != pages_count_lounge_bar else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `id_rate`, `description`, `img`, `link`, `id_average_cost`, `numphone` FROM `lounge_bar` WHERE `id` = '{id}';")
    name, street, id_rate, description, img, link, id_average_cost, numphone = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to lounge_bar | {left_lounge_bar}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_lounge_bar)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to lounge_bar | {right_lounge_bar}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['pool'])
def pool(message, id=1, previous_message=None):
    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `pool`")
    pages_count_pool = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_pool = id - 1 if id != 1 else pages_count_pool
    right_pool = id + 1 if id != pages_count_pool else 1

    product_query = cursor.execute(
        f"SELECT `name`, `id_rate`, `numphone`, `street`, `workschedule`, `id_average_cost`, `link`, `description`, `img` FROM `pool` WHERE `id` = '{id}';")
    name, id_rate, numphone, street, workschedule, id_average_cost, link, description, img = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to pool | {left_pool}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_pool)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to pool | {right_pool}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"🕘 Время работы: {workschedule}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"🕘 Время работы: {workschedule}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['kvizi'])
def kvizi(message, id=1, previous_message=None):
    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `kvizi`")
    pages_count_kvizi = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_kvizi = id - 1 if id != 1 else pages_count_kvizi
    right_kvizi = id + 1 if id != pages_count_kvizi else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `descript`, `numphone`, `img`, `id_average_cost` FROM `kvizi` WHERE `id` = '{id}';")
    name, street, descript, numphone, img, id_average_cost = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to kvizi | {left_kvizi}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_kvizi)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to kvizi | {right_kvizi}')
    street_button = types.InlineKeyboardButton("Ссылка", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"💵 Оплата: {id_average_cost}\n\n"
        msg += f"{descript}" if descript != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"☎️ Номер телефона: {numphone}\n"
        msg += f"💵 Оплата: {id_average_cost}\n\n"
        msg += f"{descript}" if descript != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons)

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['bar_pub'])
def bar_pub(message, id=1, previous_message=None):
    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `bar_pub`")
    pages_count_bar_pub = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_bar_pub = id - 1 if id != 1 else pages_count_bar_pub
    right_bar_pub = id + 1 if id != pages_count_bar_pub else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `id_rate`, `description`, `img`, `link`, `id_average_cost`, `numphone` FROM `bar_pub` WHERE `id` = '{id}';")
    name, street, id_rate, description, img, link, id_average_cost, numphone = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to bar_pub | {left_bar_pub}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_bar_pub)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to bar_pub | {right_bar_pub}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{description}" if description != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['table_games'])
def table_games(message, id=1, previous_message=None):
    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `table_games`")
    pages_count_table_games = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_table_games = id - 1 if id != 1 else pages_count_table_games
    right_table_games = id + 1 if id != pages_count_table_games else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `descript`, `link`, `numphone`, `img`, `id_rate`, `id_average_cost` FROM `table_games` WHERE `id` = '{id}';")
    name, street, descript, link, numphone, img, id_rate, id_average_cost = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to table_games | {left_table_games}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_table_games)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to table_games | {right_table_games}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{descript}" if descript != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')
    except:
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{descript}" if descript != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass

@bot.message_handler(commands=['pastry_shops'])
def pastry_shops(message, id=1, previous_message=None):
    connect = sqlite3.connect("dada_db.db")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `pastry_shops`")
    pages_count_pastry_shops = int(pages_count_query.fetchone()[0])
    buttons = types.InlineKeyboardMarkup()

    left_pastry_shops = id - 1 if id != 1 else pages_count_pastry_shops
    right_pastry_shops = id + 1 if id != pages_count_pastry_shops else 1

    product_query = cursor.execute(
        f"SELECT `name`, `street`, `descript`, `link`, `numphone`, `img`, `id_rate`, `id_average_cost` FROM `pastry_shops` WHERE `id` = '{id}';")
    name, street, descript, link, numphone, img, id_rate, id_average_cost = product_query.fetchone()

    left_button = types.InlineKeyboardButton("←", callback_data=f'to pastry_shops | {left_pastry_shops}')
    page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_pastry_shops)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to pastry_shops | {right_pastry_shops}')
    link_button = types.InlineKeyboardButton("Сайт", url=link, callback_data='buy')
    street_button = types.InlineKeyboardButton("Я.Карты", url=street, callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(link_button, street_button)

    cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
    connect.commit()

    try:
        try:
            photo = open(img, 'rb')
        except:
            photo = img
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{descript}" if descript != None else '_нет_'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')

    except:
        msg = f"*{name}*\n\n"
        msg += f"⭐️ Рейтинг: {id_rate}\n"
        msg += f"💵 Средний чек: {id_average_cost}₽\n"
        msg += f"☎️ Номер телефона: {numphone}\n\n"
        msg += f"{descript}" if descript != None else '_нет_'

        bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass
# Обзорные места

@bot.message_handler(commands=['route_1'])
def route_1(message, id=1, previous_message=None):

    if user_state.get(message.chat.id) == 'pressed':

        connect = sqlite3.connect("dada_db.db")
        cursor = connect.cursor()

        pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `route_1`")
        pages_count_route_1 = int(pages_count_query.fetchone()[0])
        buttons = types.InlineKeyboardMarkup()

        left_route_1 = id - 1 if id != 1 else pages_count_route_1
        right_route_1 = id + 1 if id != pages_count_route_1 else 1

        product_query = cursor.execute(
            f"SELECT `description`, `link`, `name` FROM `route_1` WHERE `id` = '{id}';")
        description, link, name = product_query.fetchone()

        left_button = types.InlineKeyboardButton("←", callback_data=f'to route_1 | {left_route_1}')
        page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_route_1)}", callback_data='_')
        right_button = types.InlineKeyboardButton("→", callback_data=f'to route_1 | {right_route_1}')
        buttons.add(left_button, page_button, right_button)

        cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
        connect.commit()

        try:
            try:
                photo = open(link, 'rb')
            except:
                photo = link
            msg = f"*{name}*\n\n"
            msg += f"{description}" if description != None else '_нет_'

            bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')

        except:
            msg = f"*{name}*\n\n"
            msg += f"{description}" if description != None else '_нет_'

            bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

        try:
            bot.delete_message(message.chat.id, previous_message.id)
        except:
            pass

    else:
        bot.send_message(message.chat.id, 'Вы не оплатили подписку ❌')

@bot.message_handler(commands=['route_2'])
def route_2(message, id=1, previous_message=None):

    if user_state.get(message.chat.id) == 'pressed':

        connect = sqlite3.connect("dada_db.db")
        cursor = connect.cursor()

        pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `route_2`")
        pages_count_route_2 = int(pages_count_query.fetchone()[0])
        buttons = types.InlineKeyboardMarkup()

        left_route_2 = id - 1 if id != 1 else pages_count_route_2
        right_route_2 = id + 1 if id != pages_count_route_2 else 1

        product_query = cursor.execute(
            f"SELECT `name`, `description`, `img` FROM `route_2` WHERE `id` = '{id}';")
        name, description, img = product_query.fetchone()

        left_button = types.InlineKeyboardButton("←", callback_data=f'to route_2 | {left_route_2}')
        page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_route_2)}", callback_data='_')
        right_button = types.InlineKeyboardButton("→", callback_data=f'to route_2 | {right_route_2}')
        buttons.add(left_button, page_button, right_button)

        cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
        connect.commit()

        try:
            try:
                photo = open(img, 'rb')
            except:
                photo = img
            msg = f"*{name}*\n\n"
            msg += f"{description}" if description != None else '_нет_'

            bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')

        except:
            msg = f"*{name}*\n\n"
            msg += f"{description}" if description != None else '_нет_'

            bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

        try:
            bot.delete_message(message.chat.id, previous_message.id)
        except:
            pass

    else:
        bot.send_message(message.chat.id, 'Вы не оплатили подписку ❌')

@bot.message_handler(commands=['route_3'])
def route_3(message, id=1, previous_message=None):

    if user_state.get(message.chat.id) == 'pressed':

        connect = sqlite3.connect("dada_db.db")
        cursor = connect.cursor()

        pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `route_3`")
        pages_count_route_3 = int(pages_count_query.fetchone()[0])
        buttons = types.InlineKeyboardMarkup()

        left_route_3 = id - 1 if id != 1 else pages_count_route_3
        right_route_3 = id + 1 if id != pages_count_route_3 else 1

        product_query = cursor.execute(
            f"SELECT `name`, `description`, `img` FROM `route_3` WHERE `id` = '{id}';")
        name, description, img = product_query.fetchone()

        left_button = types.InlineKeyboardButton("←", callback_data=f'to route_3 | {left_route_3}')
        page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_route_3)}", callback_data='_')
        right_button = types.InlineKeyboardButton("→", callback_data=f'to route_3 | {right_route_3}')
        buttons.add(left_button, page_button, right_button)

        cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
        connect.commit()

        try:
            try:
                photo = open(img, 'rb')
            except:
                photo = img
            msg = f"*{name}*\n\n"
            msg += f"{description}" if description != None else '_нет_'

            bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')

        except:
            msg = f"*{name}*\n\n"
            msg += f"{description}" if description != None else '_нет_'

            bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

        try:
            bot.delete_message(message.chat.id, previous_message.id)
        except:
            pass

    else:
        bot.send_message(message.chat.id, 'Вы не оплатили подписку ❌')

@bot.message_handler(commands=['foto_1'])
def foto_1(message, id=1, previous_message=None):

    if user_state.get(message.chat.id) == 'pressed':

        connect = sqlite3.connect("dada_db.db")
        cursor = connect.cursor()

        pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `foto_1`")
        pages_count_foto_1 = int(pages_count_query.fetchone()[0])
        buttons = types.InlineKeyboardMarkup()

        left_foto_1 = id - 1 if id != 1 else pages_count_foto_1
        right_foto_1 = id + 1 if id != pages_count_foto_1 else 1

        product_query = cursor.execute(
            f"SELECT `name`, `what`, `id_average_cost`, `id_rate`, `numphone`, `description`, `img` FROM `foto_1` WHERE `id` = '{id}';")
        name, what, id_average_cost, id_rate, numphone, description, img = product_query.fetchone()

        left_button = types.InlineKeyboardButton("←", callback_data=f'to foto_1 | {left_foto_1}')
        page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_foto_1)}", callback_data='_')
        right_button = types.InlineKeyboardButton("→", callback_data=f'to foto_1 | {right_foto_1}')
        buttons.add(left_button, page_button, right_button)

        cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
        connect.commit()

        try:
            try:
                photo = open(img, 'rb')
            except:
                photo = img
            msg = f"*{name}*\n\n"
            msg += f"{what}\n" if what != None else None

            bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')

        except:
            msg = f"*{name}*\n\n"
            msg += f"{what}\n" if what != None else None

            bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

        try:
            bot.delete_message(message.chat.id, previous_message.id)
        except:
            pass

    else:
        bot.send_message(message.chat.id, 'Вы не оплатили подписку ❌')

@bot.message_handler(commands=['foto_2'])
def foto_2(message, id=1, previous_message=None):

    if user_state.get(message.chat.id) == 'pressed':

        connect = sqlite3.connect("dada_db.db")
        cursor = connect.cursor()

        pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `foto_2`")
        pages_count_foto_2 = int(pages_count_query.fetchone()[0])
        buttons = types.InlineKeyboardMarkup()

        left_foto_2 = id - 1 if id != 1 else pages_count_foto_2
        right_foto_2 = id + 1 if id != pages_count_foto_2 else 1

        product_query = cursor.execute(
            f"SELECT `name`, `what`, `id_average_cost`, `id_rate`, `numphone`, `description`, `img` FROM `foto_2` WHERE `id` = '{id}';")
        name, what, id_average_cost, id_rate, numphone, description, img = product_query.fetchone()

        left_button = types.InlineKeyboardButton("←", callback_data=f'to foto_2 | {left_foto_2}')
        page_button = types.InlineKeyboardButton(f"{str(id)}/{str(pages_count_foto_2)}", callback_data='_')
        right_button = types.InlineKeyboardButton("→", callback_data=f'to foto_2 | {right_foto_2}')
        buttons.add(left_button, page_button, right_button)

        cursor.execute(f"UPDATE `users` SET `id` = {id} WHERE `users`.`id` = {message.chat.id};")
        connect.commit()

        try:
            try:
                photo = open(img, 'rb')
            except:
                photo = img
            msg = f"*{name}*\n\n"
            msg += f"{what}\n" if what != None else None

            bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons, parse_mode='Markdown')

        except:
            msg = f"*{name}*\n\n"
            msg += f"{what}\n" if what != None else None

            bot.send_message(message.chat.id, msg, reply_markup=buttons, parse_mode='Markdown')

        try:
            bot.delete_message(message.chat.id, previous_message.id)
        except:
            pass

    else:
        bot.send_message(message.chat.id, 'Вы не оплатили подписку ❌')

# Обработчик callback

@bot.callback_query_handler(func=lambda c: True)
def callback_query(call):

    try:
        if 'to' in call.data:
            id = int(call.data.split('|')[-1])

            if "canteen" in call.data:
                canteen(call.message, id, call.message)

            elif "asianfood" in call.data:
                asianfood(call.message, id, call.message)

            elif "fastfood" in call.data:
                fastfood(call.message, id, call.message)

            elif "slavicfood" in call.data:
                slavicfood(call.message, id, call.message)

            elif "seafood" in call.data:
                seafood(call.message, id, call.message)

            elif "questroom" in call.data:
                questroom(call.message, id, call.message)

            elif "nightclub" in call.data:
                nightclub(call.message, id, call.message)

            elif "italianfood" in call.data:
                italianfood(call.message, id, call.message)

            elif "georgianfood" in call.data:
                georgianfood(call.message, id, call.message)

            elif "karaoke" in call.data:
                karaoke(call.message, id, call.message)

            elif "anticafe" in call.data:
                anticafe(call.message, id, call.message)

            elif "gameclub" in call.data:
                gameclub(call.message, id, call.message)

            elif "paintball_karting" in call.data:
                paintball_karting(call.message, id, call.message)

            elif "horseride" in call.data:
                horseride(call.message, id, call.message)

            elif "lounge_bar" in call.data:
                lounge_bar(call.message, id, call.message)

            elif "pool" in call.data:
                pool(call.message, id, call.message)

            elif "kvizi" in call.data:
                kvizi(call.message, id, call.message)

            elif "bar_pub" in call.data:
                bar_pub(call.message, id, call.message)

            elif "table_games" in call.data:
                table_games(call.message, id, call.message)

            elif "pastry_shops" in call.data:
                pastry_shops(call.message, id, call.message)

            elif "route_1" in call.data:
                route_1(call.message, id, call.message)

            elif "route_2" in call.data:
                route_2(call.message, id, call.message)

            elif "route_3" in call.data:
                route_3(call.message, id, call.message)

            elif "foto_1" in call.data:
                foto_1(call.message, id, call.message)

            elif "foto_2" in call.data:
                foto_2(call.message, id, call.message)

        elif call.message:

            if call.data == '1_month':

                markup = types.InlineKeyboardMarkup(row_width=1)

                instagramm = types.InlineKeyboardButton("Ссылка на оплату", url='https://www.tinkoff.ru/',
                                                    callback_data='oplata')
                sales = types.InlineKeyboardButton("Я оплатил ✅", callback_data='pay')

                markup.add(instagramm, sales)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Чтобы получить доступ к платным предложениям на 1 месяц, оплатите чек по ссылке и нажмите кнопку "Я оплатил ✅"',
                                  reply_markup=markup)

            elif call.data == '6_month':

                markup = types.InlineKeyboardMarkup(row_width=1)

                instagramm = types.InlineKeyboardButton("Ссылка на оплату", url='https://www.tinkoff.ru/',
                                                    callback_data='oplata')
                sales = types.InlineKeyboardButton("Я оплатил ✅", callback_data='pay')

                markup.add(instagramm, sales)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Чтобы получить доступ к платным предложениям на 6 месяцев, оплатите чек по ссылке и нажмите кнопку "Я оплатил ✅"',
                                  reply_markup=markup)

            elif call.data == '12_month':

                markup = types.InlineKeyboardMarkup(row_width=1)

                instagramm = types.InlineKeyboardButton("Ссылка на оплату", url='https://www.tinkoff.ru/',
                                                    callback_data='oplata')
                sales = types.InlineKeyboardButton("Я оплатил ✅", callback_data='pay')

                markup.add(instagramm, sales)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Чтобы получить доступ к платным предложениям на 12 месяцев, оплатите чек по ссылке и нажмите кнопку "Я оплатил ✅"',
                                  reply_markup=markup)

            elif call.data == 'pay':

                user_state[call.message.chat.id] = 'pressed'

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                eat = types.KeyboardButton("Где поесть? 🍜")
                time = types.KeyboardButton("Как провести время? 👀")
                pay = types.KeyboardButton("Платные предложения 💵")

                markup.add(eat, time, pay)

                bot.send_message(call.message.chat.id, 'Поздравляем!\n\n'
                                                   'Вы поддержали наш проект, и теперь у Вас есть доступ к платному контенту.', reply_markup=markup)

                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    except Exception as e:
        print(repr(e))

@bot.message_handler(commands=['about'])

def about(message):

    bot.send_message(message.chat.id, "Мы - команда Т23ОН-01, разработали этого бота для итогового проекта по модулю «Основы экономики и бизнеса». Над ним работали лучшие умы и программисты всего университета. Надеемся, что он Вам понравится:)\n\n"
                                      "Структура бота была сделана с нуля при помощи языков программирования Python и базы данных Sqlite3, а также с ипользованием библиотеки pyTelegramBotAPI\n\n"
                                      "Технический администратор, по всем вопросам: @kxwarvta")

    # bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(open('photo_bot/volgograd.jpg', 'rb'))])

@bot.message_handler(content_types=['text'])

def lalala(message):

    if message.chat.type == 'private':

        #ветка "Где поесть?"

        if message.text == 'Где поесть? 🍜':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            kitchen_selection = types.KeyboardButton("Выбор кухни 🤔")
            popular_establishments = types.KeyboardButton("Популярные заведения 🔝")
            establishments_nearby = types.KeyboardButton("Заведения рядом 📍")
            back = types.KeyboardButton("Назад 🔙")

            markup.add(kitchen_selection, popular_establishments, establishments_nearby, back)

            bot.send_message(message.chat.id, 'Выберите место:', reply_markup=markup)

        #дочерние кнопки "Где поесть?"

        elif message.text == 'Выбор кухни 🤔':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

            seafood = types.KeyboardButton("Морская 🦐")
            asianfood = types.KeyboardButton("Азиатская 🍣")
            georgianfood = types.KeyboardButton("Грузинская 🥙")
            italianfood = types.KeyboardButton("Итальянская 🍕")
            slavicfood = types.KeyboardButton("Славянская 🥘")
            fastfood = types.KeyboardButton("Фастфуды 🍔")
            pastry_shops = types.KeyboardButton("Кондитерские 🍬")
            bar_pub = types.KeyboardButton("Бары и пабы 🍸")
            canteen = types.KeyboardButton("Столовые 🍲")
            back = types.KeyboardButton("Назад 🔙")

            markup.add(seafood, asianfood, georgianfood, italianfood, slavicfood, fastfood, bar_pub, canteen)
            markup.add(pastry_shops, back)

            bot.send_message(message.chat.id, 'Выберите кухню:', reply_markup=markup)

        elif message.text == 'Популярные заведения 🔝':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            niche_harcho = types.KeyboardButton("Ничё Харчо!")
            erti = types.KeyboardButton("Эрти")
            magadan = types.KeyboardButton("Магадан")
            sumo_sam = types.KeyboardButton("Sumo Sam")
            cow = types.KeyboardButton("Корова")
            cheese_factory = types.KeyboardButton("Сыроварня")
            back = types.KeyboardButton("Назад 🔙")

            markup.add(niche_harcho, erti, magadan, sumo_sam, cow, cheese_factory, back)

            bot.send_message(message.chat.id, 'Популярные заведения 🔝', reply_markup=markup)

        elif message.text == 'Заведения рядом 📍':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

            location = types.KeyboardButton("Показать заведения рядом", request_location=True)
            back = types.KeyboardButton("Назад 🔙")

            markup.add(location, back)

            bot.send_message(message.chat.id, "Вы отправили месторасположение", reply_markup=markup)

        #ветка "Как провести время?"

        elif message.text == 'Как провести время? 👀':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            chill = types.KeyboardButton("Расслабиться 😮‍💨")
            view_the_city = types.KeyboardButton("Посмотреть город 👀")
            benefit = types.KeyboardButton("Отдохнуть с пользой ☺️")
            back = types.KeyboardButton("Назад 🔙")

            markup.add(chill, view_the_city, benefit, back)

            bot.send_message(message.chat.id, 'Выберите место, где Вы хотите провести время:\n', reply_markup=markup)

        #дочерние кнопки "Как провести время?"

        elif message.text == 'Расслабиться 😮‍💨':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            hookah = types.KeyboardButton("Кальянные 😶‍🌫️")
            anticafe = types.KeyboardButton("Анти-кафе 🥴")
            nightclub = types.KeyboardButton("Ночные клубы 🍓")
            karaoke = types.KeyboardButton("Караоке 🎤")
            back = types.KeyboardButton("Назад 🔙")

            markup.add(hookah, anticafe, nightclub, karaoke, back)

            bot.send_message(message.chat.id, "Выберите место, где Вы хотите расслабиться:", reply_markup=markup)

        elif message.text == 'Посмотреть город 👀':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item43 = types.KeyboardButton("1️⃣ Маршрут")
            item44 = types.KeyboardButton("2️⃣ Маршрут")
            item45 = types.KeyboardButton("3️⃣ Маршрут")
            back = types.KeyboardButton("Назад 🔙")

            markup.add(item43, item44, item45, back)

            bot.send_message(message.chat.id, "Выберите место, где Вы хотите погулять:", reply_markup=markup)

        #Ветка "Отдохнуть с пользой"

        elif message.text == 'Отдохнуть с пользой ☺️':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            physical_activities = types.KeyboardButton("Физические активности 💪")
            passive_activities = types.KeyboardButton("Пассивные активности 😉")
            back = types.KeyboardButton("Назад 🔙")

            markup.add(physical_activities, passive_activities, back)

            bot.send_message(message.chat.id, "Выберите место, где Вы хотите отдохнуть с пользой:", reply_markup=markup)

        #Дочерние кнопки "Отдохнуть с пользой"

        elif message.text == 'Физические активности 💪':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            billiards_bowling = types.KeyboardButton("Бильярд, боулинг 🎳")
            questroom = types.KeyboardButton("Квесты 👣")
            horseride = types.KeyboardButton("Конные прогулки 🐴")
            paintball_karting = types.KeyboardButton("Пейнтбол, картинг 🏎")
            back = types.KeyboardButton("Назад 🔙")

            markup.add(billiards_bowling, questroom, horseride, paintball_karting, back)

            bot.send_message(message.chat.id, 'Выберите место:', reply_markup=markup)

        elif message.text == 'Пассивные активности 😉':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            gameclub = types.KeyboardButton("Компьютерные клубы 🖥")
            dekstop = types.KeyboardButton("Настольные игры 🃏")
            quizzes = types.KeyboardButton("Квизы ❔")
            back = types.KeyboardButton("Назад 🔙")

            markup.add(gameclub)
            markup.add(dekstop, quizzes)
            markup.add(back)

            bot.send_message(message.chat.id, 'Выберите место:', reply_markup=markup)

        #back button

        elif message.text == 'Назад 🔙':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            food = types.KeyboardButton("Где поесть? 🍜")
            spend_time = types.KeyboardButton("Как провести время? 👀")
            pay = types.KeyboardButton("Платные предложения 💸")

            markup.add(food, spend_time, pay)

            bot.send_message(message.chat.id, 'Главное меню 🏚', reply_markup=markup)

        elif message.text == 'Назад ◀️':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            food = types.KeyboardButton("Где поесть? 🍜")
            spend_time = types.KeyboardButton("Как провести время? 👀")
            pay = types.KeyboardButton("Платные предложения 💵")

            markup.add(food, spend_time, pay)

            bot.send_message(message.chat.id, 'Главное меню 🏚', reply_markup=markup)

        #back button "Маршрут по барам"

        elif message.text == 'Назад к маршрутам 🔙':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

            lite_version = types.KeyboardButton("Lite версия")
            middle_version = types.KeyboardButton("Middle версия")
            hard_version = types.KeyboardButton("Hard версия")
            back = types.KeyboardButton("Назад 🔙")

            markup.add(lite_version, middle_version, hard_version, back)

            bot.send_message(message.chat.id, 'Маршрут по барам', reply_markup=markup)

        # back button "Маршрут по барам" после оплаты

        elif message.text == 'Назад к маршрутам ◀️':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

            lite_version = types.KeyboardButton("Lite версия")
            middle_version = types.KeyboardButton("Middle версия")
            hard_version = types.KeyboardButton("Hard версия")
            back = types.KeyboardButton("Назад ◀️")

            markup.add(lite_version, middle_version, hard_version, back)

            bot.send_message(message.chat.id, 'Маршрут по барам', reply_markup=markup)

        #выбор кухни

        elif message.text == 'Азиатская 🍣':

            bot.send_message(message.chat.id, 'Чтобы посмотреть заведения с азиатской кухней, нажмите на /asianfood')

        elif message.text == 'Столовые 🍲':

            bot.send_message(message.chat.id, 'Чтобы посмотреть столовые, нажмите на /canteen')

        elif message.text == 'Фастфуды 🍔':

            bot.send_message(message.chat.id, 'Чтобы посмотреть заведения с фастфудом, нажмите /fastfood')

        elif message.text == 'Славянская 🥘':

            bot.send_message(message.chat.id, 'Чтобы посмотреть заведения со славянской кухней, нажмите на /slavicfood')

        elif message.text == 'Морская 🦐':

            bot.send_message(message.chat.id, 'Чтобы посмотреть заведения с морской кухней, нажмите на /seafood')

        elif message.text == 'Квесты 👣':

            bot.send_message(message.chat.id, 'Чтобы посмотреть квизы, нажмите /questroom')

        elif message.text == 'Ночные клубы 🍓':

            bot.send_message(message.chat.id, 'Чтобы посмотреть ночные клубы, нажмите на /nightclub')

        elif message.text == 'Итальянская 🍕':

            bot.send_message(message.chat.id, 'Чтобы посмотреть заведения с итальянской кухней, нажмите на /italianfood')

        elif message.text == 'Грузинская 🥙':

            bot.send_message(message.chat.id, 'Чтобы посмотреть заведения с грузинской кухней, нажмите на /georgianfood')

        elif message.text == 'Караоке 🎤':

            bot.send_message(message.chat.id, 'Чтобы посмотреть места с караоке, нажмите на /karaoke')

        elif message.text == 'Анти-кафе 🥴':

            bot.send_message(message.chat.id, 'Чтобы посмотреть анти-кафе, нажмите на /anticafe')

        elif message.text == 'Компьютерные клубы 🖥':

            bot.send_message(message.chat.id, 'Чтобы посмотреть компьютерные клубы, нажмите на /gameclub')

        elif message.text == 'Пейнтбол, картинг 🏎':

            bot.send_message(message.chat.id, 'Чтобы посмотреть места с пейнтболом и картингом, нажмите на /paintball_karting')

        elif message.text == 'Конные прогулки 🐴':

            bot.send_message(message.chat.id, 'Чтобы прогуляться на конях, нажмите на /horseride')

        elif message.text == 'Кальянные 😶‍🌫️':

            bot.send_message(message.chat.id, 'Чтобы посмотреть кальянные, нажмите на /lounge_bar')

        elif message.text == 'Бильярд, боулинг 🎳':

            bot.send_message(message.chat.id, 'Чтобы поиграть в бильярд или боулинг, нажмите на /pool')

        elif message.text == 'Квизы ❔':

            bot.send_message(message.chat.id, 'Чтобы поиграть в квизы, нажмите на /kvizi')

        elif message.text == 'Бары и пабы 🍸':

            bot.send_message(message.chat.id, 'Чтобы сходить в бары или пабы, нажмите на /bar_pub')

        elif message.text == 'Настольные игры 🃏':

            bot.send_message(message.chat.id, 'Чтобы поиграть в настольные игры, нажмите на /table_games')

        elif message.text == 'Кондитерские 🍬':

            bot.send_message(message.chat.id, 'Чтобы посмотреть кондитерские, нажмите на /pastry_shops')

        elif message.text == '1️⃣ Маршрут':

            bot.send_message(message.chat.id, 'Чтобы посмотреть первый маршрут, нажмите на /route_1')

        elif message.text == '2️⃣ Маршрут':

            bot.send_message(message.chat.id, 'Чтобы посмотреть второй маршрут, нажмите на /route_2')

        elif message.text == '3️⃣ Маршрут':

            bot.send_message(message.chat.id, 'Чтобы посмотреть третий маршрут, нажмите на /route_3')

        elif message.text == 'Маршрут 1️⃣':

            bot.send_message(message.chat.id, 'Чтобы посмотреть первый инстамаршрут, нажмите на /foto_1')

        elif message.text == 'Маршрут 2️⃣':

            bot.send_message(message.chat.id, 'Чтобы посмотреть второй инстамаршрут, нажмите на /foto_2')

        #популярные заведения:

        elif message.text == 'Магадан':

            markup = types.InlineKeyboardMarkup(row_width=2)

            vk = types.InlineKeyboardButton("VK", url='https://vk.com/magadanrnd', callback_data='vkvk')
            site = types.InlineKeyboardButton("Ссылка на сайт", url='https://magadanrnd.ru', callback_data='m')
            ya_maps = types.InlineKeyboardButton("Ссылка на Я.Карты", url='https://yandex.ru/maps/org/magadan/231267455827/?ll=39.752415%2C47.240329&z=12.96', callback_data='p')

            photo = open('photo_bot/magadan.png', 'rb')

            markup.add(site, ya_maps, vk)

            text = "*Магадан*\n\n"\
                   "🍽️ Ресторан европейской кухни\n" \
                   "💵 Средний чек: 2400 ₽\n"\
                   "⭐️ Рейтинг: 4.8\n" \
                   "☎️ Номер телефона: +7 (928) 111-18-77\n\n"\
                   "Меню ресторана включает: магаданские крабы и креветки, сахалинские морские ежи и гребешки, черноморская барабуля и рапаны и многое другое! Качество блюд и индивидуальный подход к каждому клиенту вас приятно удивят!"

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')

        elif message.text == 'Ничё Харчо!':

            markup = types.InlineKeyboardMarkup(row_width=2)

            ya_maps = types.InlineKeyboardButton("Ссылка на Я.Карты", url='https://yandex.ru/maps/-/CCU0VSrVCD', callback='d')

            photo = open('photo_bot/niche.jpg', 'rb')

            markup.add(ya_maps)

            text = "*Ничё Харчо!*\n\n"\
                   "🍽️ Грузинская закусочная\n" \
                   "💵 Средний чек: 400 ₽\n"\
                   "⭐️ Рейтинг: 4.3\n" \
                   "☎️ Номер телефона: +7 (950) 853-21-98\n\n" \
                   "Меню бистро включает: хинкали, хачапури, пхали, чебуреки, пури, супы и многое другое! Любимые блюда по доступным ценам, красивый интерьер, кавказское гостеприимство и удобное расположение в центре вас не оставят равнодушным!"

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')

        elif message.text == 'Эрти':

            markup = types.InlineKeyboardMarkup(row_width=2)

            ya_maps = types.InlineKeyboardButton("Ссылка на Я.Карты", url='https://yandex.ru/maps/-/CCU0V0G8lC', callback_data='u')
            site = types.InlineKeyboardButton("Ссылка на сайт", url='https://ertirestaurant.ru/', callback_data='t')
            social = types.InlineKeyboardButton("Соцсети", url='https://t.me/ertirest', callback_data='tg')
            menu = types.InlineKeyboardButton("Меню", url='https://drive.google.com/file/d/1IcGjqxN1icVnVem2dgBGU9i2vTfawgsC/preview')

            photo = open('photo_bot/erti.jpg', 'rb')

            markup.add(ya_maps, social, menu, site)

            text = "*Эрти*\n\n" \
                   "🍽️ Ресторан грузинской кухни\n" \
                   "💵 Средний чек: 1300 ₽\n" \
                   "⭐️ Рейтинг: 5.0\n" \
                   "☎️ Номер телефона: +7 (938) 158-58-58\n\n" \
                   "Эрти - это место, где сочетаются древние грузинские традиции и свежие веяния современности. Интерьер заведения сочетает в себе стильный лофт и колоритную этнику. Здесь есть все, чтобы перенести вас в живописные просторы Грузии: аджапсандал, чаквавили, хачапури, хенкали и многое другое!"

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')

        elif message.text == 'Sumo Sam':

            markup = types.InlineKeyboardMarkup(row_width=1)

            ya_maps1 = types.InlineKeyboardButton('Ссылка на Я.Карты', url='https://clck.ru/34ciWP', callback_data='qwe')

            photo = open('photo_bot/sumasam.jpg', 'rb')

            markup.add(ya_maps1)

            text = "*Sumo Sam*\n\n" \
                   "🍽️ Азиатское бистро\n" \
                   "💵 Средний чек: 600 ₽\n" \
                   "⭐️ Рейтинг: 4.4\n" \
                   "☎️ Номер телефона: +7 (918) 594-43-55\n\n" \
                   "Sumo Sam - азиатское бистро в центре города. Здесь вы сможете насладиться такими блюдами азиатской кухни, как: суширито, том ям, поке, вагаси моти и др. А приветливый персонал и стильный интерьер создадут для вас атмосферу уюта."

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')

        elif message.text == 'Корова':

            markup = types.InlineKeyboardMarkup(row_width=2)

            ya_maps = types.InlineKeyboardButton('Ссылка на Я.Карты', url='https://yandex.ru/maps/-/CCU0V0h61A', callback_data='qwgse')
            site = types.InlineKeyboardButton('Ссылка на сайт', url='https://cowbar.ru/', callback_data='dlssfddddgl')
            menu = types.InlineKeyboardButton('Меню', url='https://drive.google.com/file/d/1Bzf35QlAfTdgvxLV6tcdg6dMQCC6wtgi/view')

            photo = open('photo_bot/cow.jpg', 'rb')

            markup.add(ya_maps, menu, site)

            text = "*Cow Bar & Restaurant | Ресторан Корова*\n\n" \
                   "🍽️ Стейк-хаус\n" \
                   "💵 Средний чек: 2300 ₽\n" \
                   "⭐️ Рейтинг: 5.0\n" \
                   "☎️ Номер телефона: +7 (863) 221-12-95\n\n" \
                   "Ресторан с мясом на открытом огне и собственной коптильней. Его меню включает: стейки, бургеры, крылышки, ребра и другие мясные деликатесы. Внимательный персонал, стильный интерьер, быстрая подача, разнообразный ассортимент блюд и напитков - все это благоприятствует получению только положительных эмоций!"

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')

        elif message.text == 'Сыроварня':

            markup = types.InlineKeyboardMarkup(row_width=2)

            ya_maps = types.InlineKeyboardButton('Ссылка на Я.Карты', url='https://yandex.ru/maps/org/syrovarnya/208795372921/?ll=39.733397%2C47.225571&z=16.75', callback_data='qdsgwe')
            site = types.InlineKeyboardButton('Ссылка на сайт', url='https://www.syrovarnya.com/syrovarnya-rostov-na-donu', callback_data='dlsdgdsl')
            menu = types.InlineKeyboardButton('Меню', url='https://www.novikovgroup.ru/upload/iblock/eed/31k4krp2lw67eddxi1tinbe09u0x2lew.pdf')

            photo = open('photo_bot/sirovarnya.jpg', 'rb')

            markup.add(ya_maps, menu, site)

            text = "*Сыроварня*\n\n" \
                   "🍽️ Ресторан итальянской кухни\n" \
                   "💵 Средний чек: 2000 ₽\n" \
                   "⭐️ Рейтинг: 5.0\n" \
                   "☎️ Номер телефона: +7 (988) 549-37-64\n\n" \
                   "Это семейный ресторан, с домашней итальянской кухней, приятной атмосферой и душевным сервисом. Меню построено в основном на сырах собственного производства, за процессом создания которых вы сможете понаблюдать. Локация, интерьер, персонал, блюда - все на высшем уровне!"

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')

        #маршрут по барам

        elif message.text == 'Маршрут по барам 🍹🚶':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

            lite_version = types.KeyboardButton('Lite версия')
            middle_version = types.KeyboardButton('Middle версия')
            hard_version = types.KeyboardButton('Hard версия')
            back = types.KeyboardButton('Назад ◀️')

            markup.add(lite_version, middle_version, hard_version, back)

            bot.send_message(message.chat.id, 'Выберите желаемый уровень веселья😜:', reply_markup=markup)

        elif message.text == 'Lite версия':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

            L_eco = types.KeyboardButton('Lite\n💸')
            L_middle = types.KeyboardButton('Lite\n💸💸')
            L_premium = types.KeyboardButton('Lite\n💸💸💸')
            back = types.KeyboardButton('Назад к маршрутам ◀️')

            markup.add(L_eco, L_middle, L_premium, back)

            bot.send_message(message.chat.id, 'Выберите Ваш ценовой сегмент:', reply_markup=markup)

        elif message.text == 'Middle версия':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

            M_eco = types.KeyboardButton('Middle\n💸')
            M_middle = types.KeyboardButton('Middle\n💸💸')
            M_premium = types.KeyboardButton('Middle\n💸💸💸')
            back = types.KeyboardButton('Назад к маршрутам ◀️')

            markup.add(M_eco, M_middle, M_premium, back)

            bot.send_message(message.chat.id, 'Выберите Ваш ценовой сегмент:', reply_markup=markup)

        elif message.text == 'Hard версия':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

            H_eco = types.KeyboardButton('Hard\n💸')
            H_middle = types.KeyboardButton('Hard\n💸💸')
            H_premium = types.KeyboardButton('Hard\n💸💸💸')
            back = types.KeyboardButton('Назад к маршрутам ◀️')

            markup.add(H_eco, H_middle, H_premium, back)

            bot.send_message(message.chat.id, 'Выберите Ваш ценовой сегмент:', reply_markup=markup)

        elif message.text == 'Lite\n💸':

            markup = types.InlineKeyboardMarkup(row_width=1)

            ya_maps = types.InlineKeyboardButton('Ссылка на маршрут в Я.Картах', url='https://clck.ru/34ZPhF', callback_data='qdsgwe')

            photo = open('photo_bot/wine.jpg', 'rb')

            markup.add(ya_maps)

            text = "1️⃣ *Abbey Road Pub*\n" \
                   "🍽️ Английский Паб\n" \
                   "⭐️ Рейтинг: 4,7\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Пиво Corona - 250₽\n" \
                   "◻️ Биттер Aperol - 225₽\n\n" \
                   "2️⃣ *Багдад mint*\n" \
                   "🍽️ Кальян-бар\n" \
                   "⭐️ Рейтинг: 4,4\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Палома - 440₽\n" \
                   "◻️ Девушка из высшего общества - 380₽"

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')
            bot.delete_message(message.chat.id, message.message_id)

        elif message.text == 'Lite\n💸💸':

            markup = types.InlineKeyboardMarkup(row_width=1)

            ya_maps = types.InlineKeyboardButton('Ссылка на маршрут в Я.Картах', url='https://clck.ru/34ZPbi', callback_data='qdsgwe')

            photo = open('photo_bot/wine.jpg', 'rb')

            markup.add(ya_maps)

            text = "1️⃣ *London Pub*\n" \
                   "🍽️ Паб\n" \
                   "⭐️ Рейтинг: 4,8\n\n" \
                   "Что выпить❓\n" \
                   "◻️ London Cider - 230₽\n" \
                   "◻️ Мундир Золотой - 230₽\n\n" \
                   "2️⃣ *Свой бар*\n" \
                   "🍽️ Бар\n" \
                   "⭐️ Рейтинг: 5,0\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Вежливый русский - 500₽\n" \
                   "◻️ Hustler - 500₽\n" \
                   "◻️ Aviation - 500₽"

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')
            bot.delete_message(message.chat.id, message.message_id)

        elif message.text == 'Lite\n💸💸💸':

            markup = types.InlineKeyboardMarkup(row_width=1)

            ya_maps = types.InlineKeyboardButton('Ссылка на маршрут в Я.Картах', url='https://clck.ru/34ZPcD', callback_data='qdsgwe')

            photo = open('photo_bot/wine.jpg', 'rb')

            markup.add(ya_maps)

            text = "1️⃣ *Рюмочная хрусталь*\n" \
                   "🍽️ Бар\n" \
                   "⭐️ Рейтинг: 4,9\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Белый русский - 400₽\n" \
                   "◻️ Клубничка 18+ - 150₽\n" \
                   "◻️ Фиеро толик - 400₽\n\n" \
                   "2️⃣ *Министерство культуры*\n" \
                   "🎤 Караоке-клуб\n" \
                   "⭐️ Рейтинг: 4,4\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Citron highball - 680₽\n" \
                   "◻️ Mandarin sour - 680₽" \

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')
            bot.delete_message(message.chat.id, message.message_id)

        elif message.text == 'Middle\n💸':

            markup = types.InlineKeyboardMarkup(row_width=1)

            ya_maps = types.InlineKeyboardButton('Ссылка на маршрут в Я.Картах', url='https://clck.ru/34ZPcx', callback_data='qdsgwe')

            photo = open('photo_bot/wine.jpg', 'rb')

            markup.add(ya_maps)

            text = "1️⃣ *Мойше*\n" \
                   "🍽️ Бар\n" \
                   "⭐️ Рейтинг: 4,9\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Тыква на текиле - 180₽\n" \
                   "◻️ Орех на дубе виски - 180₽\n" \
                   "◻️ Кофе и банан на водке - 180₽\n\n" \
                   "2️⃣ *Вдох Выдох*\n" \
                   "💨 Кальянная \n" \
                   "⭐️ Рейтинг: 4,4\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Сидр - 200₽\n" \
                   "Кальян ❓️\n" \
                   "◻️ Кальян - 900₽" \

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')
            bot.delete_message(message.chat.id, message.message_id)

        elif message.text == 'Middle\n💸💸':

            markup = types.InlineKeyboardMarkup(row_width=1)

            ya_maps = types.InlineKeyboardButton('Ссылка на маршрут в Я.Картах',
                                                url='https://clck.ru/34ZPe8',
                                                callback_data='qdsgwe')

            photo = open('photo_bot/wine.jpg', 'rb')

            markup.add(ya_maps)

            text = "1️⃣ *Ludovic*\n" \
                   "🎤 Караоке\n" \
                   "⭐️ Рейтинг: 4,6\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Бомбей Брамбл - 550₽\n" \
                   "◻️ Martini fiero - 900₽\n\n" \
                   "2️⃣ *Мёд*\n" \
                   "🪩 Ночной клуб\n" \
                   "⭐️ Рейтинг: 4,3\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Муха в Самбуке - 350₽\n" \
                   "️◻️ Голубая лагуна - 290₽\n" \

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')
            bot.delete_message(message.chat.id, message.message_id)

        elif message.text == 'Middle\n💸💸💸':

            markup = types.InlineKeyboardMarkup(row_width=1)

            ya_maps = types.InlineKeyboardButton('Ссылка на маршрут в Я.Картах',
                                                url='https://clck.ru/34ZPeq',
                                                callback_data='qdsgwe')

            photo = open('photo_bot/wine.jpg', 'rb')

            markup.add(ya_maps)

            text = "1️⃣ *Эмбарго*\n" \
                   "🍽️ Бар\n" \
                   "⭐️ Рейтинг: 4,8\n\n" \
                   "Что выпить❓\n" \
                   "◻️ E-ON Black Power&Tundra Authentic - 550₽\n" \
                   "◻️ E-ON Danger Berry&Gin - 750₽\n" \
                   "◻️ E-ON Danger Berry&Gin - 750₽\n\n" \
                   "2️⃣ *Б29*\n" \
                   "⭐️ Рейтинг: 4,8 \n" \
                   "🍽️ Бар\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Хиросима - 350₽\n" \
                   "◻️ Зеленая Фея - 700₽\n" \
                   "◻️ Апероль шприц - 550₽" \

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')
            bot.delete_message(message.chat.id, message.message_id)

        elif message.text == 'Hard\n💸':

            markup = types.InlineKeyboardMarkup(row_width=1)

            ya_maps = types.InlineKeyboardButton('Ссылка на маршрут в Я.Картах',
                                                url='https://clck.ru/34ZPfR',
                                                callback_data='qdsgwe')

            photo = open('photo_bot/wine.jpg', 'rb')

            markup.add(ya_maps)

            text = "1️⃣ *Пунш*\n" \
                   "🪩 Клуб\n" \
                   "⭐️ Рейтинг: 3,2\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Джокер - 400₽\n" \
                   "◻️ Кукарача - 250₽\n" \
                   "◻️ Б-25 - 250₽\n" \
                   "◻️ Водка энергетик - 200₽\n\n" \
                   "2️⃣ *Квадрат*\n" \
                   "🍽️ Бар\n" \
                   "⭐️ Рейтинг: 5,0\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Имбирный эль - 250₽\n" \

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')
            bot.delete_message(message.chat.id, message.message_id)

        elif message.text == 'Hard\n💸💸':

            markup = types.InlineKeyboardMarkup(row_width=1)

            ya_maps = types.InlineKeyboardButton('Ссылка на маршрут в Я.Картах',
                                                url='https://clck.ru/34ZPgC',
                                                callback_data='qdsgwe')

            photo = open('photo_bot/wine.jpg', 'rb')

            markup.add(ya_maps)

            text = "1️⃣ *Бар 13*\n" \
                   "🪩 Ночной клуб\n" \
                   "⭐️ Рейтинг: 4,4\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Мартини тоник - 400₽\n" \
                   "◻️ Эйнштейн - 400₽\n" \
                   "◻️ Май тай - 550₽\n" \
                   "◻️ Эль Дестиладор - 500₽\n\n" \
                   "2️⃣ *Шамайка House*\n" \
                   "🍽️ Паб-ресторан\n" \
                   "⭐️ Рейтинг: 5,0\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Шамайка светлое - 149₽\n" \
                   "◻️ Jameson - 340₽" \

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')
            bot.delete_message(message.chat.id, message.message_id)

        elif message.text == 'Hard\n💸💸💸':

            markup = types.InlineKeyboardMarkup(row_width=1)

            ya_maps = types.InlineKeyboardButton('Ссылка на маршрут в Я.Картах',
                                                url='https://clck.ru/34ZPgW',
                                                callback_data='qdsgwe')

            photo = open('photo_bot/wine.jpg', 'rb')

            markup.add(ya_maps)

            text = "1️⃣ *Голодранец*\n" \
                   "🍽️ Пивной бар\n" \
                   "⭐️ Рейтинг: 4,9\n\n" \
                   "Что выпить❓\n" \
                   "◻️ Камнем по голове - 250₽\n" \
                   "◻️ Бродилка - 250₽\n\n" \
                   "2️⃣ *O.W. Grant*\n" \
                   "🍽️ Бар\n" \
                   "⭐️ Рейтинг: 4,7\n\n" \
                   "Что выпить❓\n" \
                   "◻️ ABSOLUT - 250₽\n" \
                   "◻️ MICHTERS - 850₽\n" \
                   "◻️ SOTOR - 700₽\n" \
                   "◻️ EDEL WEISSER DALMATIAN DRY GIN - 550₽" \

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')
            bot.delete_message(message.chat.id, message.message_id)

        # ветка "Платные предложения"

        elif message.text == 'Платные предложения 💸':

            markup = types.InlineKeyboardMarkup(row_width=2)
            eat = types.InlineKeyboardButton("На 1 месяц", callback_data='1_month')
            time = types.InlineKeyboardButton("На 6 месяцев", callback_data='6_month')
            pay = types.InlineKeyboardButton("На 12 месяцев", callback_data='12_month')

            markup.add(eat, time, pay)

            bot.send_message(message.chat.id, "🎉 По-настоящему запоминающиеся впечатления от Ростова-на-Дону с T-Rostov!\n\n"
                                              "Вас ждут:\n"
                                              "💰Эксклюзивные скидки в лучших заведениях города\n"
                                              "📸 Маршруты по самым красивым и фотогеничным местам города\n"
                                              "🍹 Незабываемые алкотуры по ярким барам города\n\n"
                                              "Станьте одним из немногих обладателей привилегий, доступных только нашим премиум-подписчикам!🔥\n\n"
                                              "◻️ 1 мес. = 199₽\n◻️ 6 мес. = 1079₽\n◻️ 12 мес. = 1799₽\n\n"
                                              "Выберите период подписки:",
                             reply_markup=markup)

        # ветка "Платные предложения после покупки"

        elif message.text == 'Платные предложения 💵':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            instagramm = types.KeyboardButton("Инстаграмные места 📸")
            sales = types.KeyboardButton("Скидки, промокоды 🈹")
            route = types.KeyboardButton("Маршрут по барам 🍹🚶")
            back = types.KeyboardButton("Назад ◀️")

            markup.add(instagramm, sales, route, back)

            bot.send_message(message.chat.id, 'Выберите место:', reply_markup=markup)

        elif message.text == 'Скидки, промокоды 🈹':

            markup = types.InlineKeyboardMarkup(row_width=1)

            ya_maps = types.InlineKeyboardButton('Ссылка на заведение',
                                                 url='https://clck.ru/34bkgS',
                                                 callback_data='qdsgwe')

            photo = open('photo_bot/moishe.png', 'rb')

            markup.add(ya_maps)

            text = "*Мойше*\n\n" \
                   "🍽️ Бар\n" \
                   "💵 Средний чек: 1100₽\n" \
                   "⭐️ Рейтинг: 4,9\n\n" \
                   "💬 У этого бара есть душа, и её зовут Мойше. Каждый коктейль - это захватывающая история, которая сблизит вас с ней. Здесь вы сможете насладиться оригинальными комбинациями вкусов, экспериментальными ингредиентами и превосходными сочетаниями, которые не оставят вас равнодушными!\n\n" \
                   "Сделайте заказ от 1000₽ и получите комплимент от заведения!\n" \
                   "_Промокод_: `5286`" \

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup, parse_mode='Markdown')

        elif message.text == 'Инстаграмные места 📸':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            place1 = types.KeyboardButton("Маршрут 1️⃣")
            place2 = types.KeyboardButton("Маршрут 2️⃣")
            back = types.KeyboardButton("Назад ◀️")

            markup.add(place1, place2, back)

            bot.send_message(message.chat.id, 'Выберите маршрут:', reply_markup=markup)

        else:
            bot.send_message(message.chat.id, 'Я не знаю, что ответить 🤷‍♂️')

            sti = open('photo_bot/sticker1.webp', 'rb')
            bot.send_sticker(message.chat.id, sti)

# Заведения рядом

coordinats = [[47.216998, 39.722837], [47.295992, 39.714052], [47.223779, 39.725972], [47.217084, 39.715785],
              [47.229268, 39.754709], [47.218792, 39.7023912], [47.223639, 39.723592], [47.224893, 39.728308],
              [47.233986, 39.716414], [47.223681, 39.690192], [47.219967, 39.708302], [47.260473, 39.720735],
              [47.203997, 39.723735], [59.781546, 30.148099], [47.219703, 39.710773], [39.702452, 47.212757],
              [47.236886, 39.743202], [47.2332894, 39.735396], [47.222935, 39.695816], [47.287967, 39.712560],
              [47.22547, 39.73008], [47.220897, 39.714007], [47.225364, 39.739070]]

rest_name = ["Эрти", "Гурия", "Lilo", "Не Горюй", "Хинкали Djan",
             "За100лье", "Дружба", "Еда всегда", "Территория Еды",
             "Имбирь", "Вкусно и Точка", "Бургер Кинг", "KFC", "Subway",
             "Штефан Бургер", "Вкусно house", "Черная кошка", "Хлеб и Сало",
             "Живаго", "Бульвар", "Магадан", "Раки и Гады", "More Fish’ka"]
Eda_blizko = {}

@bot.message_handler(content_types=['location'])
def check_location(message):
    user_locate = [message.location.latitude, message.location.longitude]
    for i in range(len(coordinats)):
        p = ((user_locate[0] - coordinats[i][0]) ** 2 + (user_locate[1] - coordinats[i][1]) ** 2) ** (1 / 2)
        Eda_blizko[p] = rest_name[i]
    bot.send_message(message.chat.id, f'📍 Первое заведение: "{Eda_blizko[nsmallest(23, Eda_blizko)[0]]}"\n'
                                      f'📍 Второе заведение: "{Eda_blizko[nsmallest(23, Eda_blizko)[1]]}"\n'
                                      f'📍 Третье заведение: {Eda_blizko[nsmallest(23, Eda_blizko)[2]]}\n'
                                      f'📍 Четвертое заведение: "{Eda_blizko[nsmallest(23, Eda_blizko)[3]]}"\n'
                                      f'📍 Пятое заведение: "{Eda_blizko[nsmallest(23, Eda_blizko)[4]]}"')

def location (message):
    if message.location is not None:

        print(message.location)
        print(message)

    bot.send_message(message.chat.id, message.location)


# RUN
bot.polling(none_stop=True)