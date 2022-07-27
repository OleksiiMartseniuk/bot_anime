from enum import Enum
from datetime import datetime


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
    return f"<b>{data['title'].split('/')[0]}</b> \n\n" \
           f"<b>Время выхода</b> 🕜️ ({date_time}) \n" \
           f"<b>Рейтинг</b> 📊 {data['rating']}\n" \
           f"<b>Голоса</b> 🗳️ {data['votes']}\n" \
           f"<a href='{data['link']}'>Смотреть на animevost.org</a>"
