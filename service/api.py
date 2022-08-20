import httpx
import logging

from config.settings import API_URL

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
        params = {'anons': 'True'}
        return await self._get(self.api_url, params)

    async def get_anime_day(self, day: str) -> dict | None:
        """Получения аниме по дню недели"""
        params = {'day_week': day}
        return await self._get(self.api_url, params)

    async def get_genre(self) -> list | None:
        """Жанры"""
        url = self.api_url + 'genre/'
        return await self._get(url)

    async def get_filter_genre(self, title: str, page: int = 1) -> dict | None:
        """Фильтр по жанрам"""
        params = {'genre': title, 'page': page}
        return await self._get(self.api_url, params)

    async def get_count_anime(self) -> int | None:
        """Количество аниме"""
        result = await self._get(self.api_url)
        return result.get('count')

    async def search(self, q: str, page: int = 1) -> dict | None:
        """Поиск по названию"""
        params = {'search': q, 'page': page}
        return await self._get(self.api_url, params)

    async def get_indefinite_exit(self) -> dict | None:
        """Аниме с неопределенным сроком выхода"""
        params = {'indefinite_exit': True, 'ordering': '-updated'}
        return await self._get(self.api_url, params)
