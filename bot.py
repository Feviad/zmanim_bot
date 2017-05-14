# -*- coding: utf-8 -*-
import re
import telebot
import botan
import config
import zmanim
import rosh_hodesh
import shabbos
import daf
import functions as f
import holidays as h
from flask import Flask, request


# Подключение к боту
bot = telebot.TeleBot(config.TOKEN)
URL = 'http://db.ou.org/zmanim'

loc_pattern = r'^-?\d{1,2}\.{1}\d+, {1}-?\d{1,2}\.{1}\d+$'


@bot.message_handler(commands=['start'])
def handle_start(message):
    # проверяем id в бд, если нет - добавляем
    f.check_id_in_db(message.from_user)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Русский', 'English')
    bot.send_message(message.from_user.id,
                     'Выберите язык/Choose the language',
                     reply_markup=user_markup
                     )
    botan.track(message.from_user.id, message, 'start')


@bot.message_handler(commands=['help'])
def handle_help(message):
    menu = telebot.types.ReplyKeyboardMarkup(True, False)
    menu.row('🇷🇺', '🇱🇷', 'Назад/Back')
    help_str = 'Пожалуйста, выберите язык справки'
    bot.send_message(message.from_user.id,
                     help_str,
                     reply_markup=menu)
    botan.track(message.from_user.id, message, 'help')


@bot.message_handler(commands=['report'])
def handle_report(message):
    report_str = 'Чтобы сообщить об ошибке, пожалуйста, напишите сюда \n' \
                 't.me/benyomin, или сюда \nt.me/Meir_Yartzev. \nПожалуйста,' \
                 ' убедитесь, что вы ознакомились с часто задаваемыми' \
                 ' вопросами, доступными по команде /help\n\nFor bug report ' \
                 'please write to \nt.me/benyomin or \nt.me/Meir_Yartzev. ' \
                 '\nPlease, make sure that you had been read '\
                 'F.A.Q. available by command /help'
    bot.send_message(message.from_user.id,
                     report_str,
                     disable_web_page_preview=True)
    botan.track(message.from_user.id, message, 'report')


