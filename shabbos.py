import pytz
import requests
from datetime import datetime, timedelta
import functions as f
import data


URL = 'http://db.ou.org/zmanim/getCalendarData.php'


def get_next_weekday(startdate, weekday):
    d = datetime.strptime(startdate, '%Y-%m-%d')
    t = timedelta((7 + weekday - d.weekday()) % 7)
    return (d + t).strftime('%Y-%m-%d')


def get_shabbos_string(loc, lang):
    tz = f.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    date_str = f'{now.year}-{now.month}-{now.day}'
    shabbat_date = get_next_weekday(date_str, 5)
    month = shabbat_date[5:7:]
    day = shabbat_date[8::]
    year = shabbat_date[:4:]
    params = {'mode': 'day',
              'timezone': tz,
              'dateBegin': f'{month}/{day}/{year}',
              'lat': loc[0],
              'lng': loc[1]
              }
    shabbat = requests.get(URL, params=params)
    shabbat_dict = shabbat.json()
    if lang == 'Русский':
        shabbat_str = 'Недельная глава: {}\n' \
                      'Зажигание свечей: {}\n' \
                      'Выход звёзд: {}'.format(
                            data.parashat[shabbat_dict['parsha_shabbos']],
                            shabbat_dict['candle_lighting_shabbos'][:-3:],
                            shabbat_dict['zmanim']['tzeis_850_degrees'][:-3]
                            )
    elif lang == 'English':
        shabbat_str = 'Parshat hashavua: {}\n' \
                      'Candle lighting: {}\n' \
                      'Tzeit hakochavim: {}'.format(
                            shabbat_dict['parsha_shabbos'],
                            shabbat_dict['candle_lighting_shabbos'][:-3:],
                            shabbat_dict['zmanim']['tzeis_850_degrees'][:-3]
                            )
    return shabbat_str

if __name__ == '__main__':
    pass
