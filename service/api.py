from base.api_client import ClientBase
from config.settings import API_URL, API_KEY


class ApiClient(ClientBase):
    """Api"""

    def __init__(self):
        self.api_url = API_URL

    async def get_anons(self) -> dict | None:
        """Получения анонсов"""
        url = self.api_url + 'anime/'
        params = {'anons': 'True'}
        return await self.get(url, params)

    async def get_anime_day(self, day: str) -> dict | None:
        """Получения аниме по дню недели"""
        url = self.api_url + 'anime/'
        params = {'day_week': day}
        return await self.get(url, params)

    async def get_genre(self) -> list | None:
        """Жанры"""
        url = self.api_url + 'anime/genre/'
        return await self.get(url)

    async def get_filter_genre(self, title: str, page: int = 1) -> dict | None:
        """Фильтр по жанрам"""
        url = self.api_url + 'anime/'
        params = {'genre': title, 'page': page}
        return await self.get(url, params)

    async def get_count_anime(self) -> int | None:
        """Количество аниме"""
        url = self.api_url + 'anime/'
        result = await self.get(url)
        return result.get('count')

    async def search(self, q: str, page: int = 1) -> dict | None:
        """Поиск по названию"""
        url = self.api_url + 'anime/'
        params = {'search': q, 'page': page}
        return await self.get(url, params)

    async def get_indefinite_exit(self) -> dict | None:
        """Аниме с неопределенным сроком выхода"""
        url = self.api_url + 'anime/'
        params = {'indefinite_exit': True, 'ordering': '-updated'}
        return await self.get(url, params)

    async def sent_statistic(
            self, id_user: int, action: str, message: str
    ) -> dict | None:
        """Запись статистики"""
        url = self.api_url + 'bot/statistic/'
        headers = {'Authorization': f'Token {API_KEY}'}
        data = {
            'id_user': id_user,
            'action': action,
            'message': message
        }
        return await self.post(url, data, headers=headers)

    async def sent_message(
            self, id_user: int, message: str
    ) -> dict | None:
        """Отправка сообщения пользователя"""
        url = self.api_url + 'bot/message/'
        headers = {'Authorization': f'Token {API_KEY}'}
        data = {
            'id_user': id_user,
            'message': message
        }
        return await self.post(url, data, headers=headers)

    async def create_user(
        self, username: str, user_id: int, chat_id: int
    ) -> dict | None:
        """Создания пользователя"""
        url = self.api_url + 'bot/create-user/'
        headers = {'Authorization': f'Token {API_KEY}'}
        data = {
            'username': username,
            'user_id': user_id,
            'chat_id': chat_id
        }
        return await self.post(url, data, headers=headers)

    async def get_anime_track(
        self, user_id: int, subscriber: bool
    ) -> list | None:
        """Вывод аниме с отслеживание пользователя
        Parameters:
            subscriber (bool) - True: Получения список подписок
            subscriber (bool) - False: Получения список возможных подписок
        """
        url = self.api_url + 'bot/get-anime/'
        headers = {'Authorization': f'Token {API_KEY}'}
        params = {
            'user_id': user_id,
            'subscriber': subscriber
        }
        return await self.get(url, params, headers=headers)

    async def add_anime_track(
        self, anime_ids: list[int], user_id: int
    ) -> dict | None:
        """Добавить аниме в отслеживаемые пользователем"""
        url = self.api_url + 'bot/add-anime/'
        headers = {'Authorization': f'Token {API_KEY}'}
        data = {
            'anime_ids': anime_ids,
            'user_id': user_id
        }
        return await self.post(url, data, headers=headers)

    async def remove_anime_track(
        self, anime_ids: list[int], user_id: int
    ) -> dict | None:
        """Удаления аниме с отслеживаемые пользователем"""
        url = self.api_url + 'bot/remove-anime/'
        headers = {'Authorization': f'Token {API_KEY}'}
        data = {
            'anime_ids': anime_ids,
            'user_id': user_id
        }
        return await self.post(url, data, headers=headers)
