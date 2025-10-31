class GoogleCloud:
    """Files stored in Google Cloud Storage. Partial implementation, integration in bcbio-vm.
    """

    @classmethod
    def check_resource(self, resource):
        return resource.startswith('gs:')

    @classmethod
    def download(self, filename, input_dir, dl_dir=None):
        return None