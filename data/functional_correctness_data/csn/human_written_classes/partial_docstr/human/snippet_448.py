class SnippetEvent:
    """The class that represents callback events for mobly snippet library.

    DEPRECATED: Use mobly.snippet.callback_event.CallbackEvent instead.

    Attributes:
      callback_id: string, the callback ID associated with the event.
      name: string, the name of the event.
      creation_time: int, the epoch time when the event is created on the
        Rpc server side.
      data: dictionary, the data held by the event. Can be None.
    """

    def __init__(self, callback_id, name, creation_time, data):
        self.callback_id = callback_id
        self.name = name
        self.creation_time = creation_time
        self.data = data

    def __repr__(self):
        return 'SnippetEvent(callback_id: %s, name: %s, creation_time: %s, data: %s)' % (self.callback_id, self.name, self.creation_time, self.data)