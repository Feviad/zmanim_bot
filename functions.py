import sqlite3
import requests
import telebot
import bot


def check_id_in_db(user):
    conn = sqlite3.connect('telegram_bot.db')
    cur = conn.cursor()
    query = f'SELECT id FROM users WHERE id = {user}'
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


def check_location(message):
    conn = sqlite3.connect('telegram_bot.db')
    cur = conn.cursor()
    user = message.from_user.id
    lat = message.location.latitude
    long = message.location.longitude
    query = f'SELECT latitude, longitude FROM locations ' \
            f'WHERE id = {user}'
    locations_in_db = cur.execute(query).fetchone()
    if not locations_in_db:
        query = f'INSERT INTO locations (id, latitude, longitude)' \
                f'VALUES (\'{user}\', \'{lat}\', \'{long}\')'
        cur.execute(query)
        conn.commit()
        bot.bot.send_message(user, 'Координаты получены/Location recived')
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
    conn = sqlite3.connect('telegram_bot.db')
    cur = conn.cursor()
    query = f'SELECT latitude, longitude FROM locations WHERE id = {user_id}'
    location = cur.execute(query).fetchone()
    if not location:
        return False
    return location


def check_tz(user, tz):
    conn = sqlite3.connect('telegram_bot.db')
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
        user_markup.row('Zmanim', 'Shabbos', 'Holydays')
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
        user_markup.row('Зманим', 'Шаббат', 'Праздники')
        user_markup.row('Расширенные Зманим', 'Рош-Ходеш')
        user_markup.row('Посты', 'Даф Йоми (Талмуд)')
        user_markup.row('Обновить местоположение', 'Сменить язык')
    elif lang == 'English':
        user_markup.row('Зманим', 'Шаббат', 'Праздники')
        user_markup.row('Расширенные Зманим', 'Рош-Ходеш')
        user_markup.row('Посты', 'Даф Йоми (Талмуд)')
        user_markup.row('Обновить местоположение', 'Сменить язык')


if __name__ == '__main__':
    pass