@bot.message_handler(content_types=['location'])
def handle_text(message):
    f.check_location(message.from_user.id,
                     message.location.latitude,
                     message.location.longitude
                     )
    tz = f.get_tz_by_location(f.get_location_by_id(message.from_user.id))
    f.check_tz(message.from_user.id, tz)
    botan.track(message.from_user.id, message, 'Получил геометку')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Сменить язык' or    \
       message.text == 'Change language' or \
       message.text == 'Назад/Back':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Русский', 'English')
        bot.send_message(message.from_user.id, 'Выберите язык/'
                                               'Choose the language',
                         reply_markup=user_markup)
        botan.track(message.from_user.id, message, 'Выбор языка')

    elif message.text == '🇱🇷':  # FAQ
        bot.send_message(message.from_user.id, 'https://goo.gl/4320iu')
        botan.track(message.from_user.id, message, 'FAQ')
    elif message.text == '🇷🇺':  # ЧАВО
        bot.send_message(message.from_user.id, 'https://goo.gl/bavHuO')
        botan.track(message.from_user.id, message, 'ЧАВО')

    elif message.text == 'Русский':
        user_markup = f.get_main_menu(message.text)
        bot.send_message(message.from_user.id, text='Выберите',
                         reply_markup=user_markup)
        botan.track(message.from_user.id, message, 'Выбран русский язык')
    elif message.text == 'English':
        user_markup = f.get_main_menu(message.text)
        bot.send_message(message.from_user.id, text='Choose the option',
                         reply_markup=user_markup)
        botan.track(message.from_user.id, message, 'Выбран английский язык')

    elif message.text == 'Зманим':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            zmanim_str = zmanim.get_zmanim(loc, 'Русский')
            bot.send_message(message.chat.id, zmanim_str)
            botan.track(message.from_user.id, message, 'Зманим Рус')
    elif message.text == 'Zmanim':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            zmanim_str = zmanim.get_zmanim(loc, 'English')
            bot.send_message(message.chat.id, zmanim_str)
            botan.track(message.from_user.id, message, 'Зманим Англ')

    elif message.text == 'Расширенные Зманим':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            zmanim_str = zmanim.get_ext_zmanim(loc, 'Русский')
            bot.send_message(message.chat.id, zmanim_str)
            botan.track(message.from_user.id, message,
                        'Расширенные Зманим Рус')
    elif message.text == 'Extended Zmanim':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            zmanim_str = zmanim.get_ext_zmanim(loc, 'English')
            bot.send_message(message.chat.id, zmanim_str)
            botan.track(message.from_user.id, message,
                        'Расширенные зманим Англ')

    elif message.text == 'Шаббат':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.from_user.id,
                             'Отправьте свое местоположение')
        else:
            shabbat_str = shabbos.get_shabbos_string(loc, 'Русский')
            bot.send_message(message.from_user.id, shabbat_str)
            botan.track(message.from_user.id, message, 'Шаббат Рус')
    elif message.text == 'Shabbos':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.from_user.id, 'Send your location')
        else:
            shabbat_str = shabbos.get_shabbos_string(loc, 'English')
            bot.send_message(message.from_user.id, shabbat_str)
            botan.track(message.from_user.id, message, 'Шаббат Англ')

    elif message.text == 'Рош-Ходеш':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        rh = rosh_hodesh.get_rh(loc, 'Русский')
        bot.send_message(message.chat.id, rh)
        botan.track(message.from_user.id, message, 'Рош-Ходеш Рус')
    elif message.text == 'Rosh Chodesh':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        rh = rosh_hodesh.get_rh(loc, 'English')
        bot.send_message(message.chat.id, rh)
        botan.track(message.from_user.id, message, 'Рош-Ходеш Англ')

    elif message.text == 'Праздники':
        holiday_menu = f.get_holiday_menu('Русский')
        bot.send_message(message.from_user.id, 'Выберите '
                                               '(клавиатуру можно скроллить)',
                         reply_markup=holiday_menu)
        botan.track(message.from_user.id, message, 'Праздники Рус')
    elif message.text == 'Holidays':
        holiday_menu = f.get_holiday_menu('English')
        bot.send_message(message.from_user.id, 'Choose (scroll keyboard)',
                         reply_markup=holiday_menu)
        botan.track(message.from_user.id, message, 'Праздники Англ')

    elif message.text == 'Посты':
        fast_menu = f.get_fast_menu('Русский')
        bot.send_message(message.from_user.id, 'Выберите',
                         reply_markup=fast_menu)
        botan.track(message.from_user.id, message, 'Посты Рус')
    elif message.text == 'Fast days':
        fast_menu = f.get_fast_menu('English')
        bot.send_message(message.from_user.id, 'Choose',
                         reply_markup=fast_menu)
        botan.track(message.from_user.id, message, 'Посты Англ')

    elif message.text == 'Даф Йоми (Талмуд)':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        daf_yomi = daf.get_daf(loc, 'Русский')
        bot.send_message(message.from_user.id, daf_yomi)
        botan.track(message.from_user.id, message, 'Дай Йоми Рус')
    elif message.text == 'Daf Yomi':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        daf_yomi = daf.get_daf(loc, 'English')
        bot.send_message(message.from_user.id, daf_yomi)
        botan.track(message.from_user.id, message, 'Даф Йоми Англ')

    elif re.match(loc_pattern, message.text):
        print(123)
        loc = message.text.split(sep=', ')
        f.check_location(message.from_user.id, loc[0], loc[1])
        botan.track(message.from_user.id, message, 'Получил текстовую локацию')

    elif message.text == 'Обновить местоположение':
        upd_str = 'Пожалуйста, пришлите новые координаты'
        bot.send_message(message.from_user.id, upd_str)
        botan.track(message.from_user.id, message, 'Обновить локацию Рус')
    elif message.text == 'Update location':
        upd_str = 'Please, send new location'
        bot.send_message(message.from_user.id, upd_str)
        botan.track(message.from_user.id, message, 'Обновил Локацию Англ')

    elif message.text == 'Назад':
        user_markup = f.get_main_menu('Русский')
        bot.send_message(message.from_user.id, 'Выберите:',
                         reply_markup=user_markup)
        botan.track(message.from_user.id, message, 'Назад Рус')
    elif message.text == 'Back':
        user_markup = f.get_main_menu('English')
        bot.send_message(message.from_user.id, 'Choose:',
                         reply_markup=user_markup)
        botan.track(message.from_user.id, message, 'Назад Англ')
