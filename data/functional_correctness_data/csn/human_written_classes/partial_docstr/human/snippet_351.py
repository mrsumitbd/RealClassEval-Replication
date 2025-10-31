class SevenBridges:
    """Files stored in SevenBridges. Partial implementation, integration in bcbio-vm.
    """

    @classmethod
    def check_resource(self, resource):
        return resource.startswith('sbg:')

    @classmethod
    def download(self, filename, input_dir, dl_dir=None):
        return None