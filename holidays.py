# -*- coding: utf-8 -*-
import requests
import time
from datetime import datetime, timedelta
import pytz
import re
import data
import functions as f

URL = 'http://db.ou.org/zmanim'


# Получаем словарь , index - индекс в общем json'е
def get_holidays_dict(index, loc):
    tz = f.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    year = now.year
    month = now.month
    day = now.day
    if tz == 'Asia/Jerusalem' or tz == 'Asia/Tel_Aviv' or tz == 'Asia/Hebron':
        israel = 'israelHolidays=true'
        url = f'{URL}/getHolidayCalData.php?year={year}&{israel}'
    else:
        url = f'{URL}/getHolidayCalData.php?year={year}'

    holidays = requests.get(url)
    holidays_dicts = holidays.json()
    holidays_dict = holidays_dicts[index]
    if month == 1 and holidays_dict['name'] == 'AsarahBTevet'\
            or holidays_dict['name'] == 'Chanukah':
        url = f'{URL}/getHolidayCalData.php?year={year - 1}'
        holidays = requests.get(url)
        holidays_dicts = holidays.json()
        holidays_dict = holidays_dicts[index]
        h_numbers = re.findall(r'\d+', holidays_dict['dateYear1'])
        brackets = re.findall(r'[(){}[\]]+', holidays_dict['dateYear1'])
        if brackets and int(h_numbers[1]) > int(day)\
                and holidays_dict['name'] == 'Chanukah'\
                or brackets and holidays_dict['name'] == 'AsarahBTevet'\
                and int(h_numbers[0]) > int(day):
            url = f'{URL}/getHolidayCalData.php?year={year - 1}'
            holidays = requests.get(url)
            holidays_dicts = holidays.json()
            holidays_dict = holidays_dicts[index]
        else:
            url = f'{URL}/getHolidayCalData.php?year={year}'
            holidays = requests.get(url)
            holidays_dicts = holidays.json()
            holidays_dict = holidays_dicts[index]
    return holidays_dict


# Парсим название праздника/поста, чтобы перевести его
def get_holiday_name(holidays_dict, lang):
    holiday = re.findall(r'[a-zA-z]+', holidays_dict['name'])
    name = ''
    if lang == 'Русский':
        name = str(data.holidays_name[str(holiday[0])])
    elif lang == 'English':
        name = str(data.holidays_name_en[str(holiday[0])])

    return name


