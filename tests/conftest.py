import pytest
import os

from chronos import Storage
from chronos.scheduler import Scheduler


@pytest.fixture
def sample_function():
    pass


@pytest.fixture
async def async_function():
    result = None

    async def fn(param):
        nonlocal result
        result = param

    return fn, lambda: result


@pytest.fixture
def sync_function():
    result = None

    def fn(param):
        nonlocal result
        result = param

    return fn, lambda: result


@pytest.fixture
def storage():
    db_path = "chronos.test"
    storage = Storage(path=db_path)

    yield storage

    if db_path != ":memory:":
        if os.path.exists(db_path):
            os.remove(db_path)


@pytest.fixture
def scheduler():
    db_path = "chronos.test"
    scheduler = Scheduler(db_path)

    yield scheduler

    if db_path != ":memory:":
        if os.path.exists(db_path):
            os.remove(db_path)
