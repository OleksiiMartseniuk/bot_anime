from base.api_client import ClientBase


class AniLibriaClient(ClientBase):
    """AniLibria"""

    def __init__(self) -> None:
        # https://github.com/anilibria/docs/blob/master/api_v2.md
        self.url_base = 'https://api.anilibria.tv/'
        self.url_api = self.url_base + 'v2/'

    async def get_title(self, id: int = None, code: str = None) -> dict | None:
        """Получить информацию о тайтле по id или коду"""
        url = self.url_api + 'getTitle'
        if id:
            params = {'id': id}
        elif code:
            params = {'code': code}
        else:
            return None
        return await self.get(url=url, params=params)

    async def get_anime_gay(self, day: int) -> list[dict] | None:
        """Получить список аниме по дню"""
        url = self.url_api + 'getSchedule'
        params = {'days': day}
        return await self.get(url=url, params=params)