# Получаем данные по празднику
def get_holiday_data(holidays_dict, loc, lang):
    tz = f.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    year = now.year
    month = now.month
    day = now.day
    h_numbers = re.findall(r'\d+', holidays_dict['dateYear1'])
    d_m = re.findall(r'[a-zA-z]+', holidays_dict['dateYear1'])
    h_numbers_2 = re.findall(r'\d+', holidays_dict['dateYear2'])
    d_m_2 = re.findall(r'[a-zA-z]+', holidays_dict['dateYear2'])
    brackets = re.findall(r'[(){}[\]]+', holidays_dict['dateYear1'])
    holiday_number = ''
    if len(d_m) == 4 or len(d_m_2) == 4:
        day2 = h_numbers[1]
        month2 = data.holidays_month_index[d_m[3]]
        if brackets:
            month2 = 13
        if int(month2) == int(month) and int(day2) < int(day)\
                or int(month2) < int(month):
            if lang == 'Русский':
                holiday_number = f'Дата: {h_numbers_2[0]}' \
                                 f' {data.holidays_month[d_m_2[1]]} -' \
                                 f' {h_numbers_2[1]}' \
                                 f' {data.holidays_month[d_m_2[3]]}' \
                                 f' {year + 1} годa,' \
                                 f' {data.hdays_of_7[d_m_2[0]]} -' \
                                 f' {data.hdays_of_7[d_m_2[2]]}'
            elif lang == 'English':
                holiday_number = f'Date: {h_numbers_2[0]}' \
                                 f' {data.holidays_month_en[d_m_2[1]]} -' \
                                 f' {h_numbers_2[1]}' \
                                 f' {data.holidays_month_en[d_m_2[3]]}' \
                                 f' {year + 1} year,' \
                                 f' {data.hdays_of_7_en[d_m_2[0]]} -' \
                                 f' {data.hdays_of_7_en[d_m_2[2]]}'
        elif month == 1 and holidays_dict['name'] == 'AsarahBTevet'\
                or month == 1 and holidays_dict['name'] == 'Chanukah':
            if lang == 'Русский':
                holiday_number = f'Дата: {h_numbers_2[0]}' \
                                 f' {data.holidays_month[d_m_2[1]]} -' \
                                 f' {h_numbers_2[1]}' \
                                 f' {data.holidays_month[d_m_2[3]]}' \
                                 f' {year} годa,' \
                                 f' {data.hdays_of_7[d_m_2[0]]} -' \
                                 f' {data.hdays_of_7[d_m_2[2]]}'
            elif lang == 'English':
                holiday_number = f'Date: {h_numbers_2[0]}' \
                                 f' {data.holidays_month_en[d_m_2[1]]} -' \
                                 f' {h_numbers_2[1]}' \
                                 f' {data.holidays_month_en[d_m_2[3]]}' \
                                 f' {year} year,' \
                                 f' {data.hdays_of_7_en[d_m_2[0]]} -' \
                                 f' {data.hdays_of_7_en[d_m_2[2]]}'
        elif month2 == 13:
            if lang == 'Русский':
                holiday_number = f'Дата: {h_numbers[0]}' \
                                 f' {data.holidays_month[d_m[1]]} -' \
                                 f' {h_numbers[1]}' \
                                 f' {data.holidays_month[d_m[3]]}' \
                                 f' {year + 1} годa,' \
                                 f' {data.hdays_of_7[d_m[0]]} -' \
                                 f' {data.hdays_of_7[d_m[2]]}'
            elif lang == 'English':
                holiday_number = f'Date: {h_numbers[0]}' \
                                 f' {data.holidays_month_en[d_m[1]]} -' \
                                 f' {h_numbers[1]}' \
                                 f' {data.holidays_month_en[d_m[3]]}' \
                                 f' {year + 1} year,' \
                                 f' {data.hdays_of_7_en[d_m[0]]} -' \
                                 f' {data.hdays_of_7_en[d_m[2]]}'
        else:
            if lang == 'Русский':
                holiday_number = f'Дата: {h_numbers[0]}' \
                                 f' {data.holidays_month[d_m[1]]} -' \
                                 f' {h_numbers[1]}' \
                                 f' {data.holidays_month[d_m[3]]}' \
                                 f' {year} годa,' \
                                 f' {data.hdays_of_7[d_m[0]]} -' \
                                 f' {data.hdays_of_7[d_m[2]]}'
            elif lang == 'English':
                holiday_number = f'Date: {h_numbers[0]}' \
                                 f' {data.holidays_month_en[d_m[1]]} -' \
                                 f' {h_numbers[1]}' \
                                 f' {data.holidays_month_en[d_m[3]]}' \
                                 f' {year} year,' \
                                 f' {data.hdays_of_7_en[d_m[0]]} -' \
                                 f' {data.hdays_of_7_en[d_m[2]]}'
    else:
        day1 = h_numbers[0]
        month1 = data.holidays_month_index[d_m[1]]
        if brackets:
            month1 = 13
        if int(month1) < int(month) or int(month1) == int(month)\
                and int(day) > int(day1):
            if lang == 'Русский':
                holiday_number = f'Дата: {h_numbers_2[0]}' \
                                 f' {data.holidays_month[d_m_2[1]]},' \
                                 f' {year + 1} годa,' \
                                 f' {data.hdays_of_7[d_m_2[0]]}'
            elif lang == 'English':
                holiday_number = f'Date: {h_numbers_2[0]}' \
                                 f' {data.holidays_month_en[d_m_2[1]]},' \
                                 f' {year + 1} year,' \
                                 f' {data.hdays_of_7_en[d_m_2[0]]}'
        elif month == 1 and holidays_dict['name'] == 'AsarahBTevet' \
                or holidays_dict['name'] == 'Chanukah':
            if lang == 'Русский':
                holiday_number = f'Дата: {h_numbers_2[0]}' \
                                 f' {data.holidays_month[d_m_2[1]]},' \
                                 f' {year} годa,' \
                                 f' {data.hdays_of_7[d_m_2[0]]}'
            elif lang == 'English':
                holiday_number = f'Date: {h_numbers_2[0]}' \
                                 f' {data.holidays_month_en[d_m_2[1]]},' \
                                 f' {year} year,' \
                                 f' {data.hdays_of_7_en[d_m_2[0]]}'
        elif month1 == 13:
                if lang == 'Русский':
                    holiday_number = f'Дата: {h_numbers[0]}' \
                                     f' {data.holidays_month[d_m[1]]},' \
                                     f' {year + 1} годa,' \
                                     f' {data.hdays_of_7[d_m[0]]}'
                elif lang == 'English':
                    holiday_number = f'Date: {h_numbers[0]}' \
                                     f' {data.holidays_month_en[d_m[1]]},' \
                                     f' {year + 1} year,' \
                                     f' {data.hdays_of_7_en[d_m[0]]}'
        else:
            if lang == 'Русский':
                holiday_number = f'Дата: {h_numbers[0]}' \
                                 f' {data.holidays_month[d_m[1]]},' \
                                 f' {year} годa,' \
                                 f' {data.hdays_of_7[d_m[0]]}'
            elif lang == 'English':
                holiday_number = f'Date: {h_numbers[0]}' \
                                 f' {data.holidays_month_en[d_m[1]]},' \
                                 f' {year} year,' \
                                 f' {data.hdays_of_7_en[d_m[0]]}'
    return holiday_number


