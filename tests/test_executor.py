import pytest
from chronos.executor import TaskExecutor
from chronos.task import Task


@pytest.mark.asyncio
async def test_executor_runs_sync_function(sync_function):
    sync_fn, get_result = sync_function

    executor = TaskExecutor()
    task = Task(function=sync_fn, params=["test_param"], next_run=0)

    await executor.execute(task)
    assert get_result() == "test_param"


@pytest.mark.asyncio
async def test_executor_runs_async_function(async_function):
    async_fn, get_result = await async_function

    executor = TaskExecutor()

    task = Task(function=async_fn, params=["test_param"], next_run=0)

    await executor.execute(task)

    assert get_result() == "test_param"
