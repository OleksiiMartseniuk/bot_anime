import httpx
import logging


logger = logging.getLogger(__name__)


class ClientBase:
    """Основной клиент"""

    async def get(self, url: str, params: dict = {}, **kwargs) -> dict | None:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, **kwargs)
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f'[{url}] - status_code'
                                 f'[{response.status_code}]')
        except httpx.RequestError as exc:
            logger.error(f'Исключения {exc.__class__} [{str(exc)}] url[{url}]')

    async def post(self, url: str, data: dict, **kwargs) -> dict | None:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data, **kwargs)
                if response.status_code == 201:
                    return response.json()
                else:
                    logger.error(f'[{url}] - status_code'
                                 f'[{response.status_code}]')
        except httpx.RequestError as exc:
            logger.error(f'Исключения {exc.__class__} [{str(exc)}] url[{url}]')