# Начало и конец поста
def fast(get_dict, loc, lang):
    tz = f.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    year = now.year
    month = now.month
    day = now.day
    h_numbers = re.findall(r'\d+', get_dict['dateYear1'])
    d_m = re.findall(r'[a-zA-z]+', get_dict['dateYear1'])
    h_numbers_2 = re.findall(r'\d+', get_dict['dateYear2'])
    d_m_2 = re.findall(r'[a-zA-z]+', get_dict['dateYear2'])
    brackets = re.findall(r'[(){}[\]]+', get_dict['dateYear1'])

    month_time = data.holidays_month_index[d_m[1]]
    if brackets:
        month_time = 13
    if int(month_time) < int(month) or int(month_time) == int(month)\
            and int(h_numbers[0]) < int(day):
        month_time = data.holidays_month_index[d_m_2[1]]
        day_time = h_numbers_2[0]
    else:
        day_time = h_numbers[0]
        month_time = data.holidays_month_index[d_m[1]]
    holiday_time = requests.get(
        f'{URL}/getCalendarData.php?mode=day&timezone='
        f'{tz}&dateBegin={month_time}/{day_time}/{year}'
        f'&lat={loc[0]}&lng={loc[1]}&havdala_offset=72')

    holi_time_dict = holiday_time.json()
    earlier_time = datetime.strptime(holi_time_dict['zmanim']['sunset'],
                                     "%H:%M:%S")
    earlier_delta = timedelta(minutes=31)
    earlier_delta2 = timedelta(minutes=28)
    earlier_delta3 = timedelta(minutes=25)
    sefer_ben_ashmashot = str(datetime.time(earlier_time + earlier_delta))
    nevareshet = str(datetime.time(earlier_time + earlier_delta2))
    shmirat_shabat = str(datetime.time(earlier_time + earlier_delta3))
    fast_time = ''
    if get_dict['name'] == 'TishaBAv':
        delta = timedelta(days=1)
        date1 = datetime.strptime(f'{month_time}/{day_time}/{year}',
                                  '%m/%d/%Y')
        d1 = date1 - delta
        spec_date = re.findall(r'\d+', str(d1))
        holiday_time_av = requests.get(
            f'{URL}/getCalendarData.php?mode=day&timezone='
            f'{tz}&dateBegin={spec_date[1]}/{spec_date[2]}/{spec_date[0]}'
            f'&lat={loc[0]}&lng={loc[1]}&havdala_offset=72')
        holi_time_dict_av = holiday_time_av.json()
        if lang == 'Русский':
            fast_time = 'Начало поста: {}' \
                        ' {}' \
                        ' {:.5s}\n' \
                        'Конец поста: {}' \
                        ' {}\n' \
                        'Самый ранний выход звезд' \
                        ' {:.5s}\n' \
                        'Сефер бен Ашмашот: {:.5s}\n' \
                        'Неварешет: {:.5s}\n' \
                        'Шмират шаббат килхата: {:.5s}'\
                .format(spec_date[2],
                        data.gr_months_index[str(spec_date[1])],
                        holi_time_dict_av["zmanim"]["sunset"],
                        day_time, data.gr_months_index[month_time],
                        holi_time_dict["zmanim"]["tzeis_595_degrees"],
                        sefer_ben_ashmashot, nevareshet, shmirat_shabat)
        elif lang == 'English':
            fast_time = 'Fast begins: {}' \
                        ' {}' \
                        ' {:.5s}\n' \
                        'The fast ends: {}' \
                        ' {}\n' \
                        'Earlier time of tzeit akohavim' \
                        ' {:.5s}\n' \
                        'Sefer ben Ashmashot: {:.5s}\n' \
                        'Nevareshet: {:.5s}\n' \
                        'Shmirat shabbat kelhata: {:.5s}'\
                .format(spec_date[2],
                        data.gr_months_index_en[str(spec_date[1])],
                        holi_time_dict_av["zmanim"]["sunset"],
                        day_time, data.gr_months_index_en[month_time],
                        holi_time_dict["zmanim"]["tzeis_595_degrees"],
                        sefer_ben_ashmashot, nevareshet, shmirat_shabat)
    elif get_dict['name'] == 'ShivaAsarBTammuz':
        chazot_time = datetime.strptime(holi_time_dict['zmanim']['chatzos'],
                                        "%H:%M:%S")
        d_delta = timedelta(hours=12)
        dtime = chazot_time - d_delta

        chazot_fast = str(datetime.time(dtime))
        if lang == 'Русский':
            fast_time = 'Начало поста: {}' \
                        ' {}' \
                        ' {:.5s}\n' \
                        'Конец поста: {}' \
                        ' {}\n' \
                        'Самый ранний выход звезд' \
                        ' {:.5s}\n' \
                        'Сефер бен Ашмашот: {:.5s}\n' \
                        'Неварешет: {:.5s}\n' \
                        'Шмират шаббат килхата: {:.5s}'\
                .format(day_time,
                        data.gr_months_index[month_time],
                        chazot_fast,
                        day_time, data.gr_months_index[month_time],
                        holi_time_dict["zmanim"]["tzeis_595_degrees"],
                        sefer_ben_ashmashot, nevareshet, shmirat_shabat)
        elif lang == 'English':
            fast_time = 'The fast begins: {}' \
                        ' {}' \
                        ' {:.5s}\n' \
                        'Fast ends: {}' \
                        ' {}\n' \
                        'Earlier time of tzeit akohavim' \
                        ' {:.5s}\n' \
                        'Sefer ben Ashmashot: {:.5s}\n' \
                        'Nevareshet: {:.5s}\n' \
                        'Shmirat shabbat kelhata: {:.5s}'\
                .format(day_time,
                        data.gr_months_index_en[month_time],
                        chazot_fast,
                        day_time, data.gr_months_index_en[month_time],
                        holi_time_dict["zmanim"]["tzeis_595_degrees"],
                        sefer_ben_ashmashot, nevareshet, shmirat_shabat)
    else:
        if lang == 'Русский':
            fast_time = 'Начало поста: {}' \
                        ' {}' \
                        ' {:.5s}\n' \
                        'Конец поста: {}' \
                        ' {}\n' \
                        'Самый ранний выход звезд' \
                        ' {:.5s}\n' \
                        'Сефер бен Ашмашот: {:.5s}\n' \
                        'Неварешет: {:.5s}\n' \
                        'Шмират шаббат килхата: {:.5s}'\
                .format(day_time,
                        data.gr_months_index[month_time],
                        holi_time_dict["zmanim"]["alos_ma"],
                        day_time, data.gr_months_index[month_time],
                        holi_time_dict["zmanim"]["tzeis_595_degrees"],
                        sefer_ben_ashmashot, nevareshet, shmirat_shabat)
        elif lang == 'English':
            fast_time = 'The fast begins: {}' \
                        ' {}' \
                        ' {:.5s}\n' \
                        'Fast ends: {}' \
                        ' {}\n' \
                        'Earlier time of tzeit akohavim' \
                        ' {:.5s}\n' \
                        'Sefer ben Ashmashot: {:.5s}\n' \
                        'Nevareshet: {:.5s}\n' \
                        'Shmirat shabbat kelhata: {:.5s}'\
                .format(day_time,
                        data.gr_months_index_en[month_time],
                        holi_time_dict["zmanim"]["alos_ma"],
                        day_time, data.gr_months_index_en[month_time],
                        holi_time_dict["zmanim"]["tzeis_595_degrees"],
                        sefer_ben_ashmashot, nevareshet, shmirat_shabat)

    return fast_time