###############################################################################
    elif message.text == 'Рош-Ашана':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            loc = ['55.7', '37.5']
            h_str = h.rosh_hashanah(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Рош аШана Рус')
    elif message.text == 'Rosh HaShanah':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            h_str = h.rosh_hashanah(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Рош аШана Англ')

    elif message.text == 'Йом-Кипур':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.yom_kipur(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Йом-Кипур Рус')
    elif message.text == 'Yom Kippur':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            h_str = h.yom_kipur(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Йом-Кипур Англ')

    elif message.text == 'Суккот':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.succos(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Суккот Рус')
    elif message.text == 'Succos':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            h_str = h.succos(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Суккот Англ')

    elif message.text == 'Шмини Ацерет':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.shmini_atzeres_simhat(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Шмини Ацерет Рус')
    elif message.text == 'Shmini Atzeres':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            h_str = h.shmini_atzeres_simhat(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Шмини Ацерет Англ')

    elif message.text == 'Ханука':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.chanukah(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Ханука Рус')
    elif message.text == 'Chanukah':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            h_str = h.chanukah(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Ханука Англ')

    elif message.text == 'Ту биШват':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.tu_bshevat(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Ту биШват Рус')
    elif message.text == 'Tu BShevat':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            h_str = h.tu_bshevat(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Ту-биШват Англ')

    elif message.text == 'Пурим':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.purim(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Пурим Рус')
    elif message.text == 'Purim':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            h_str = h.purim(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Пурим Англ')

    elif message.text == 'Пейсах':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.pesach(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Пейсах Рус')
    elif message.text == 'Pesach':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            h_str = h.pesach(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Пейсах Англ')

    elif message.text == 'Лаг баОмер':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.lag_baomer(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Лаг Баомер Рус')
    elif message.text == 'Lag BaOmer':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            h_str = h.lag_baomer(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Лаг Баомер Англ')

    elif message.text == 'Шавуот':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.shavuot(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Шавуот Рус')
    elif message.text == 'Shavuot':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            h_str = h.shavuot(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Шавуот Англ')

    elif message.text == '15 Ава':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.tu_bav(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, '15 Ава Рус')
    elif message.text == 'Tu BAv':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.tu_bav(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, '15 Ава Англ')

    elif message.text == 'Израильские праздники':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.get_israel(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message,
                        'Израильские праздники Рус')
    elif message.text == 'Israel holidays':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Send your location')
        else:
            h_str = h.get_israel(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message,
                        'Израильские праздники Англ')

    elif message.text == 'Пост Гедалии':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.tzom_gedaliah(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Пост Гедалии Рус')
    elif message.text == 'Tzom Gedaliah':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.tzom_gedaliah(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Пост Гедалии Англ')

    elif message.text == '10 Тевета':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.asarah_btevet(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, '10 Тевета Рус')
    elif message.text == 'Asarah BTevet':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.asarah_btevet(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, '10 Тевета Англ')

    elif message.text == 'Пост Эстер':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.taanit_esther(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Пост Эстер Рус')
    elif message.text == 'Taanit Esther':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.taanit_esther(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, 'Пост Эстер Англ')

    elif message.text == '17 Таммуза':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.shiva_asar_tammuz(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, '17 Таммуза Рус')
    elif message.text == 'Shiva Asar BTammuz':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.shiva_asar_tammuz(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, '17 Таммуза Англ')

    elif message.text == '9 Ава':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.tisha_bav(loc, 'Русский')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, '9 Ава Рус')
    elif message.text == 'Tisha BAv':
        loc = f.get_location_by_id(message.from_user.id)
        if not loc:
            bot.send_message(message.chat.id, 'Отправьте свое местоположение')
        else:
            h_str = h.tisha_bav(loc, 'English')
            bot.send_message(message.from_user.id, h_str)
            botan.track(message.from_user.id, message, '9 Ава Англ')


app = Flask(__name__)


@app.route('/{}'.format(config.TOKEN), methods=['POST'])
def view():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'ok'



bot.remove_webhook()
url = config.URL
bot.set_webhook(url)
