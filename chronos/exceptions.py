class SchedulerError(Exception):
    """Base class for scheduler-related errors."""

    pass


class TaskExecutionError(SchedulerError):
    """Raised when a task execution fails."""

    def __init__(self, task_id: str, message: str):
        super().__init__(f"Task {task_id} failed: {message}")
        self.task_id = task_id


class StorageError(SchedulerError):
    """Raised for storage-related errors."""

    def __init__(self, message: str):
        super().__init__(f"Storage error: {message}")
