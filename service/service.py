from enum import Enum
from datetime import datetime

import aiogram.utils.markdown as fmt


class Week(Enum):
    monday = 'понедельник'
    tuesday = 'вторник'
    wednesday = 'среда'
    thursday = 'четверг'
    friday = 'пятница'
    saturday = 'суббота'
    sunday = 'воскресенье'


def card(data: dict) -> str:
    """Вывод аниме"""
    if data['timer']:
        date_time = datetime.fromtimestamp(data['timer'])
        date_time = date_time.strftime('%H:%M')
    else:
        date_time = 'В течении дня'
    return f"{fmt.hide_link(data['url_image_preview'])} " \
           f"<b>{data['title'].split('/')[0]}</b> \n\n" \
           f"Время выхода ~({date_time}) \n" \
           f"Рейтинг {data['rating']}\n" \
           f"Голоса {data['votes']}\n" \
           f"<a href='{data['link']}'>Смотреть на animevost.org</a>"
