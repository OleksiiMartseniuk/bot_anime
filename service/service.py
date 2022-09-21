import math
import re
import logging

from pydantic import ValidationError
from enum import Enum
from datetime import datetime

from . import schemas


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
    time = f'<b>Время выхода</b> 🕜️ ({date_time}) \n' if schedules else ''
    date = re.findall(r'\s\d+\s\w+', data['title'])
    date_string = 'Не определена'
    if date:
        date_string = f'<b>Дата выхода</b> 📅 {date[0].strip()}'
    anons = f'<b>Анонс</b> ✅ \n{date_string} \n' if data['anons'] else ''
    return f"<b>{data['title'].split('/')[0]}</b> \n\n" \
           f"{anons}" \
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


def get_anime_anilibria(item: dict) -> schemas.AnimeAniLibria | None:
    """Получения схемы AnimeAniLibria"""
    try:
        names = schemas.Names(
            ru=item.get('names').get('ru'),
            en=item.get('names').get('en')
        )
        posters = schemas.Posters(
            small=item.get('posters').get('small').get('url'),
            medium=item.get('posters').get('medium').get('url'),
            original=item.get('posters').get('original').get('url')
        )
        type = schemas.PType(
            full_string=item.get('type').get('full_string'),
            string=item.get('type').get('string'),
            series=item.get('type').get('series'),
            length=item.get('type').get('length')
        )
        anime = schemas.AnimeAniLibria(
            id=item.get('id'),
            code=item.get('code'),
            names=names,
            posters=posters,
            updated=item.get('updated'),
            last_change=item.get('last_change'),
            type=type,
            genres=item.get('genres'),
            description=item.get('description'),
        )
    except ValidationError as e:
        logger.error(e)
        return

    return anime


def cart_anilibria(anime: schemas.AnimeAniLibria) -> str:
    """Вывод аниме anilibria"""
    time = datetime.utcfromtimestamp(anime.updated)
    time = time.strftime('%m/%d/%Y %H:%M')
    return f"<b>{anime.names.ru}</b> \n\n" \
           f"<b>Жанр</b>: {' '.join(anime.genres)}\n" \
           f"<b>Обновлен</b> 🕜️ {time} \n" \
           f"<b>Описания</b> 📔: {anime.description}"
