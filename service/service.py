from datetime import datetime

import aiogram.utils.markdown as fmt


def card(data: dict, schedules: bool = False) -> str:
    """Вывод аниме"""
    if data['timer']:
        date_time = datetime.fromtimestamp(data['timer'])
        date_time = date_time.strftime('%H:%M')
    else:
        date_time = 'В течении дня'
    time = f'Time: {date_time} \n\n' if schedules else ''
    return f"{fmt.hide_link(data['url_image_preview'])} " \
           f"<b>{data['title'].split('/')[0]}</b> \n\n" \
           f"{time} " \
           f"<a href='{data['link']}'>animevost</a>"
