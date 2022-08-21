import httpx
import logging

from config.settings import API_URL, API_KEY

logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self):
        self.api_url = API_URL

    async def _get(self, url: str, params: dict = {}, **kwargs) -> dict | None:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, **kwargs)
            if response.status_code == 200:
                return response.json()
            else:
                 logger.error(f'[{url}] - statuscode[{response.status_code}]')

    async def _post(self, url: str, data: dict, **kwargs) -> dict | None:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, **kwargs)
            if response.status_code == 201:
                return response.json()
            else:
                 logger.error(f'[{url}] - statuscode[{response.status_code}]')

    async def get_anons(self) -> dict | None:
        """Получения анонсов"""
        url = self.api_url + 'anime/'
        params = {'anons': 'True'}
        return await self._get(url, params)

    async def get_anime_day(self, day: str) -> dict | None:
        """Получения аниме по дню недели"""
        url = self.api_url + 'anime/'
        params = {'day_week': day}
        return await self._get(url, params)

    async def get_genre(self) -> list | None:
        """Жанры"""
        url = self.api_url + 'anime/genre/'
        return await self._get(url)

    async def get_filter_genre(self, title: str, page: int = 1) -> dict | None:
        """Фильтр по жанрам"""
        url = self.api_url + 'anime/'
        params = {'genre': title, 'page': page}
        return await self._get(url, params)

    async def get_count_anime(self) -> int | None:
        """Количество аниме"""
        url = self.api_url + 'anime/'
        result = await self._get(url)
        return result.get('count')

    async def search(self, q: str, page: int = 1) -> dict | None:
        """Поиск по названию"""
        url = self.api_url + 'anime/'
        params = {'search': q, 'page': page}
        return await self._get(url, params)

    async def get_indefinite_exit(self) -> dict | None:
        """Аниме с неопределенным сроком выхода"""
        url = self.api_url + 'anime/'
        params = {'indefinite_exit': True, 'ordering': '-updated'}
        return await self._get(url, params)

    async def sent_statistic(
            self,
            id_user: int,
            action: str,
            message: str
    ) -> dict | None:
        """Запись статистики"""
        url = self.api_url + 'bot/statistic/'
        headers = {'Authorization': f'Token {API_KEY}'}
        data = {
            'id_user': id_user,
            'action': action,
            'message': message
        }
        return await self._post(url, data, headers=headers)

    async def sent_message(
            self,
            id_user: int,
            message: str
    ) -> dict | None:
        """Отправка сообщения пользователя"""
        url = self.api_url + 'bot/massage/'
        headers = {'Authorization': f'Token {API_KEY}'}
        data = {
            'id_user': id_user,
            'message': message
        }
        return await self._post(url, data, headers=headers)
