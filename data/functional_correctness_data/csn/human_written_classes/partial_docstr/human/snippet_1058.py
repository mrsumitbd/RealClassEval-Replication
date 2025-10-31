class RemoteSetupHandler:
    """ Default behavior. Fetch setup information from remote Pulsar server.
    """

    def __init__(self, client):
        self.client = client

    def setup(self, **setup_args):
        setup_args['use_metadata'] = 'true'
        return self.client.remote_setup(**setup_args)

    @property
    def local(self):
        """
        """
        return False