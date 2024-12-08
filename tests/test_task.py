import time

from chronos.task import Task


def test_task_initialization(sample_function):
    """Test task initialization."""
    task = Task(function=sample_function, params=[1, 2, 3], next_run=time.time())
    assert task.function == sample_function
    assert task.params == [1, 2, 3]


def test_task_serialization(sample_function):
    """Test task serialization and deserialization."""
    task = Task(function=sample_function, params=[1, 2, 3], next_run=time.time())
    blob = task.blob
    deserialized_task = Task.from_blob(blob)  # Deserialize the task

    assert deserialized_task.function == task.function
    assert deserialized_task.params == task.params
    assert deserialized_task.next_run == task.next_run


def test_task_rescheduling(sample_function):
    """Test task rescheduling."""
    task = Task(
        function=sample_function, params=[], next_run=time.time(), interval_seconds=10
    )
    assert task.schedule_next_run()
    assert task.next_run > time.time()
