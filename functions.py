import sqlite3
import urllib.parse as urlparse
import os
import re
import requests
import psycopg2
import telebot
import bot
import config


def check_id_in_db(user):
    if os.environ.get('LOCAL') == 'YES':
        conn = sqlite3.connect('telegram_bot.db')
    else:
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])

        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    cur = conn.cursor()
    query = f'SELECT id FROM users WHERE id = {user.id}'
    status = cur.execute(query).fetchone()
    if not status:
        if not user.first_name:
            user.first_name = 'NULL'
        if not user.last_name:
            user.last_name = 'NULL'
        query = f'INSERT INTO users (id, first_name, last_name)' \
                f'VALUES (' \
                f'\'{user.id}\', \'{user.first_name}\', \'{user.last_name}\')'
        cur.execute(query)
        conn.commit()
    conn.close()


def check_location(user, lat, long):
    if os.environ.get('LOCAL') == 'YES':
        conn = sqlite3.connect('telegram_bot.db')
    else:
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])

        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    cur = conn.cursor()
    query = f'SELECT latitude, longitude FROM locations ' \
            f'WHERE id = {user}'
    locations_in_db = cur.execute(query).fetchone()
    if not locations_in_db:
        query = f'INSERT INTO locations (id, latitude, longitude)' \
                f'VALUES (\'{user}\', \'{lat}\', \'{long}\')'
        cur.execute(query)
        conn.commit()
        bot.bot.send_message(user, 'Координаты получены/Location has been '
                                   'recived')
    # если координаты в бд отличаются от присланных, обновляем бд
        print(locations_in_db)
    elif lat != locations_in_db[0] or long != locations_in_db[1]:
        query = f'UPDATE locations SET ' \
                f'latitude = \'{lat}\', longitude = \'{long}\'' \
                f'WHERE id = {user}'
        bot.bot.send_message(user, 'Координаты обновлены/Location updated')
        cur.execute(query)
        conn.commit()

    conn.close()


def get_location_by_id(user_id):
    if os.environ.get('LOCAL') == 'YES':
        conn = sqlite3.connect('telegram_bot.db')
    else:
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])

        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    cur = conn.cursor()
    query = f'SELECT latitude, longitude FROM locations WHERE id = {user_id}'
    location = cur.execute(query).fetchone()
    if not location:
        return False
    return location


def check_tz(user, tz):
    if os.environ.get('LOCAL') == 'YES':
        conn = sqlite3.connect('telegram_bot.db')
    else:
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])

        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    cur = conn.cursor()
    query = f'SELECT tz FROM tz WHERE id = {user}'
    time_zone = cur.execute(query).fetchone()
    if not time_zone:
        query = f'INSERT INTO tz (id, tz) VALUES ({user}, \'{tz}\')'
        cur.execute(query)
        conn.commit()
    elif time_zone != tz:
        query = f'UPDATE tz SET tz = \'{tz}\' WHERE id = {user}'
        cur.execute(query)
        conn.commit()


def get_tz_by_location(location):
    url = f'http://api.timezonedb.com/v2/get-time-zone?' \
          f'key=2KSPDV130SP1&format=json&' \
          f'by=position&lat={location[0]}&lng={location[1]}'
    tz_data = requests.get(url).json()
    tz = tz_data['zoneName']
    return tz


def get_main_menu(lang):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    if lang == 'English':
        user_markup.row('Zmanim', 'Shabbos', 'Holidays')
        user_markup.row('Extended Zmanim', 'Rosh Chodesh')
        user_markup.row('Fast days', 'Daf Yomi')
        user_markup.row('Update location', 'Change language')
    elif lang == 'Русский':
        user_markup.row('Зманим', 'Шаббат', 'Праздники')
        user_markup.row('Расширенные Зманим', 'Рош-Ходеш')
        user_markup.row('Посты', 'Даф Йоми (Талмуд)')
        user_markup.row('Обновить местоположение', 'Сменить язык')
    return user_markup


def get_holiday_menu(lang):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    if lang == 'Русский':
        user_markup.row('Рош-Ашана', 'Йом-Кипур')
        user_markup.row('Суккот', 'Шмини Ацерет')
        user_markup.row('Ханука', 'Ту биШват', 'Пурим')
        user_markup.row('Пейсах', 'Лаг баОмер', 'Шавуот')
        user_markup.row('15 Ава', 'Израильские праздники')
        user_markup.row('Назад')
    elif lang == 'English':
        user_markup.row('Rosh HaShanah', 'Yom Kippur')
        user_markup.row('Succos', 'Shmini Atzeres')
        user_markup.row('Chanukah', 'Tu BShevat', 'Purim')
        user_markup.row('Pesach', 'Lag BaOmer', 'Shavuot')
        user_markup.row('Tu BAv', 'Israel holidays')
        user_markup.row('Back')
    return user_markup


def get_fast_menu(lang):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    if lang == 'Русский':
        user_markup.row('Пост Гедалии', '10 Тевета')
        user_markup.row('Пост Эстер', '17 Таммуза')
        user_markup.row('9 Ава')
        user_markup.row('Назад')
    elif lang == 'English':
        user_markup.row('Tzom Gedaliah', 'Asarah BTevet')
        user_markup.row('Taanit Esther', 'Shiva Asar BTammuz')
        user_markup.row('Tisha BAv')
        user_markup.row('Back')
    return user_markup


def check_str_location(str):
    pattern = r'^(-)?(\d){1,2}(\.){1}(\d)+(, ){1}(-)?(\d){1,2}(\.){1}(\d)+'
    location = re.search(pattern, str).group(0)
    if location:
        loc = location.split(sep=', ')
        return loc
    else:
        return False


if __name__ == '__main__':
    pass
