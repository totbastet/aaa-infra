from dataclasses import dataclass

import asyncpg


@dataclass
class ItemEntry:
    item_id: int
    user_id: int
    title: str
    description: str


class ItemStorage:
    def __init__(self):
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        self._pool = await asyncpg.create_pool()

    async def disconnect(self) -> None:
        await self._pool.close()

    async def create_tables_structure(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS items (
            item_id INT PRIMARY KEY,
            user_id INT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL);
        """

        async with self._pool.acquire() as connection:
            await connection.execute(query)

    async def save_items(self, items: list[ItemEntry]) -> None:
        data = [(item.item_id, item.user_id, item.title, item.description) for item in items]
        query = """
        INSERT INTO items (item_id, user_id, title, description)
        VALUES ($1, $2, $3, $4)
        """

        async with self._pool.acquire() as connection:
            await connection.executemany(query, data)

    async def find_similar_items(
        self, user_id: int, title: str, description: str
    ) -> list[ItemEntry]:
        """
        Напишите код для поиска записей, имеющих указанные user_id, title и description.
        """
        query = """
        SELECT item_id, user_id, title, description
        FROM items
        WHERE user_id = $1 AND title = $2 AND description = $3;
        """

        async with self._pool.acquire() as connection:
            rows = await connection.fetch(query, user_id, title, description)
        
        return [
            ItemEntry(
                item_id=row['item_id'],
                user_id=row['user_id'],
                title=row['title'],
                description=row['description'])
                for row in rows
            ]
