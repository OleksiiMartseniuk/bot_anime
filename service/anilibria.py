from base.api_client import ClientBase


class AniLibriaClient(ClientBase):
    """AniLibria"""

    def __init__(self) -> None:
        # https://github.com/anilibria/docs/blob/master/api_v2.md
        self.url_base = 'https://api.anilibria.tv/'
        self.url_api = self.url_base + 'v2/'

    async def get_anime_gay(self, day: int) -> list[dict] | None:
        """Получить список аниме по дню"""
        url = self.url_api + 'getSchedule'
        params = {'days': day}
        return await self.get(url=url, params=params)