# Время зажигания и Авдолы Рош-Ашана, Шавуота
def rosh_ash_shavout(get_dict, loc, lang):
    tz = f.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    year = now.year
    month = now.month
    day = now.day
    h_numbers = re.findall(r'\d+', get_dict['dateYear1'])
    d_m = re.findall(r'[a-zA-z]+', get_dict['dateYear1'])
    h_numbers_2 = re.findall(r'\d+', get_dict['dateYear2'])
    d_m_2 = re.findall(r'[a-zA-z]+', get_dict['dateYear2'])

    month_time = data.holidays_month_index[d_m[1]]
    if month_time < month or month_time == month\
            and int(h_numbers[0]) < int(day):
        month_time = data.holidays_month_index[d_m_2[1]]
        day_time = h_numbers_2[0]
    else:
        day_time = h_numbers[0]
        month_time = data.holidays_month_index[d_m[1]]
    holiday_time = requests.get(
        f'{URL}/getCalendarData.php?mode=day&timezone='
        f'{tz}&dateBegin={month_time}/{day_time}/{year}'
        f'&lat={loc[0]}&lng={loc[1]}&havdala_offset=72')

    holi_time_dict = holiday_time.json()

    date1 = datetime.strptime(f'{month_time}/{day_time}/{year}', '%m/%d/%Y')
    delta1 = timedelta(days=1)
    delta2 = timedelta(days=2)
    d1 = date1 - delta1
    d2 = date1 + delta1
    d3 = date1 + delta2
    spec_date1 = re.findall(r'\d+', str(d1))
    spec_date2 = re.findall(r'\d+', str(d2))
    spec_date3 = re.findall(r'\d+', str(d3))
    holiday_time_ra1 = requests.get(
        f'{URL}/getCalendarData.php?mode=day&timezone='
        f'{tz}&dateBegin={spec_date1[1]}/{spec_date1[2]}/{spec_date1[0]}'
        f'&lat={loc[0]}&lng={loc[1]}&havdala_offset=72')
    holiday_time_ra2 = requests.get(
        f'{URL}/getCalendarData.php?mode=day&timezone='
        f'{tz}&dateBegin={spec_date2[1]}/{spec_date2[2]}/{spec_date2[0]}'
        f'&lat={loc[0]}&lng={loc[1]}&havdala_offset=72')
    holiday_time_ra3 = requests.get(
        f'{URL}/getCalendarData.php?mode=day&timezone='
        f'{tz}&dateBegin={spec_date3[1]}/{spec_date3[2]}/{spec_date3[0]}'
        f'&lat={loc[0]}&lng={loc[1]}&havdala_offset=72')

    holi_time_dict_ra1 = holiday_time_ra1.json()
    holi_time_dict_ra2 = holiday_time_ra2.json()
    holi_time_dict_ra3 = holiday_time_ra3.json()
    d_candle = datetime.strptime(holi_time_dict_ra1['zmanim']['sunset'],
                                 "%H:%M:%S")
    d_candle2 = datetime.strptime(holi_time_dict_ra2['zmanim']['sunset'],
                                  "%H:%M:%S")
    d_delta = timedelta(minutes=18)
    ra_time = ''
    if holi_time_dict['dayOfWeek'] == '4':
        if lang == 'Русский':
            ra_time = 'Зажигание свечей: {}' \
                      ' {}' \
                      ' {:.5s}\n' \
                      'Зажигание свечей: {}' \
                      ' {}' \
                      ' {:.5s}\n' \
                      'Зажигание свечей (Шаббат): {}' \
                      ' {}' \
                      ' {:.5s}\n' \
                      'Авдала: {}' \
                      ' {}' \
                      ' {:.5s}'\
                .format(spec_date1[2],
                        data.gr_months_index[str(spec_date1[1])],
                        str(datetime.time(d_candle - d_delta)), day_time,
                        data.gr_months_index[month_time],
                        holi_time_dict["zmanim"]["tzeis_850_degrees"],
                        spec_date2[2],
                        data.gr_months_index[str(spec_date2[1])],
                        str(datetime.time(d_candle2 - d_delta)),
                        spec_date3[2],
                        data.gr_months_index[str(spec_date3[1])],
                        holi_time_dict_ra3["zmanim"]["tzeis_850_degrees"])
        elif lang == 'English':
            ra_time = 'Candle lighting: {}' \
                      ' {}' \
                      ' {:.5s}\n' \
                      'Candle lighting: {}' \
                      ' {}' \
                      ' {:.5s}\n' \
                      'Candle lighting: {}' \
                      ' {} ' \
                      '{:.5s}\n' \
                      'Avdala: {}' \
                      ' {}' \
                      ' {:.5s}'\
                .format(spec_date1[2],
                        data.gr_months_index_en[str(spec_date1[1])],
                        str(datetime.time(d_candle - d_delta)), day_time,
                        data.gr_months_index_en[month_time],
                        holi_time_dict["zmanim"]["tzeis_850_degrees"],
                        spec_date2[2],
                        data.gr_months_index_en[str(spec_date2[1])],
                        str(datetime.time(d_candle2 - d_delta)),
                        spec_date3[2],
                        data.gr_months_index_en[str(spec_date3[1])],
                        holi_time_dict_ra3["zmanim"]["tzeis_850_degrees"])
    else:
        if lang == 'Русский':
            ra_time = 'Зажигание свечей: {}' \
                      ' {}' \
                      ' {:.5s}\n' \
                      'Зажигание свечей: {}' \
                      ' {}' \
                      ' {:.5s}\n' \
                      'Авдала: {}' \
                      ' {}' \
                      ' {:.5s}'\
                .format(spec_date1[2],
                        data.gr_months_index[str(spec_date1[1])],
                        str(datetime.time(d_candle - d_delta)), day_time,
                        data.gr_months_index[month_time],
                        holi_time_dict["zmanim"]["tzeis_850_degrees"],
                        spec_date2[2],
                        data.gr_months_index[str(spec_date2[1])],
                        holi_time_dict_ra2["zmanim"]["tzeis_850_degrees"])
        elif lang == 'English':
            ra_time = 'Candle lighting: {}' \
                      ' {}' \
                      ' {:.5s}\n' \
                      'Candle lighting: {}' \
                      ' {}' \
                      ' {:.5s}\n' \
                      'Avdala: {}' \
                      ' {}' \
                      ' {:.5s}'\
                .format(spec_date1[2],
                        data.gr_months_index_en[str(spec_date1[1])],
                        str(datetime.time(d_candle - d_delta)), day_time,
                        data.gr_months_index_en[month_time],
                        holi_time_dict["zmanim"]["tzeis_850_degrees"],
                        spec_date2[2],
                        data.gr_months_index_en[str(spec_date2[1])],
                        holi_time_dict_ra2["zmanim"]["tzeis_850_degrees"])

    return ra_time


