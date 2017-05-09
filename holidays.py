# -*- coding: utf-8 -*-
import requests
import re
from convertdate import hebrew
from datetime import datetime
from tzlocal import get_localzone
import data


now = datetime.now()
tz = get_localzone()
hebrew_year = hebrew.from_gregorian(now.year, now.month, now.day)
holiday = dict()
URL = 'http://db.ou.org/zmanim'
year = now.year
month = now.month
day = now.day


# Получаем словарь , index - индекс в общем json'е
def get_holidays_dict(index):
    if tz == 'Asia/Jerusalem' or tz == 'Asia/Tel_Aviv' or tz == 'Asia/Hebron':
        israel = 'israelHolidays=true'
        url = f'{URL}/getHolidayCalData.php?year={now.year}&{israel}'
    else:
        url = f'{URL}/getHolidayCalData.php?year={now.year}'

    holidays = requests.get(url)
    holidays_dicts = holidays.json()
    holidays_dict = holidays_dicts[index]

    return holidays_dict


# Парсим название праздника/поста, чтобы перевести его
def get_holiday_name(holidays_dict):
    holiday = re.findall(r'[a-zA-z]+', holidays_dict['name'])
    holiday_str = f'{holiday[0]}'

    return data.holidays_name[holiday_str]


# Получаем данные по празднику
def get_holiday_data(holidays_dict):
    h_numbers = re.findall(r'\d+', holidays_dict['dateYear1'])
    d_m = re.findall(r'[a-zA-z]+', holidays_dict['dateYear1'])
    h_numbers_2 = re.findall(r'\d+', holidays_dict['dateYear2'])
    d_m_2 = re.findall(r'[a-zA-z]+', holidays_dict['dateYear2'])

    if len(h_numbers) == 2 and len(d_m) == 4 or len(d_m_2) == 4:
        day2 = h_numbers[1]
        month2 = data.holidays_month_index[d_m[3]]
        if int(month2) == int(month) and int(day2) < int(day)\
                or int(month2) < int(month):
            holiday_number = f' {year + 1} год,' \
                             f' {data.hdays_of_7[d_m_2[0]]},' \
                             f' {h_numbers_2 [0]}' \
                             f' {data.holidays_month[d_m_2[1]]}' \
                             f' - {data.hdays_of_7[d_m_2[2]]},' \
                             f' {h_numbers_2 [1]}' \
                             f' {data.holidays_month[d_m_2[3]]}'
        else:
            holiday_number = f' {year} год,' \
                             f' {data.hdays_of_7[d_m[0]]},' \
                             f' {h_numbers[0]}' \
                             f' {data.holidays_month[d_m[1]]}' \
                             f' - {data.hdays_of_7[d_m[2]]},' \
                             f' {h_numbers[1]}' \
                             f' {data.holidays_month[d_m[3]]}'
    else:
        day1 = h_numbers[0]
        month1 = data.holidays_month_index[d_m[1]]

        if int(month1) == int(month) and int(day) > int(day1)\
                or int(month1) < int(month):
            holiday_number = f' {year + 1} год,' \
                             f' {data.hdays_of_7[d_m_2[0]]},' \
                             f' {h_numbers_2[0]}' \
                             f' {data.holidays_month[d_m_2[1]]}'
        else:
            holiday_number = f' {year} год,' \
                             f' {data.hdays_of_7[d_m[0]]},' \
                             f' {h_numbers[0]}' \
                             f' {data.holidays_month[d_m[1]]}'
    return holiday_number


index = get_holidays_dict

# Преобразовываем каждый праздник/пост
TuBShevat_name = get_holiday_name(index(0))
TuBShevat_date = get_holiday_data(index(0))
TuBShevat_str = f'Название: {TuBShevat_name}\n' \
                f'Дата: {TuBShevat_date}'

TaanitEsther_name = get_holiday_name(index(1))
TaanitEsther_date = get_holiday_data(index(1))
TaanitEsther_str = f'Название: {TaanitEsther_name}\n' \
                   f'Дата: {TaanitEsther_date}'

Purim_name = get_holiday_name(index(2))
Purim_date = get_holiday_data(index(2))
ShushanPurim_name = get_holiday_name(index(3))
ShushanPurim_date = get_holiday_data(index(3))
Purim_str = f'Название: {Purim_name}\n' \
            f'Дата: {Purim_date}\n' \
            f'Название: {ShushanPurim_name}\n' \
            f'Дата: {ShushanPurim_date}'

Pesach_name = get_holiday_name(index(4))
Pesach_date = get_holiday_data(index(4))
Pesach_str = f'Название: {Pesach_name}\n' \
             f'Дата: {Pesach_date}'

