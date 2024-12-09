
chronos: Task Scheduler for AsyncIO
==============

Task Scheduler is a simple asynchronous task scheduler written in Python using `asyncio`. It allows you to schedule tasks to run at specific times or at regular intervals. Tasks are executed in the background and can be persisted to storage, so they can be reloaded and rescheduled after restarting the application.

Features
--------
- **Asynchronous Execution**: Tasks are executed asynchronously using `asyncio`.
- **Task Persistence**: Tasks can be saved to storage and rescheduled automatically after the application restarts.
- **Recurring Tasks**: Tasks can be scheduled to run periodically.
- **Missed Task Handling**: If a task is missed (due to application shutdown or other issues), it can be configured to either skip or run once the system is ready again.

Installation
------------
poetry:
```bash
poetry add git+https://github.com/NonDoctor/chronos.git
```
or pip:
```bash
pip install git+https://github.com/NonDoctor/chronos.git
```

### Requirements
- Python 3.8 or higher (ensure you're using the correct Python version by checking your environment)

To install the project dependencies:
- aiosqlite=^20.0

Usage
-----

### Example

Here is a simple example of how to use the task scheduler:

```python
import asyncio
import time

# Dummy task function
def sample_task(param1, param2):
    print(f"Executing task with parameters: {param1}, {param2}")
    time.sleep(1)  # Simulate a task that takes some time to process

async def main():
    # Create a Scheduler instance
    scheduler = Scheduler()

    # Define a task that runs every 2 seconds
    task1 = Task(
        function=sample_task,
        params=[1, 2],
        next_run=time.time() + 1,  # Start the task to run after 1 second
        interval_seconds=2,  # Run every 2 seconds
        run_missed=True,
    )

    # Add the task to the scheduler
    scheduler.add_task(task1)

    # Start the scheduler
    scheduler.start()

    # Let it run for a few seconds
    await asyncio.sleep(10)

    # Stop the scheduler after running for a while
    await scheduler.stop()

# Ensure proper handling of the event loop
if __name__ == "__main__":
    asyncio.run(main())
```