# Время зажигания и Авдолы Йом-Кипура
def yom_kippurim(get_dict, loc, lang):
    tz = f.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    year = now.year
    month = now.month
    day = now.day
    h_numbers = re.findall(r'\d+', get_dict['dateYear1'])
    d_m = re.findall(r'[a-zA-z]+', get_dict['dateYear1'])
    h_numbers_2 = re.findall(r'\d+', get_dict['dateYear2'])
    d_m_2 = re.findall(r'[a-zA-z]+', get_dict['dateYear2'])

    month_time = data.holidays_month_index[d_m[1]]
    if month_time < month or month_time == month\
            and int(h_numbers[0]) < int(day):
        month_time = data.holidays_month_index[d_m_2[1]]
        day_time = h_numbers_2[0]
    else:
        day_time = h_numbers[0]
        month_time = data.holidays_month_index[d_m[1]]
    holiday_time = requests.get(
        f'{URL}/getCalendarData.php?mode=day&timezone='
        f'{tz}&dateBegin={month_time}/{day_time}/{year}'
        f'&lat={loc[0]}&lng={loc[1]}&havdala_offset=72')
    holi_time_dict = holiday_time.json()

    delta = timedelta(days=1)
    date1 = datetime.strptime(f'{month_time}/{day_time}/{year}', '%m/%d/%Y')
    d1 = date1 - delta
    spec_date = re.findall(r'\d+', str(d1))
    holiday_time_candle = requests.get(
        f'{URL}/getCalendarData.php?mode=day&timezone='
        f'{tz}&dateBegin={spec_date[1]}/{spec_date[2]}/{spec_date[0]}'
        f'&lat={loc[0]}&lng={loc[1]}&havdala_offset=72')
    holi_time_dict_candle = holiday_time_candle.json()

    d1 = datetime.strptime(holi_time_dict_candle['zmanim']['sunset'],
                           "%H:%M:%S")
    d_delta = timedelta(minutes=18)
    fast_time = ''
    if lang == 'Русский':
        fast_time = 'Зажигание свечей и начало поста: {}' \
                    ' {}' \
                    ' {:.5s}\n' \
                    'Авдала и конец поста: {}' \
                    ' {}' \
                    ' {:.5s}'\
            .format(spec_date[2], data.gr_months_index[str(spec_date[1])],
                    str(datetime.time(d1 - d_delta)), day_time,
                    data.gr_months_index[month_time],
                    holi_time_dict["zmanim"]["tzeis_850_degrees"])
    elif lang == 'English':
        fast_time = 'Candle lighting and the fast begins: {}' \
                    ' {}' \
                    ' {:.5s}\n' \
                    'Avdala and the fast ends: {}' \
                    ' {}' \
                    ' {:.5s}'\
            .format(spec_date[2], data.gr_months_index_en[str(spec_date[1])],
                    str(datetime.time(d1 - d_delta)), day_time,
                    data.gr_months_index_en[month_time],
                    holi_time_dict["zmanim"]["tzeis_850_degrees"])

    return fast_time


