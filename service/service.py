import math
import re
import logging

from enum import Enum
from datetime import datetime

from .api import ApiClient


logger = logging.getLogger(__name__)


class Week(Enum):
    monday = 'понедельник'
    tuesday = 'вторник'
    wednesday = 'среда'
    thursday = 'четверг'
    friday = 'пятница'
    saturday = 'суббота'
    sunday = 'воскресенье'


def card(data: dict, schedules: bool = False) -> str:
    """Вывод аниме"""
    if data['timer']:
        date_time = datetime.fromtimestamp(data['timer'])
        date_time = date_time.strftime('%H:%M')
    else:
        date_time = 'В течении дня'
    day_name = data.get('day_week')
    if day_name:
        week_day_name = f'<b>День недели</b> 📅 {Week[day_name].value} \n'
    day = week_day_name if day_name else ''
    time = f'<b>Время выхода</b> 🕜️ ({date_time}) \n' if schedules else ''
    date = re.findall(r'\s\d+\s\w+', data['title'])
    date_string = 'Не определена'
    if date:
        date_string = f'<b>Дата выхода</b> 📅 {date[0].strip()}'
    anons = f'<b>Анонс</b> ✅ \n{date_string} \n' if data['anons'] else ''
    return f"<b>{data['title'].split('/')[0]}</b> \n\n" \
           f"{anons}" \
           f"{day}" \
           f"{time}" \
           f"<b>Рейтинг</b> 📊 {data['rating']}\n" \
           f"<b>Голоса</b> 🗳️ {data['votes']}\n\n" \
           f"<a href='{data['link']}'>Смотреть на animevost.org</a>\n" \
           f"<a href='{get_link_mirror(data['link'])}'>Зеркало v2.vost.pw</a>"


def get_page_list(page_count: int) -> list[int]:
    """Получения списка страниц"""
    count = page_count / 20
    return [x for x in reversed(range(1, math.ceil(count) + 1))]


def get_link_mirror(link: str) -> str | None:
    """Генерация ссылки зеркала"""
    if not link:
        # Ссылки нет
        return link
    result = re.sub(r'/animevost.org/', '/v2.vost.pw/', link)
    return result


def get_image(url_image_preview: str, telegram_id_file: str | None) -> str:
    """Получения доступной картинки"""
    return telegram_id_file if telegram_id_file else url_image_preview


async def user_registration(username: str, user_id: int, chat_id: int) -> None:
    """Регистрация пользователя"""
    # Проверка на существующего пользователя
    user = await ApiClient().get_user(user_id)
    if not user:
        # Регистрация пользователя
        await ApiClient().create_user(username, user_id, chat_id)
