
class SessionListener:

    def callback(self, root, raw):
        self.root = root
        self.raw = raw
        # You can add more logic here if needed

    def errback(self, ex):
        self.error = ex
        # You can add more logic here if needed
