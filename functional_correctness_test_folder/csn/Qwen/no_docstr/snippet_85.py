
class SessionListener:

    def callback(self, root, raw):
        # Process the successful session data
        print(f"Session data received: {root}, Raw data: {raw}")

    def errback(self, ex):
        # Handle exceptions that occur during the session
        print(f"An error occurred: {ex}")
