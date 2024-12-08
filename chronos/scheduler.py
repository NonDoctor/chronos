import asyncio
import logging
from time import time
from typing import Optional

from chronos.storage import Storage
from chronos.task import Task
from chronos.executor import TaskExecutor

logger = logging.getLogger(__name__)


class Scheduler:
    """
    A Scheduler to manage and execute tasks.
    It orchestrates task scheduling, execution, and storage persistence.
    """

    def __init__(self, storage_path: Optional[str] = None):
        self.executor = TaskExecutor()  # Handles task execution
        self.storage = Storage(storage_path) if storage_path else Storage()
        self.tasks = []  # Tracks all running asyncio tasks
        self.running = False  # Indicates if the scheduler is running

    async def __run_task(self, task: Task, save: bool = False):
        """
        Executes a single task and reschedules it if necessary.

        Args:
            task (Task): The task to execute.
            save (bool): Whether to save the task to storage before execution.
        """
        try:
            # Save the task to storage if specified
            if save:
                await self.storage.save_task(task)

            # Calculate the time to wait before executing the task
            pause = task.next_run - time()
            if pause > 0:
                await asyncio.sleep(pause)  # Wait until the scheduled time
            else:
                if not task.run_missed:
                    logger.warning(
                        f"Task {task.id} missed its run and will not execute."
                    )
                    return  # Skip execution if missed runs are not allowed

            # Execute the task
            await self.executor.execute(task)
            logger.debug(f"Task {task.id} executed successfully.")

            # Reschedule the task if it's recurring
            if task.schedule_next_run():
                await self.storage.update_task(
                    task
                )  # Update the new run time in storage
                logger.debug(f"Task {task.id} rescheduled for next run.")
                task_runner = asyncio.create_task(self.__run_task(task))
                self.tasks.append(task_runner)
            else:
                # Remove the task from storage if it's completed
                await self.storage.remove_task(task.id)
                logger.debug(f"Task {task.id} completed and removed from storage.")
        except Exception as e:
            # Log any exceptions during task execution
            logger.error(f"Task {task.id} failed: {e}")

    async def add_task(self, task: Task):
        """
        Adds a task to the scheduler and starts its execution.

        Args:
            task (Task): The task to add.
        """
        # Schedule the task for execution
        task_runner = asyncio.create_task(self.__run_task(task, save=True))
        self.tasks.append(task_runner)

    async def __start(self):
        """
        Starts the scheduler and initializes tasks from storage.
        """
        try:
            self.running = True
            # Retrieve all tasks from storage
            tasks = await self.storage.get_all_tasks()
            logger.info(f"Scheduler started with {len(tasks)} tasks.")
            # Start all retrieved tasks
            for task in tasks:
                task_runner = asyncio.create_task(self.__run_task(task))
                self.tasks.append(task_runner)
        except Exception as e:
            # Log and re-raise exceptions during the start process
            logger.error(f"Failed to start scheduler: {e}")
            raise

    def start(self):
        """
        Starts the scheduler in the current event loop.
        If no event loop is running, it creates and runs one.
        """
        try:
            ioloop = asyncio.get_event_loop()
            if not ioloop.is_running():
                # Start the scheduler in a new event loop
                ioloop.run_until_complete(self.__start())
            else:
                # Schedule the start coroutine in the existing loop
                asyncio.create_task(self.__start())
        except RuntimeError as e:
            # Handle runtime errors related to the event loop
            logger.error(f"Runtime error during scheduler start: {e}")
            raise

    async def stop(self):
        """
        Stops the scheduler and cancels all running tasks.
        """
        self.running = False
        logger.info("Scheduler stopping...")
        # Cancel all running tasks
        for task in self.tasks:
            if not task.done():
                task.cancel()
        # Wait for all tasks to finish or handle cancellations
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()
