
class SessionListener:
    """
    A class used to listen to session events.

    Methods
    -------
    callback(root, raw)
        Called when a session event is received.
    errback(ex)
        Called when an error occurs during a session event.
    """

    def callback(self, root, raw):
        """
        Called when a session event is received.

        Parameters
        ----------
        root : object
            The root object of the session event.
        raw : object
            The raw data of the session event.
        """
        pass

    def errback(self, ex):
        """
        Called when an error occurs during a session event.

        Parameters
        ----------
        ex : Exception
            The exception that occurred.
        """
        pass


# Example implementation
class MySessionListener(SessionListener):
    def callback(self, root, raw):
        print(f"Received session event: root={root}, raw={raw}")

    def errback(self, ex):
        print(f"Error occurred during session event: {ex}")


# Example usage
if __name__ == "__main__":
    listener = MySessionListener()
    listener.callback("example_root", "example_raw")
    listener.errback(Exception("example_error"))
