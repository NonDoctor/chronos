import logging
import asyncio

from chronos.task import Task
from chronos.exceptions import TaskExecutionError


logger = logging.getLogger(__name__)


class TaskExecutor:
    """
    Executes tasks, supporting both synchronous and asynchronous functions.
    """

    def _find_function(self, func):
        """Determine if the function is asynchronous."""
        if asyncio.iscoroutinefunction(func):
            return True
        elif callable(func):
            return False
        else:
            raise TypeError(f"{func.__name__} is not a valid function.")

    async def execute(self, task: Task):
        """Execute a given task."""
        try:
            is_async = self._find_function(task.function)
            if is_async:
                await task.function(*task.params)
            else:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, task.function, *task.params)  # type: ignore
        except Exception as e:
            raise TaskExecutionError(task.id, str(e))