# Время зажигания и Авдолы Пейсаха и Суккота
def pesach_sukkot(get_dict, number, loc, lang):
    tz = f.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    year = now.year
    month = now.month
    day = now.day
    israel = False
    if tz == 'Asia/Jerusalem' or tz == 'Asia/Tel_Aviv' or tz == 'Asia/Hebron':
        israel = True
    h_numbers = re.findall(r'\d+', get_dict['dateYear1'])
    d_m = re.findall(r'[a-zA-z]+', get_dict['dateYear1'])
    h_numbers_2 = re.findall(r'\d+', get_dict['dateYear2'])
    d_m_2 = re.findall(r'[a-zA-z]+', get_dict['dateYear2'])
    if get_dict['name'] == 'Pesach':
        month_time = data.holidays_month_index[d_m[3]]
    else:
        month_time = data.holidays_month_index[d_m[1]]
    day_time = ''
    if number == 1:
        if month_time < month or month_time == month \
                and int(h_numbers[1]) < int(day):
            month_time = data.holidays_month_index[d_m_2[1]]
            day_time = h_numbers_2[0]
        else:
            day_time = h_numbers[0]
            month_time = data.holidays_month_index[d_m[1]]
    elif number == 2:
        if month_time < month or month_time == month\
                and int(h_numbers[1]) < int(day):
            month_time = data.holidays_month_index[d_m_2[3]]
            day_time = h_numbers_2[1]
        else:
            day_time = h_numbers[1]
            month_time = data.holidays_month_index[d_m[3]]
    holiday_time = requests.get(
        f'{URL}/getCalendarData.php?mode=day&timezone='
        f'{tz}&dateBegin={month_time}/{day_time}/{year}'
        f'&lat={loc[0]}&lng={loc[1]}&havdala_offset=72')

    holi_time_dict = holiday_time.json()

    date1 = datetime.strptime(f'{month_time}/{day_time}/{year}', '%m/%d/%Y')
    delta1 = timedelta(days=1)
    delta2 = timedelta(days=2)
    d1 = date1 - delta1
    d2 = date1 + delta1
    d3 = date1 + delta2
    spec_date1 = re.findall(r'\d+', str(d1))
    spec_date2 = re.findall(r'\d+', str(d2))
    spec_date3 = re.findall(r'\d+', str(d3))
    holiday_time_ra1 = requests.get(
        f'{URL}/getCalendarData.php?mode=day&timezone='
        f'{tz}&dateBegin={spec_date1[1]}/{spec_date1[2]}/{spec_date1[0]}'
        f'&lat={loc[0]}&lng={loc[1]}&havdala_offset=72')
    holiday_time_ra2 = requests.get(
        f'{URL}/getCalendarData.php?mode=day&timezone='
        f'{tz}&dateBegin={spec_date2[1]}/{spec_date2[2]}/{spec_date2[0]}'
        f'&lat={loc[0]}&lng={loc[1]}&havdala_offset=72')
    holiday_time_ra3 = requests.get(
        f'{URL}/getCalendarData.php?mode=day&timezone='
        f'{tz}&dateBegin={spec_date3[1]}/{spec_date3[2]}/{spec_date3[0]}'
        f'&lat={loc[0]}&lng={loc[1]}&havdala_offset=72')
    holi_time_dict_ra1 = holiday_time_ra1.json()
    holi_time_dict_ra2 = holiday_time_ra2.json()
    holi_time_dict_ra3 = holiday_time_ra3.json()
    d_candle = datetime.strptime(holi_time_dict_ra1['zmanim']['sunset'],
                                 "%H:%M:%S")
    d_candle2 = datetime.strptime(holi_time_dict_ra2['zmanim']['sunset'],
                                  "%H:%M:%S")
    d_delta = timedelta(minutes=18)
    ra_time = ''
    # проверка на израиль
    if not israel:
        if holi_time_dict['dayOfWeek'] == '4':
            if lang == 'Русский':
                ra_time = 'Зажигание свечей: {}' \
                          ' {}' \
                          ' {:.5s}\n' \
                          'Зажигание свечей: {}' \
                          ' {}' \
                          ' {:.5s}\n' \
                          'Зажигание свечей (Шаббат): {}' \
                          ' {} ' \
                          '{:.5s}\n' \
                          'Авдала: {}' \
                          ' {}' \
                          ' {:.5s}'\
                    .format(spec_date1[2],
                            data.gr_months_index[str(spec_date1[1])],
                            str(datetime.time(d_candle - d_delta)),
                            day_time,
                            data.gr_months_index[month_time],
                            holi_time_dict["zmanim"]["tzeis_850_degrees"],
                            spec_date2[2],
                            data.gr_months_index[str(spec_date2[1])],
                            str(datetime.time(d_candle2 - d_delta)),
                            spec_date3[2],
                            data.gr_months_index[str(spec_date3[1])],
                            holi_time_dict_ra3["zmanim"]["tzeis_850_degrees"])
            elif lang == 'English':
                ra_time = 'Candle lighting: {}' \
                          ' {}' \
                          ' {:.5s}\n' \
                          'Candle lighting: {}' \
                          ' {}' \
                          ' {:.5s}\n' \
                          'Candle lighting: {}' \
                          ' {} ' \
                          '{:.5s}\n' \
                          'Avdala: {}' \
                          ' {}' \
                          ' {:.5s}'\
                    .format(spec_date1[2],
                            data.gr_months_index_en[str(spec_date1[1])],
                            str(datetime.time(d_candle - d_delta)),
                            day_time,
                            data.gr_months_index_en[month_time],
                            holi_time_dict["zmanim"]["tzeis_850_degrees"],
                            spec_date2[2],
                            data.gr_months_index_en[str(spec_date2[1])],
                            str(datetime.time(d_candle2 - d_delta)),
                            spec_date3[2],
                            data.gr_months_index_en[str(spec_date3[1])],
                            holi_time_dict_ra3["zmanim"]["tzeis_850_degrees"])
        else:
            if lang == 'Русский':
                ra_time = 'Зажигание свечей: {}' \
                          ' {}' \
                          ' {:.5s}\n' \
                          'Зажигание свечей: {}' \
                          ' {}' \
                          ' {:.5s}\n' \
                          'Авдала: {}' \
                          ' {}' \
                          ' {:.5s}'\
                    .format(spec_date1[2],
                            data.gr_months_index[str(spec_date1[1])],
                            str(datetime.time(d_candle - d_delta)),
                            day_time, data.gr_months_index[month_time],
                            holi_time_dict["zmanim"]["tzeis_850_degrees"],
                            spec_date2[2],
                            data.gr_months_index[str(spec_date2[1])],
                            holi_time_dict_ra2["zmanim"]["tzeis_850_degrees"])
            elif lang == 'English':
                ra_time = 'Candle lighting: {}' \
                          ' {}' \
                          ' {:.5s}\n' \
                          'Candle lighting: {}' \
                          ' {}' \
                          ' {:.5s}\n' \
                          'Avdala: {}' \
                          ' {}' \
                          ' {:.5s}'\
                    .format(spec_date1[2],
                            data.gr_months_index_en[str(spec_date1[1])],
                            str(datetime.time(d_candle - d_delta)),
                            day_time, data.gr_months_index_en[month_time],
                            holi_time_dict["zmanim"]["tzeis_850_degrees"],
                            spec_date2[2],
                            data.gr_months_index_en[str(spec_date2[1])],
                            holi_time_dict_ra2["zmanim"]["tzeis_850_degrees"])
    else:
        if lang == 'Русский':
            ra_time = 'Зажигание свечей: {}' \
                      ' {}' \
                      ' {:.5s}\n' \
                      'Авдала: {}' \
                      ' {}' \
                      ' {:.5s}'\
                .format(spec_date1[2],
                        data.gr_months_index[str(spec_date1[1])],
                        str(datetime.time(d_candle - d_delta)),
                        day_time, data.gr_months_index[month_time],
                        holi_time_dict["zmanim"]["tzeis_850_degrees"])
        elif lang == 'English':
            ra_time = 'Candle lighting: {}' \
                      ' {}' \
                      ' {:.5s}\n' \
                      'Avdala: {}' \
                      ' {}' \
                      ' {:.5s}'\
                .format(spec_date1[2],
                        data.gr_months_index_en[str(spec_date1[1])],
                        str(datetime.time(d_candle - d_delta)),
                        day_time, data.gr_months_index_en[month_time],
                        holi_time_dict["zmanim"]["tzeis_850_degrees"])

    return ra_time


