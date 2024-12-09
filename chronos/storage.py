import logging
import sqlite3
from typing import List, Optional

import aiosqlite
from .task import Task
from .exceptions import StorageError

logger = logging.getLogger(__name__)


class Storage:
    """
    Handles task persistence using SQLite.
    """

    def __init__(self, path: str = "chronos.session"):
        self.path: str = path
        try:
            with sqlite3.connect(self.path) as db:
                db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tasks (
                        id TEXT PRIMARY KEY,
                        data BLOB NOT NULL
                    )
                    """
                )
                db.commit()
            logger.debug("Storage initialized.")
        except sqlite3.Error as e:
            raise StorageError(str(e))

    async def save_task(self, task: Task):
        """Save a task to the database."""
        try:
            async with aiosqlite.connect(self.path) as db:
                await db.execute(
                    "INSERT INTO tasks (id, data) VALUES (?, ?)",
                    (task.id, task.blob),
                )
                await db.commit()
            logger.debug(f"Task {task.id} saved to storage.")
        except aiosqlite.Error as e:
            raise StorageError(str(e))

    async def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID."""
        try:
            async with aiosqlite.connect(self.path) as db:
                async with db.execute(
                    "SELECT data FROM tasks WHERE id = ?", (task_id,)
                ) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        return Task.from_blob(row[0])
            return None
        except aiosqlite.Error as e:
            raise StorageError(str(e))

    async def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from the database."""
        try:
            async with aiosqlite.connect(self.path) as db:
                async with db.execute("SELECT data FROM tasks") as cursor:
                    tasks = [Task.from_blob(row[0]) async for row in cursor]
            return tasks
        except aiosqlite.Error as e:
            raise StorageError(str(e))

    async def update_task(self, task: Task):
        """Update an existing task in the database."""
        try:
            async with aiosqlite.connect(self.path) as db:
                await db.execute(
                    "UPDATE tasks SET data = ? WHERE id = ?",
                    (task.blob, task.id),
                )
                await db.commit()
            logger.debug(f"Task {task.id} updated in storage.")
        except aiosqlite.Error as e:
            raise StorageError(str(e))

    async def remove_task(self, task_id: str):
        """Remove a task from the database."""
        try:
            async with aiosqlite.connect(self.path) as db:
                await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                await db.commit()
            logger.debug(f"Task {task_id} removed from storage.")
        except aiosqlite.Error as e:
            raise StorageError(str(e))