YomHaShoah_name = get_holiday_name(index(5))
YomHaShoah_date = get_holiday_data(index(5))
YomHaZikaron_name = get_holiday_name(index(6))
YomHaZikaron_date = get_holiday_data(index(6))
YomHaAtzmaut_name = get_holiday_name(index(7))
YomHaAtzmaut_date = get_holiday_data(index(7))
YomYerushalayim_name = get_holiday_name(index(9))
YomYerushalayim_date = get_holiday_data(index(9))
Israel_str = f'Название: {YomHaShoah_name}\n' \
             f'Дата: {YomHaShoah_date}\n\n' \
             f'Название: {YomHaZikaron_name}\n' \
             f'Дата: {YomHaZikaron_date}\n\n' \
             f'Название: {YomHaAtzmaut_name}\n' \
             f'Дата: {YomHaAtzmaut_date}\n\n' \
             f'Название: {YomYerushalayim_name}\n' \
             f'Дата: {YomYerushalayim_date}'

LagBaOmer_name = get_holiday_name(index(8))
LagBaOmer_date = get_holiday_data(index(8))
LagBaOmer_str = f'Название: {LagBaOmer_name}\n' \
                f'Дата: {LagBaOmer_date}'

Shavuot_name = get_holiday_name(index(10))
Shavuot_date = get_holiday_data(index(10))
Shavuot_str = f'Название: {Shavuot_name}\n' \
              f'Дата: {Shavuot_date}'

ShivaAsarBTammuz_name = get_holiday_name(index(11))
ShivaAsarBTammuz_date = get_holiday_data(index(11))
ShivaAsarBTammuz_str = f'Название: {ShivaAsarBTammuz_name}\n' \
                       f'Дата: {ShivaAsarBTammuz_date}'

TishaBAv_name = get_holiday_name(index(12))
TishaBAv_date = get_holiday_data(index(12))
TishaBAv_str = f'Название: {TishaBAv_name}\n' \
               f'Дата: {TishaBAv_date}'

TuBAv_name = get_holiday_name(index(13))
TuBAv_date = get_holiday_data(index(13))
TuBAv_str = f'Название: {TuBAv_name}\n' \
            f'Дата: {TuBAv_date}'

RoshHaShanah_name = get_holiday_name(index(14))
RoshHaShanah_date = get_holiday_data(index(14))
RoshHaShanah_str = f'Название: {RoshHaShanah_name}\n' \
                   f'Дата: {RoshHaShanah_date}'

TzomGedaliah_name = get_holiday_name(index(15))
TzomGedaliah_date = get_holiday_data(index(15))
TzomGedaliah_str = f'Название: {TzomGedaliah_name}\n' \
                   f'Дата: {TzomGedaliah_date}'

YomKippur_name = get_holiday_name(index(16))
YomKippur_date = get_holiday_data(index(16))
YomKippur_str = f'Название: {YomKippur_name}\n' \
                   f'Дата: {YomKippur_date}'

Succos_name = get_holiday_name(index(17))
Succos_date = get_holiday_data(index(17))
HoshanaRabba_name = get_holiday_name(index(18))
HoshanaRabba_date = get_holiday_data(index(18))
Succos_str = f'Название: {Succos_name}\n' \
             f'Дата: {Succos_date}\n\n' \
             f'Название: {HoshanaRabba_name}\n' \
             f'Дата: {HoshanaRabba_date}'

ShminiAtzeres_name = get_holiday_name(index(19))
ShminiAtzeres_date = get_holiday_data(index(19))
SimhatTorah_name = get_holiday_name(index(20))
SimhatTorah_date = get_holiday_data(index(20))
ShminiAtzeres_Simhat_str = f'Название: {ShminiAtzeres_name}\n' \
                                f'Дата: {ShminiAtzeres_date}\n\n' \
                                f'Название: {SimhatTorah_name}\n' \
                                f'Дата: {SimhatTorah_date}'

SukkotShminiAtzeret_name = get_holiday_name(index(21))
SukkotShminiAtzeret_date = get_holiday_data(index(21))
SukkotShminiAtzeret_str = f'Название: {SukkotShminiAtzeret_name}\n' \
                          f'Дата: {SukkotShminiAtzeret_date}'

Chanukah_name = get_holiday_name(index(22))
Chanukah_date = get_holiday_data(index(22))
Chanukah_str = f'Название: {Chanukah_name}\n' \
               f'Дата: {Chanukah_date}'

AsarahBTevet_name = get_holiday_name(index(23))
AsarahBTevet_date = get_holiday_data(index(23))
AsarahBTevet_str = f'Название: {AsarahBTevet_name}\n' \
                   f'Дата: {AsarahBTevet_date}'








