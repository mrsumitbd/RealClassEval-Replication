class DNAnexus:
    """Files stored in DNAnexus. Partial implementation, integration in bcbio-vm.
    """

    @classmethod
    def check_resource(self, resource):
        return resource.startswith('dx:')

    @classmethod
    def download(self, filename, input_dir, dl_dir=None):
        return None