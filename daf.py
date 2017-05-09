import requests
import pytz
import data
import functions as f
from datetime import datetime


URL = 'http://db.ou.org/zmanim'


def get_daf(loc, lang):
    tz = f.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    daf = requests.get('{}/getCalendarData.php?mode=day&timezone='
                       '{}&dateBegin={}/{}/{}'
                       '&lat={}&lng={}'.format(URL, tz, now.month,
                                               now.day,
                                               now.year,
                                               loc[0],
                                               loc[1]))
    daf_dict = daf.json()
    if lang == 'Русский':
        daf_str = f'Трактат: {data.talmud[daf_dict["dafYomi"]["masechta"]]}' \
                  f'\nЛист: {daf_dict["dafYomi"]["daf"]}'
    elif lang == 'English':
        daf_str = f'Masechta: {daf_dict["dafYomi"]["masechta"]}\n' \
                  f'Daf: {daf_dict["dafYomi"]["daf"]}'
    return daf_str
