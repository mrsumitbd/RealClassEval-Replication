from natix.validator.miner_performance_tracker import MinerPerformanceTracker
import bittensor as bt
import numpy as np

class MockValidator:

    def __init__(self, config):
        self.config = config
        subtensor = MockSubtensor(config.netuid, wallet=bt.MockWallet())
        self.performance_tracker = MinerPerformanceTracker()
        self.metagraph = MockMetagraph(netuid=config.netuid, subtensor=subtensor)
        self.dendrite = MockDendrite(bt.MockWallet())
        self.real_image_datasets = [MockImageDataset(f'fake-path/dataset-{i}', 'train', None, False) for i in range(3)]
        self.synthetic_data_generator = MockSyntheticDataGenerator(prompt_type='annotation', use_random_diffuser=True, diffuser_name=None)
        self.total_real_images = sum([len(ds) for ds in self.real_image_datasets])
        self.scores = np.zeros(self.metagraph.n, dtype=np.float32)
        self._fake_prob = config.fake_prob

    def update_scores(self, rewards, miner_uids):
        pass

    def save_miner_history(self):
        pass