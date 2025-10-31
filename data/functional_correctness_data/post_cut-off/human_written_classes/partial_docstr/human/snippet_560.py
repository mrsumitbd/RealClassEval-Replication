from pathlib import Path
from zea.io_lib import load_video
from zea.utils import translate
import numpy as np
from zea.data import generate_zea_dataset

class H5Processor:
    """
    Stores a few variables and paths to allow for hyperthreading.
    """

    def __init__(self, path_out_h5, path_out=None, num_val=500, num_test=500, range_from=(0, 255), range_to=(-60, 0), splits=None):
        self.path_out_h5 = Path(path_out_h5)
        self.path_out = Path(path_out) if path_out else None
        self.num_val = num_val
        self.num_test = num_test
        self.range_from = range_from
        self.range_to = range_to
        self.splits = splits
        self._process_range = (0, 1)
        for folder in ['train', 'val', 'test', 'rejected']:
            if self._to_numpy:
                (self.path_out / folder).mkdir(parents=True, exist_ok=True)
            (self.path_out_h5 / folder).mkdir(parents=True, exist_ok=True)

    @property
    def _to_numpy(self):
        return self.path_out is not None

    def translate(self, data):
        """Translate the data from the processing range to final range."""
        return translate(data, self._process_range, self.range_to)

    def get_split(self, hdf5_file: str, sequence):
        """Determine the split for a given file."""
        accepted = accept_shape(sequence[0])
        if self.splits is not None:
            split = find_split_for_file(self.splits, hdf5_file)
            assert accepted == (split != 'rejected'), 'Rejection mismatch'
            return split
        if not accepted:
            return 'rejected'
        val_counter = len(list((self.path_out_h5 / 'val').iterdir()))
        test_counter = len(list((self.path_out_h5 / 'test').iterdir()))
        if val_counter < self.num_val:
            return 'val'
        elif test_counter < self.num_test:
            return 'test'
        else:
            return 'train'

    def __call__(self, avi_file):
        """
        Processes a single h5 file using the class variables and the filename given.
        """
        hdf5_file = avi_file.stem + '.hdf5'
        sequence = load_video(avi_file)
        assert sequence.min() >= self.range_from[0], f'{sequence.min()} < {self.range_from[0]}'
        assert sequence.max() <= self.range_from[1], f'{sequence.max()} > {self.range_from[1]}'
        sequence = translate(sequence, self.range_from, self._process_range)
        sequence = segment(sequence, number_erasing=0, min_clip=0)
        split = self.get_split(hdf5_file, sequence)
        accepted = split != 'rejected'
        out_h5 = self.path_out_h5 / split / hdf5_file
        if self._to_numpy:
            out_dir = self.path_out / split / avi_file.stem
            out_dir.mkdir(parents=True, exist_ok=True)
        polar_im_set = []
        for i, im in enumerate(sequence):
            if self._to_numpy:
                np.save(out_dir / f'sc{str(i).zfill(3)}.npy', im)
            if not accepted:
                continue
            polar_im = cartesian_to_polar_matrix(im, interpolation='cubic')
            polar_im = np.clip(polar_im, *self._process_range)
            if self._to_numpy:
                np.save(out_dir / f'polar{str(i).zfill(3)}.npy', polar_im)
            polar_im_set.append(polar_im)
        if accepted:
            polar_im_set = np.stack(polar_im_set, axis=0)
        assert sequence.min() >= self._process_range[0], sequence.min()
        assert sequence.max() <= self._process_range[1], sequence.max()
        zea_dataset = {'path': out_h5, 'image_sc': self.translate(sequence), 'probe_name': 'generic', 'description': 'EchoNet dataset converted to zea format'}
        if accepted:
            zea_dataset['image'] = self.translate(polar_im_set)
        return generate_zea_dataset(**zea_dataset)