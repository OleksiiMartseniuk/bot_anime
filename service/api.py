import httpx
import logging


logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self):
        self.api_url = 'http://localhost/v1/anime/'

    async def _get(self, url: str, params: dict = {}) -> dict | None:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
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

    async def get_genre(self):
        """Жанры"""
        url = self.api_url + 'genre/'
        return await self._get(url)

    async def get_filter_genre(self, title: str):
        params = {'genre': title}
        return await self._get(self.api_url, params)
