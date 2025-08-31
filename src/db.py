import asyncio
import logging

import aiosqlite


class DbManger:
    logger = logging.getLogger(__name__)
    connection_path = ":memory:"

    def __init__(self):
        self.connection = None

    async def connect(self):
        try:
            self.connection = await aiosqlite.connect(self.connection_path)
            return True
        except Exception as e:
            self.logger.error(f"Database connection error: {e}")
            return False

    async def is_connected(self):
        if self.connection is None:
            return False
        try:
            await self.connection.execute("SELECT 1")
            return True
        except Exception as e:
            self.logger.error(f"Database connection error: {e}")
            return False

    async def get_selected_device(self):
        async with self.connection.cursor() as cursor:
            query = "SELECT serial_number FROM current_device LIMIT 1"
            result = await cursor.execute(query)
            result = await cursor.fetchone()
        return result[0] if result else None

    async def set_selected_device(self, serial_number):
        await self.connection.execute("DELETE FROM current_device")
        await self.connection.execute(
            """
            INSERT INTO current_device (serial_number) VALUES (?)
            """,
            (serial_number,),
        )
        await self.connection.commit()

    async def create_tables(self):
        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS current_device (serial_number TEXT)
            """
        )
        await self.connection.execute(
            """
            DELETE FROM current_device
            """
        )
        await self.connection.commit()

    async def close(self):
        await self.connection.close()
        self.connection = None


db_manager = DbManger()
