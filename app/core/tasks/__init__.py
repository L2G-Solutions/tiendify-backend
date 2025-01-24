from typing import Any

from celery.app.task import Task
from celery.result import AsyncResult


def run_in_background(task_func: Task, *args: Any, **kwargs: Any) -> AsyncResult:
    """Schedule a task to be executed in the background.

    Args:
        task_func (Task): The task function to be executed
        *args (Any): The task function arguments
        **kwargs (Any): The task function keyword arguments

    Returns:
        AsyncResult: The task result
    """

    res = task_func.apply_async(
        args=args,
        kwargs=kwargs,
    )

    return res
