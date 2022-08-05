import asyncpg
import datetime

from config import settings


class DataBaseClient:
    """Клиент базы данных"""
    async def _connect(self):
        """Коннект к базе"""
        conn: asyncpg.Connection = await asyncpg.connect(
            database=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.HOST_DB,
            port=settings.PORT_DB
        )
        return conn

    async def set_statistics(
            self,
            id_user: int,
            action: str,
            message: str,
            created: datetime.datetime = datetime.datetime.now()
    ):
        """Запись статистики"""
        conn = await self._connect()
        query = """
        INSERT INTO anime_botstatistics(id_user, action, message, created) 
        VALUES($1, $2, $3, $4)
        """
        await conn.execute(query, id_user, action, message, created)
        await conn.close()

    async def set_message(
            self,
            id_user: int,
            message: str,
            created: datetime.datetime = datetime.datetime.now()
    ):
        """Сообщения пользователя"""
        conn = await self._connect()
        query = """
                INSERT INTO anime_botcollbackmessage(id_user, message, created) 
                VALUES($1, $2, $3)
                """
        await conn.execute(query, id_user, message, created)
        await conn.close()
