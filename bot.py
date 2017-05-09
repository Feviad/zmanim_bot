# -*- coding: utf-8 -*-
import sqlite3
import requests
import re
import pytz
import telebot
import config
import zmanim
import rosh_hodesh
import shabbos
import daf
import data
import functions as f
from datetime import datetime, timedelta
import holidays

# Подключение к боту
bot = telebot.TeleBot(config.TOKEN)
URL = 'http://db.ou.org/zmanim'

# подключение к БД
conn = sqlite3.connect('telegram_bot.db')
cur = conn.cursor()


# Логирование запросов
def log(message, answer):
    print('\n ---------------------------')
    from datetime import datetime
    print(datetime.now())
    print('Сообщение от {0} {1}. (id = {2}) \n'
          'Текст - {3}'.format(message.from_user.first_name,
                               message.from_user.last_name,
                               str(message.from_user.id), message.text
                               )
          )
    print(answer, '\n')


@bot.message_handler(commands=['start'])
def handle_start(message):
    # проверяем id в бд, если нет - добавляем
    f.check_id_in_db(message.from_user.id)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Русский', 'English')
    bot.send_message(message.from_user.id,
                     'Выберите язык/Choose the language',
                     reply_markup=user_markup
                     )
    answer = 'Запустил старт'
    log(message, answer)


