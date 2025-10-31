class MockImageDataset:

    def __init__(self, huggingface_dataset_path: str, huggingface_datset_split: str='train', huggingface_datset_name: str=None, create_splits: bool=False, download_mode: str=None):
        self.huggingface_dataset_path = huggingface_dataset_path
        self.huggingface_dataset_name = huggingface_datset_name
        self.dataset = ''
        self.sampled_images_idx = []

    def __getitem__(self, index: int) -> dict:
        return {'image': create_random_image(), 'id': index, 'source': self.huggingface_dataset_path}

    def __len__(self):
        return 100

    def sample(self, k=1):
        return ([self.__getitem__(i) for i in range(k)], [i for i in range(k)])