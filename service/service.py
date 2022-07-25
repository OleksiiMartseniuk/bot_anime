from datetime import datetime

import aiogram.utils.markdown as fmt


def card(data: dict, schedules: bool = False) -> str:
    """Вывод аниме"""
    if data['timer']:
        date_time = datetime.fromtimestamp(data['timer'])
        date_time = date_time.strftime('%H:%M')
    else:
        date_time = 'В течении дня'
    time = f'Time: {date_time}' if schedules else ''
    return f"{fmt.hide_link(data['url_image_preview'])} " \
           f"{data['title'].split('/')[0]} \n\n" \
           f"{time} \n\n" \
           f"<a href='{data['link']}'>animevost</a>"