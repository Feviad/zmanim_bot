import requests
import re
import pytz
import data
import functions as f
from datetime import datetime, timedelta


URL = 'http://db.ou.org/zmanim'


def get_zmanim(loc, lang):
    tz = f.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    zmanim = requests.get('{}/getCalendarData.php?mode=day&timezone='
                          '{}&dateBegin={}/{}/{}'
                          '&lat={}&lng={}'.format(URL, tz, now.month,
                                                  now.day,
                                                  now.year,
                                                  loc[0],
                                                  loc[1]))
    zmanim_dict = zmanim.json()
    month = re.search(r'[a-zA-z]+', zmanim_dict['hebDateString']) \
        .group(0)
    year_day = re.findall(r'\d+', zmanim_dict['hebDateString'])
    if zmanim_dict['zmanim']['alos_ma'] == 'X:XX:XX':
        chazot_time = datetime.strptime(zmanim_dict['zmanim']['chatzos'],
                                        "%H:%M:%S")
        chazot_delta = timedelta(hours=12)
        alot_delta = chazot_time - chazot_delta
        alot_chazot_time = str(datetime.time(alot_delta))
        zmanim_dict['zmanim']['alos_ma'] = alot_chazot_time
    if lang == 'Русский':
        zmanim_str = 'Еврейская дата: {} {} {} года\n' \
                     'Рассвет (Алот Ашахар) - {:.5s}\n' \
                     'Самое ранее время надевания\n' \
                     'талита и тфлина (Мишеякир) - {:.5s}\n' \
                     'Восход солнца (Нец Ахама) - {:.5s}\n' \
                     'Конец времени чтения Шма - {:.5s}\n' \
                     'Конец времени чтения молитвы \nАмида - {:.5s}\n' \
                     'Полдень (Хацот) - {:.5s}\n' \
                     'Самое раннее время Минхи\n(Минха Гдола) - {:.5s}\n' \
                     'Заход солнца (Шкия) - {:.5s}\n' \
                     'Выход звезд (Цет Акохавим) - {:.5s}\n' \
            .format(year_day[0],
                    data.jewish_months_a[month],
                    year_day[1],
                    zmanim_dict['zmanim']['alos_ma'],
                    zmanim_dict['zmanim']['talis_ma'],
                    zmanim_dict['zmanim']['sunrise'],
                    zmanim_dict['zmanim']['sof_zman_shema_gra'],
                    zmanim_dict['zmanim']['sof_zman_tefila_gra'],
                    zmanim_dict['zmanim']['chatzos'],
                    zmanim_dict['zmanim']['mincha_gedola_ma'],
                    zmanim_dict['zmanim']['sunset'],
                    zmanim_dict['zmanim']['tzeis_595_degrees']
                    )
    elif lang == 'English':
        zmanim_str = 'Hebrew date: {} {} {}\n' \
                     'Alot Hashachar - {:.5s}\n' \
                     'Misheyakir - {:.5s}\n' \
                     'Hanetz Hachama - {:.5s}\n' \
                     'Sof Zman Shema - {:.5s}\n' \
                     'Sof Zman Tefilah - {:.5s}\n' \
                     'Chatzot Hayom - {:.5s}\n' \
                     'Mincha Gedolah - {:.5s}\n' \
                     'Shkiat Hachama - {:.5s}\n' \
                     'Tzeit Hakochavim - {:.5s}\n' \
            .format(year_day[0],
                    month,
                    year_day[1],
                    zmanim_dict['zmanim']['alos_ma'],
                    zmanim_dict['zmanim']['talis_ma'],
                    zmanim_dict['zmanim']['sunrise'],
                    zmanim_dict['zmanim']['sof_zman_shema_gra'],
                    zmanim_dict['zmanim']['sof_zman_tefila_gra'],
                    zmanim_dict['zmanim']['chatzos'],
                    zmanim_dict['zmanim']['mincha_gedola_ma'],
                    zmanim_dict['zmanim']['sunset'],
                    zmanim_dict['zmanim']['tzeis_595_degrees']
                    )
    return zmanim_str


