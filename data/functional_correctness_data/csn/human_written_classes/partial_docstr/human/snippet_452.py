class CallbackEvent:
    """The class that represents callback events for Mobly Snippet Library.

    Attributes:
      callback_id: str, the callback ID associated with the event.
      name: str, the name of the event.
      creation_time: int, the epoch time when the event is created on the
        RPC server side.
      data: dict, the data held by the event. Can be None.
    """

    def __init__(self, callback_id, name, creation_time, data):
        self.callback_id = callback_id
        self.name = name
        self.creation_time = creation_time
        self.data = data

    def __repr__(self):
        return f'CallbackEvent(callback_id: {self.callback_id}, name: {self.name}, creation_time: {self.creation_time}, data: {self.data})'