index = get_holidays_dict


def tu_bshevat(loc, lang):
    tu_bshevat_name = get_holiday_name(index(0, loc), lang)
    tu_bshevat_date = get_holiday_data(index(0, loc), loc, lang)
    tu_bshevat_str = f'{tu_bshevat_name}\n' \
                     f'{tu_bshevat_date}'
    return tu_bshevat_str


def taanit_esther(loc, lang):
    taanit_esther_name = get_holiday_name(index(1, loc), lang)
    taanit_esther_date = get_holiday_data(index(1, loc), loc, lang)
    taanit_esther_time = fast(index(1, loc), loc, lang)
    taanit_esther_str = f'{taanit_esther_name}\n' \
                        f'{taanit_esther_date}\n' \
                        f'{taanit_esther_time}'
    return taanit_esther_str


def purim(loc, lang):
    purim_name = get_holiday_name(index(2, loc), lang)
    purim_date = get_holiday_data(index(2, loc), loc, lang)
    shushan_purim_name = get_holiday_name(index(3, loc), lang)
    shushan_purim_date = get_holiday_data(index(3, loc), loc, lang)
    purim_str = f'{purim_name}\n' \
                f'{purim_date}\n\n' \
                f'{shushan_purim_name}\n' \
                f'{shushan_purim_date}'
    return purim_str


def pesach(loc, lang):
    pesach_name = get_holiday_name(index(4, loc), lang)
    pesach_date = get_holiday_data(index(4, loc), loc, lang)
    pesach_time = pesach_sukkot(index(4, loc), 1, loc, lang)
    pesach_time2 = pesach_sukkot(index(4, loc), 2, loc, lang)
    pesach_str = f'{pesach_name}\n' \
                 f'{pesach_date}\n' \
                 f'{pesach_time}\n\n' \
                 f'{pesach_time2}'
    return pesach_str


def get_israel(loc, lang):
    yom_hashoah_name = get_holiday_name(index(5, loc), lang)
    yom_hashoah_date = get_holiday_data(index(5, loc), loc, lang)
    yom_hazikaron_name = get_holiday_name(index(6, loc), lang)
    yom_hazikaron_date = get_holiday_data(index(6, loc), loc, lang)
    yom_haatzmaut_name = get_holiday_name(index(7, loc), lang)
    yom_haatzmaut_date = get_holiday_data(index(7, loc), loc, lang)
    yom_yerushalayim_name = get_holiday_name(index(9, loc), lang)
    yom_yerushalayim_date = get_holiday_data(index(9, loc), loc, lang)
    israel_str = f'{yom_hashoah_name}\n' \
                 f'{yom_hashoah_date}\n\n' \
                 f'{yom_hazikaron_name}\n' \
                 f'{yom_hazikaron_date}\n\n' \
                 f'{yom_haatzmaut_name}\n' \
                 f'{yom_haatzmaut_date}\n\n' \
                 f'{yom_yerushalayim_name}\n' \
                 f'{yom_yerushalayim_date}'
    return israel_str


def lag_baomer(loc, lang):
    lag_baomer_name = get_holiday_name(index(8, loc), lang)
    lag_baomer_date = get_holiday_data(index(8, loc), loc, lang)
    lag_baomer_str = f'{lag_baomer_name}\n' \
                     f'{lag_baomer_date}'
    return lag_baomer_str


def shavuot(loc, lang):
    shavuot_name = get_holiday_name(index(10, loc), lang)
    shavuot_date = get_holiday_data(index(10, loc), loc, lang)
    shavuot_time = rosh_ash_shavout(index(10, loc), loc, lang)
    shavuot_str = f'{shavuot_name}\n' \
                  f'{shavuot_date}\n' \
                  f'{shavuot_time}'
    return shavuot_str


