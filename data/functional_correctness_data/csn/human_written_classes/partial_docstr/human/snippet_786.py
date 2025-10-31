import bisect
import math
import random
import numpy as np

class MultiFramePartitionData:
    """
    Wrapper for PartitionData to access chunks of frames via indexes.

    Args:
        partition_data (PartitionData): The loaded partition-data.
        frames_per_chunk (int): Number of subsequent frames in a chunk.
        return_length (bool): If True, the length of the chunk is returned as well. (default ``False``)
                              The length is appended to tuple as the last element.
                              (e.g. [container1-data, container2-data, length])
        pad (bool): If True, samples that are shorter are padded with zeros to match ``frames_per_chunk``.
                    If padding is enabled, the lengths are always returned ``return_length = True``.
        shuffle (bool): If True the frames are shuffled randomly for access.
        seed (int): The seed to use for shuffling.
    """

    def __init__(self, partition_data, frames_per_chunk, return_length=False, pad=False, shuffle=True, seed=None):
        if frames_per_chunk < 1:
            raise ValueError('Number of frames per chunk has to higher than 0.')
        self.data = partition_data
        self.frames_per_chunk = frames_per_chunk
        self.pad = pad
        if self.pad:
            self.return_length = True
        else:
            self.return_length = return_length
        self.shuffle = shuffle
        self.rand = random.Random()
        self.rand.seed(a=seed)
        self.regions = self.get_utt_regions()
        self.region_offsets = [x[0] for x in self.regions]
        self.sampling = list(range(len(self)))
        if self.shuffle:
            self.rand.shuffle(self.sampling)

    def __len__(self):
        last_region = self.regions[-1]
        return last_region[0] + last_region[1]

    def __getitem__(self, item):
        index = self.sampling[item]
        region_index = bisect.bisect_right(self.region_offsets, index) - 1
        region = self.regions[region_index]
        frame_offset = (index - region[0]) * self.frames_per_chunk
        frame_end = frame_offset + self.frames_per_chunk
        data = [x[frame_offset:frame_end].astype(np.float32) for x in region[2]]
        size = data[0].shape[0]
        if self.pad and size < self.frames_per_chunk:
            padded_data = []
            for x in data:
                pad_widths = [(0, 0)] * (len(x.shape) - 1)
                pad_widths.insert(0, (0, self.frames_per_chunk - size))
                padded_x = np.pad(x, pad_widths, mode='constant', constant_values=0)
                padded_data.append(padded_x)
            data = padded_data
        if self.return_length:
            data.append(size)
        return data

    def get_utt_regions(self):
        """
        Return the regions of all utterances, assuming all utterances are concatenated.
        A region is defined by offset, length (num-frames) and
        a list of references to the utterance datasets in the containers.

        Returns:
            list: List of with a tuple for every utterances containing the region info.
        """
        regions = []
        current_offset = 0
        for utt_idx, utt_data in zip(self.data.info.utt_ids, self.data.utt_data):
            offset = current_offset
            num_frames = []
            refs = []
            for part in utt_data:
                num_frames.append(part.shape[0])
                refs.append(part)
            if len(set(num_frames)) != 1:
                raise ValueError('Utterance {} has not the same number of frames in all containers!'.format(utt_idx))
            num_chunks = math.ceil(num_frames[0] / float(self.frames_per_chunk))
            region = (offset, num_chunks, refs)
            regions.append(region)
            current_offset += num_chunks
        return regions