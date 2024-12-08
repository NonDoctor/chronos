import pytest
import time

from chronos.task import Task


@pytest.mark.asyncio
async def test_storage_save_and_retrieve_task(sample_function, storage):

    task = Task(sample_function, params=[1, 2, 3], next_run=time.time())
    await storage.save_task(task)

    retrieved_task = await storage.get_task(task.id)
    assert retrieved_task is not None
    assert retrieved_task.id == task.id


@pytest.mark.asyncio
async def test_storage_update_task(sample_function, storage):

    task = Task(function=sample_function, params=[1, 2, 3], next_run=time.time())
    await storage.save_task(task)

    task.next_run += 10
    await storage.update_task(task)

    updated_task = await storage.get_task(task.id)
    assert updated_task.next_run == task.next_run


@pytest.mark.asyncio
async def test_storage_remove_task(sample_function, storage):

    task = Task(function=sample_function, params=[1, 2, 3], next_run=time.time())
    await storage.save_task(task)

    await storage.remove_task(task.id)
    retrieved_task = await storage.get_task(task.id)
    assert retrieved_task is None