def shiva_asar_tammuz(loc, lang):
    shiva_asar_tammuz_name = get_holiday_name(index(11, loc), lang)
    shiva_asar_tammuz_date = get_holiday_data(index(11, loc), loc, lang)
    shiva_asar_tammuz_time = fast(index(11, loc), loc, lang)
    shiva_asar_tammuz_str = f'{shiva_asar_tammuz_name}\n' \
                            f'{shiva_asar_tammuz_date}\n' \
                            f'{shiva_asar_tammuz_time}'
    return shiva_asar_tammuz_str


def tisha_bav(loc, lang):
    tisha_bav_name = get_holiday_name(index(12, loc), lang)
    tisha_bav_date = get_holiday_data(index(12, loc), loc, lang)
    tisha_bav_time = fast(index(12, loc), loc, lang)
    tisha_bav_str = f'{tisha_bav_name}\n' \
                    f'{tisha_bav_date}\n' \
                    f'{tisha_bav_time}'
    return tisha_bav_str


def tu_bav(loc, lang):
    tu_bav_name = get_holiday_name(index(13, loc), lang)
    tu_bav_date = get_holiday_data(index(13, loc), loc, lang)
    tu_bav_str = f'{tu_bav_name}\n' \
                 f'{tu_bav_date}'
    return tu_bav_str


def rosh_hashanah(loc, lang):
    rosh_hashanah_name = get_holiday_name(index(14, loc), lang)
    time.sleep(1)
    rosh_date = get_holiday_data(index(14, loc), loc, lang)
    time.sleep(1)
    rosh_time = rosh_ash_shavout(index(14, loc), loc, lang)
    rosh_hashanah_str = f'{rosh_hashanah_name}\n' \
                        f'{rosh_date}\n' \
                        f'{rosh_time}'
    return rosh_hashanah_str


def tzom_gedaliah(loc, lang):
    time.sleep(5)
    tzom_gedaliah_name = get_holiday_name(index(15, loc), lang)
    time.sleep(5)
    tzom_gedaliah_date = get_holiday_data(index(15, loc), loc, lang)
    time.sleep(5)
    tzom_gedaliah_time = fast(index(15, loc), loc, lang)
    time.sleep(5)
    tzom_gedaliah_str = f'{tzom_gedaliah_name}\n' \
                        f'{tzom_gedaliah_date}\n' \
                        f'{tzom_gedaliah_time}'
    return tzom_gedaliah_str


def yom_kipur(loc, lang):
    yom_kippur_name = get_holiday_name(index(16, loc), lang)
    yom_kippur_date = get_holiday_data(index(16, loc), loc, lang)
    yom_kippur_time = yom_kippurim(index(16, loc), loc, lang)
    yom_kippur_str = f'{yom_kippur_name}\n' \
                     f'{yom_kippur_date}\n' \
                     f'{yom_kippur_time}'
    return yom_kippur_str


def succos(loc, lang):
    succos_name = get_holiday_name(index(17, loc), lang)
    succos_date = get_holiday_data(index(17, loc), loc, lang)
    succos_time = pesach_sukkot(index(21, loc), 1, loc, lang)
    hoshana_rabba_name = get_holiday_name(index(18, loc), lang)
    hoshana_rabba_date = get_holiday_data(index(18, loc), loc, lang)
    succos_str = f'{succos_name}\n' \
                 f'{succos_date}\n' \
                 f'{succos_time}\n\n' \
                 f'{hoshana_rabba_name}\n' \
                 f'{hoshana_rabba_date}'
    return succos_str


def shmini_atzeres_simhat(loc, lang):
    shmini_atzeres_simhat_name = get_holiday_name(index(19, loc), lang)
    shmini_atzeres_simhat_date = get_holiday_data(index(19, loc), loc, lang)
    simhat_torah_name = get_holiday_name(index(20, loc), lang)
    simhat_torah_date = get_holiday_data(index(20, loc), loc, lang)
    shmini_simhat_time = pesach_sukkot(index(19, loc), 1, loc, lang)
    shmini_simhat_str = f'{shmini_atzeres_simhat_name}\n' \
                        f'{shmini_atzeres_simhat_date}\n' \
                        f'{simhat_torah_name}\n' \
                        f'{simhat_torah_date}\n\n' \
                        f'{shmini_simhat_time}'
    return shmini_simhat_str


# def SukkotShminiAtzeret(lang):
#     SukkotShminiAtzeret_name = get_holiday_name(index(21), lang)
#     SukkotShminiAtzeret_date = get_holiday_data(index(21), lang)
#     SukkotShminiAtzeret_str = f'{SukkotShminiAtzeret_name}\n' \
#                               f'{SukkotShminiAtzeret_date}'
#     return SukkotShminiAtzeret_str


def chanukah(loc, lang):
    chanukah_name = get_holiday_name(index(22, loc), lang)
    chanukah_date = get_holiday_data(index(22, loc), loc, lang)
    chanukah_str = f'{chanukah_name}\n' \
                   f'{chanukah_date}'
    return chanukah_str


def asarah_btevet(loc, lang):
    asarah_btevet_name = get_holiday_name(index(23, loc), lang)
    asarah_btevet_date = get_holiday_data(index(23, loc), loc, lang)
    asarah_btevet_time = fast(index(23, loc), loc, lang)
    asarah_btevet_str = f'{asarah_btevet_name}\n' \
                        f'{asarah_btevet_date}\n' \
                        f'{asarah_btevet_time}'
    return asarah_btevet_str