@bot.message_handler(content_types=['location'])
def handle_text(message):
    f.check_location(message)
    tz = f.get_tz_by_location(f.get_location_by_id(message.from_user.id))
    f.check_tz(message.from_user.id, tz)
    answer = 'Запустил геолокацию'
    log(message, answer)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Сменить язык':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Русский', 'English')
        bot.send_message(message.from_user.id, 'Выберите язык/'
                                               'Choose the language',
                         reply_markup=user_markup)
        answer = 'Запустил смену языка'
        log(message, answer)
    if message.text == 'Change language':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Русский', 'English')
        bot.send_message(message.from_user.id, 'Выберите язык/'
                                               'Choose the language',
                         reply_markup=user_markup)
        answer = 'Запустил смену языка'
        log(message, answer)

    if message.text == 'Русский':
        user_markup = f.get_main_menu(message.text)
        bot.send_message(message.from_user.id, text='Выберите',
                         reply_markup=user_markup)
        answer = 'Запустил русский язык'
        log(message, answer)
    if message.text == 'English':
        user_markup = f.get_main_menu(message.text)
        bot.send_message(message.from_user.id, text='Choose the option',
                         reply_markup=user_markup)
        answer = 'Запустил английский язык'
        log(message, answer)

    if message.text == 'Праздники':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Рош-Ашана', 'Йом-Кипур')
        user_markup.row('Суккот', 'Шмини Ацерет и Симхат Тора')
        user_markup.row('Ханука', 'Ту биШват', 'Пейсах')
        user_markup.row('Лаг баОмер', 'Шавуот')
        user_markup.row('15 Ава', 'Израильские праздники')
        user_markup.row('Назад')
        bot.send_message(message.from_user.id, 'Выберите',
                         reply_markup=user_markup)
        answer = 'Запустил Праздники'
        log(message, answer)
    if message.text == 'Посты':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Пост 10 Тевета', 'Пост Эстер')
        user_markup.row('Пост 17 Таммуза', 'Пост 9 Ава')
        user_markup.row('Пост Гедальи')
        user_markup.row('Назад')
        bot.send_message(message.from_user.id, 'Выберите',
                         reply_markup=user_markup)
        answer = 'Запустил Посты'
        log(message, answer)

    if message.text == 'Назад':
        user_markup = f.get_main_menu('Русский')
        bot.send_message(message.from_user.id, 'Выберите:',
                         reply_markup=user_markup)
        answer = 'Запустил код'
        log(message, answer)
    if message.text == 'Back':
        user_markup = f.get_main_menu('English')
        bot.send_message(message.from_user.id, 'Choose:',
                         reply_markup=user_markup)
        answer = 'Запустил код'
        log(message, answer)

    if message.text == 'Рош-Ходеш':
        loc = f.get_location_by_id(message.from_user.id)
        rh = rosh_hodesh.get_rh(loc, 'Русский')
        bot.send_message(message.chat.id, rh)
        answer = 'Запустил Рош-Ходеш рус'
        log(message, answer)
    if message.text == 'Rosh Chodesh':
        loc = f.get_location_by_id(message.from_user.id)
        rh = rosh_hodesh.get_rh(loc, 'English')
        bot.send_message(message.chat.id, rh)
        answer = 'Запустил Рош-Ходеш англ'
        log(message, answer)

    if message.text == 'Рош-Ашана':
        bot.send_message(message.chat.id, holidays.RoshHaShanah_str)
        answer = 'Запустил Рош-Ашана'
        log(message, answer)
    if message.text == 'Пост Гедальи':
        bot.send_message(message.chat.id, holidays.TzomGedaliah_str)
        answer = 'Запустил Пост Гедальи'
        log(message, answer)
    if message.text == 'Йом-Кипур':
        bot.send_message(message.chat.id, holidays.YomKippur_str)
        answer = 'Запустил Йом-Кипур'
        log(message, answer)
    if message.text == 'Суккот':
        bot.send_message(message.chat.id, holidays.Succos_str)
        answer = 'Запустил Суккот'
        log(message, answer)
    if message.text == 'Шмини Ацерет и Симхат Тора':
        bot.send_message(message.chat.id, holidays.ShminiAtzeres_Simhat_str)
        answer = 'Запустил Шмини Ацерет и Симхат Тора'
        log(message, answer)
    if message.text == 'Ханука':
        bot.send_message(message.chat.id, holidays.Chanukah_str)
        answer = 'Запустил Хануку'
        log(message, answer)
    if message.text == 'Пост 10 Тевета':
        bot.send_message(message.chat.id, holidays.AsarahBTevet_str)
        answer = 'Запустил 10 Тевета'
        log(message, answer)
    if message.text == 'Ту биШват':
        bot.send_message(message.chat.id, holidays.TuBShevat_str)
        answer = 'Запустил Ту биШват'
        log(message, answer)
    if message.text == 'Пост Эстер':
        bot.send_message(message.chat.id, holidays.TaanitEsther_str)
        answer = 'Запустил Пост Эстер'
        log(message, answer)
    if message.text == 'Пурим':
        bot.send_message(message.chat.id, holidays.Purim_str)
        answer = 'Запустил Пурим'
        log(message, answer)
    if message.text == 'Пейсах':
        bot.send_message(message.chat.id, holidays.Pesach_str)
        answer = 'Запустил Пейсах'
        log(message, answer)
    if message.text == 'Израильские праздники':
        bot.send_message(message.chat.id, holidays.Israel_str)
        answer = 'Запустил Израильские праздники'
        log(message, answer)
    if message.text == 'Лаг баОмер':
        bot.send_message(message.chat.id, holidays.LagBaOmer_str)
        answer = 'Запустил Лаг баОмер'
        log(message, answer)
    if message.text == 'Шавуот':
        bot.send_message(message.chat.id, holidays.Shavuot_str)
        answer = 'Запустил Шавуот'
        log(message, answer)
    if message.text == 'Пост 17 Таммуза':
        bot.send_message(message.chat.id, holidays.ShivaAsarBTammuz_str)
        answer = 'Запустил 17 Таммуза'
        log(message, answer)
    if message.text == 'Пост 9 Ава':
        bot.send_message(message.chat.id, holidays.TishaBAv_str)
        answer = 'Запустил 9 Ава'
        log(message, answer)
    if message.text == '15 Ава':
        bot.send_message(message.chat.id, holidays.TuBAv_str)
        answer = 'Запустил 15 Ава'
        log(message, answer)

    if message.text == 'Шаббат':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.from_user.id, 'Отправьте свое местоположение')
        else:
            shabbat_str = shabbos.get_shabbos_string(loc, 'Русский')
            bot.send_message(message.from_user.id, shabbat_str)
            answer = 'Запустил Шаббат рус'
            log(message, answer)
    if message.text == 'Shabbos':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.from_user.id, 'Send your location')
        else:
            shabbat_str = shabbos.get_shabbos_string(loc, 'English')
            bot.send_message(message.from_user.id, shabbat_str)
            answer = 'Запустил Шаббат анг'
            log(message, answer)

    if message.text == 'Расширенные Зманим':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            zmanim_str = zmanim.get_ext_zmanim(loc, 'Русский')
            bot.send_message(message.chat.id, zmanim_str)
            answer = 'Запустил Расширенные Зманим рус'
            log(message, answer)
    if message.text == 'Extended Zmanim':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            zmanim_str = zmanim.get_ext_zmanim(loc, 'English')
            bot.send_message(message.chat.id, zmanim_str)
            answer = 'Запустил Расширенные Зманим англ'
            log(message, answer)

    if message.text == 'Зманим':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            zmanim_str = zmanim.get_zmanim(loc, 'Русский')
            bot.send_message(message.chat.id, zmanim_str)
            answer = 'Запустил Зманим рус'
            log(message, answer)
    if message.text == 'Zmanim':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            zmanim_str = zmanim.get_zmanim(loc, 'English')
            bot.send_message(message.chat.id, zmanim_str)
            answer = 'Запустил Зманим англ'
            log(message, answer)

    if message.text == 'Даф Йоми (Талмуд)':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        daf_yomi = daf.get_daf(loc, 'Русский')
        bot.send_message(message.from_user.id, daf_yomi)
        answer = 'Запустил даф йоми рус'
    if message.text == 'Daf Yomi':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        daf_yomi = daf.get_daf(loc, 'English')
        bot.send_message(message.from_user.id, daf_yomi)
        answer = 'Запустил даф йоми англ'


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