def get_ext_zmanim(loc, lang):
    tz = f.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    zmanim = requests.get('{}/getCalendarData.php?mode=day&timezone='
                          '{}&dateBegin={}/{}/{}'
                          '&lat={}&lng={}'.format(URL, tz, now.month,
                                                  now.day,
                                                  now.year,
                                                  loc[0],
                                                  loc[1]))
    zmanim_dict = zmanim.json()
    month = re.search(r'[a-zA-z]+', zmanim_dict['hebDateString']).group(0)
    year_day = re.findall(r'\d+', zmanim_dict['hebDateString'])
    if zmanim_dict['zmanim']['sof_zman_shema_ma'] == 'X:XX:XX'\
            or zmanim_dict['zmanim']['sof_zman_tefila_ma'] == 'X:XX:XX':
            zmanim_dict['zmanim']['sof_zman_shema_ma'] = '00:00:00'
            zmanim_dict['zmanim']['sof_zman_tefila_ma'] = '00:00:00'

    # блок вычисления времени путем вычитания
    d1 = datetime.strptime(zmanim_dict['zmanim']['sof_zman_shema_ma'],
                           "%H:%M:%S")
    d2 = datetime.strptime(zmanim_dict['zmanim']['sof_zman_tefila_ma'],
                           "%H:%M:%S")
    d3 = datetime.strptime(zmanim_dict['zmanim']['sof_zman_shema_gra'],
                           "%H:%M:%S")
    d4 = datetime.strptime(zmanim_dict['zmanim']['sof_zman_tefila_gra'],
                           "%H:%M:%S")
    d5 = datetime.strptime(zmanim_dict['zmanim']['chatzos'],
                           "%H:%M:%S")
    # высчитываем полночь, прибавляя 12 часов
    d_delta = timedelta(hours=12)
    d6 = d5 + d_delta

    chazot_laila = str(datetime.time(d6))
    shaa_zman_ma = str(d2 - d1)  # астрономический час по маген авраам
    shaa_zman_gra = str(d4 - d3)  # астрономический час по арго
    if zmanim_dict['zmanim']['alos_ma'] == 'X:XX:XX':
        chazot_time = datetime.strptime(zmanim_dict['zmanim']['chatzos'],
                                        "%H:%M:%S")

        chazot_delta = timedelta(hours=12)
        alot_delta = chazot_time - chazot_delta
        alot_chazot_time = str(datetime.time(alot_delta))
        zmanim_dict['zmanim']['alos_ma'] = alot_chazot_time
    if lang == 'Русский':
        zmanim_str = 'Еврейская дата: {} {} {}\n\n' \
                     'Рассвет (Алот Ашахар) - {:.5s}\n' \
                     'Самое ранее время надевания\n' \
                     'талита и тфлина (Мишеякир) - {:.5s}\n' \
                     'Восход солнца (Нец Ахама) - {:.5s}\n' \
                     'Конец времени чтения Шма (Маген Авраам) - {:.5s}\n' \
                     'Конец времени чтения Шма (АГРО) - {:.5s}\n' \
                     'Конец времени чтения молитвы Амида\n' \
                     '(Маген Авраам) - {:.5s}\n' \
                     'Конец времени чтения молитвы Амида\n(АГРО) - {:.5s}\n' \
                     'Полдень (Хацот) - {:.5s}\n' \
                     'Самое раннее время Минхи (Минха Гдола) - {:.5s}\n' \
                     'Малая Минха (Минха Ктана) - {:.5s}\n' \
                     'Полу-Минха (Плаг Минха) - {:.5s}\n' \
                     'Заход солнца (Шкия) - {:.5s}\n' \
                     'Выход звезд, 42 минуты (Цет Акохавим)  - {:.5s}\n' \
                     'Выход звезд, 72 минуты (Цет Акохавим) - {:.5s}\n' \
                     'Выход звезд, 595 градусов (Цет Акохавим) - {:.5s}\n' \
                     'Выход звезд, 850 градусов (Цет Акохавим) - {:.5s}\n' \
                     'Полночь (Хацот Алайла) - 0{:.4s}\n\n' \
                     'Астрономический час (Маген Авраам) - {:.4s}\n' \
                     'Астрономический час (АГРО) - {:.4s}' \
            .format(year_day[0],
                    month,
                    year_day[1],
                    zmanim_dict['zmanim']['alos_ma'],
                    zmanim_dict['zmanim']['talis_ma'],
                    zmanim_dict['zmanim']['sunrise'],
                    zmanim_dict['zmanim']['sof_zman_shema_ma'],
                    zmanim_dict['zmanim']['sof_zman_shema_gra'],
                    zmanim_dict['zmanim']['sof_zman_tefila_ma'],
                    zmanim_dict['zmanim']['sof_zman_tefila_gra'],
                    zmanim_dict['zmanim']['chatzos'],
                    zmanim_dict['zmanim']['mincha_gedola_ma'],
                    zmanim_dict['zmanim']['mincha_ketana_gra'],
                    zmanim_dict['zmanim']['plag_mincha_ma'],
                    zmanim_dict['zmanim']['sunset'],
                    zmanim_dict['zmanim']['tzeis_42_minutes'],
                    zmanim_dict['zmanim']['tzeis_595_degrees'],
                    zmanim_dict['zmanim']['tzeis_850_degrees'],
                    zmanim_dict['zmanim']['tzeis_72_minutes'],
                    chazot_laila, shaa_zman_ma, shaa_zman_gra)
    elif lang == 'English':
        zmanim_str = 'Hebrew date: {} {} {}\n\n' \
                     'Alot Hashachar - {:.5s}\n' \
                     'Misheyakir - {:.5s}\n' \
                     'Hanetz Hachama) - {:.5s}\n' \
                     'Sof Zman Shema (M"A) - {:.5s}\n' \
                     'Sof Zman Shema (GR"A) - {:.5s}\n' \
                     'Sof Zman Tefilah (M"A) - {:.5s}\n' \
                     'Sof Zman Tefilah (GR"A) - {:.5s}\n' \
                     'Chatzot Hayom - {:.5s}\n' \
                     'Mincha Gedolah - {:.5s}\n' \
                     'Mincha Ketanah - {:.5s}\n' \
                     'Plag Mincha - {:.5s}\n' \
                     'Shkiat Hachama - {:.5s}\n' \
                     'Tzeit Hakochavim 42 minutes  - {:.5s}\n' \
                     'Tzeit Hakochavim 72 minutes  - {:.5s}\n' \
                     'Tzeit Hakochavim 595 degrees - {:.5s}\n' \
                     'Tzeit Hakochavim 850 degrees - {:.5s}\n' \
                     'Chatzot Halayiah - 0{:.4s}\n\n' \
                     'Astronomical Hour (M"A) - {:.4s}\n' \
                     'Astronomical Hour (GR"A) - {:.4s}' \
            .format(year_day[0],
                    data.jewish_months[month],
                    year_day[1],
                    zmanim_dict['zmanim']['alos_ma'],
                    zmanim_dict['zmanim']['talis_ma'],
                    zmanim_dict['zmanim']['sunrise'],
                    zmanim_dict['zmanim']['sof_zman_shema_ma'],
                    zmanim_dict['zmanim']['sof_zman_shema_gra'],
                    zmanim_dict['zmanim']['sof_zman_tefila_ma'],
                    zmanim_dict['zmanim']['sof_zman_tefila_gra'],
                    zmanim_dict['zmanim']['chatzos'],
                    zmanim_dict['zmanim']['mincha_gedola_ma'],
                    zmanim_dict['zmanim']['mincha_ketana_gra'],
                    zmanim_dict['zmanim']['plag_mincha_ma'],
                    zmanim_dict['zmanim']['sunset'],
                    zmanim_dict['zmanim']['tzeis_42_minutes'],
                    zmanim_dict['zmanim']['tzeis_595_degrees'],
                    zmanim_dict['zmanim']['tzeis_850_degrees'],
                    zmanim_dict['zmanim']['tzeis_72_minutes'],
                    chazot_laila, shaa_zman_ma, shaa_zman_gra)

    return zmanim_str


if __name__ == '__main__':
    pass
