import asyncio

class TaskLocalStorage:
    """
    Simple task local storage
    """

    def __init__(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop

    def __setattr__(self, name, value):
        if name in ('_loop',):
            object.__setattr__(self, name, value)
        else:
            task = asyncio.current_task(loop=self._loop)
            if task is None:
                return None
            if not hasattr(task, 'context'):
                task.context = {}
            task.context[name] = value

    def __getattribute__(self, item):
        if item in ('_loop', 'clear'):
            return object.__getattribute__(self, item)
        task = asyncio.current_task(loop=self._loop)
        if task is None:
            return None
        if hasattr(task, 'context') and item in task.context:
            return task.context[item]
        raise AttributeError('Task context does not have attribute {0}'.format(item))

    def clear(self):
        task = asyncio.current_task(loop=self._loop)
        if task is not None and hasattr(task, 'context'):
            task.context.clear()