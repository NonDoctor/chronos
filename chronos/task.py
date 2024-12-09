import pickle
import uuid
from typing import Any, Callable, List, Optional


class Task:
    """
    Represents a scheduled task with its metadata and execution logic.
    """

    def __init__(
        self,
        function: Callable,
        params: List[Any],
        next_run: float,
        _id: Optional[str] = None,
        interval_seconds: Optional[int] = None,
        run_missed: bool = True,
    ):
        self.id = _id or str(uuid.uuid4())  # Unique ID for the task
        self.function = function  # Function to be executed
        self.params = params  # Parameters to be passed to the function
        self.next_run = next_run  # Timestamp for the next execution
        self.interval_seconds = interval_seconds  # Interval for periodic execution
        self.run_missed = run_missed  # Whether to run missed executions

    @classmethod
    def from_blob(cls, blob: bytes):
        """Deserialize a task from a binary blob."""
        return pickle.loads(blob)

    @property
    def blob(self) -> bytes:
        """Serialize the task to a binary blob."""
        return pickle.dumps(self)

    def schedule_next_run(self) -> bool:
        """
        Updates the task's next_run to the next interval if periodic.
        Returns True if the task is rescheduled, False otherwise.
        """
        if self.interval_seconds:
            self.next_run += self.interval_seconds
            return True
        return False

    def __repr__(self):
        """Return a string representation of the Task object."""
        return f"Task(id={self.id}, function={self.function.__name__}, params={self.params}, next_run={self.next_run}, interval_seconds={self.interval_seconds}, run_missed={self.run_missed})"
