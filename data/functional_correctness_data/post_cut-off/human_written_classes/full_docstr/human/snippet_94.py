from pathlib import Path
import numpy as np
from ultralytics.utils import DATASETS_DIR, LOGGER, NUM_THREADS, ROOT, SETTINGS_FILE, TQDM, clean_url, colorstr, emojis, is_dir_writeable, yaml_load, yaml_save
import json
from ultralytics.utils.downloads import download, safe_download, unzip_file
from multiprocessing.pool import ThreadPool

class HUBDatasetStats:
    """
    A class for generating HUB dataset JSON and `-hub` dataset directory.

    Args:
        path (str): Path to data.yaml or data.zip (with data.yaml inside data.zip). Default is 'coco8.yaml'.
        task (str): Dataset task. Options are 'detect', 'segment', 'pose', 'classify'. Default is 'detect'.
        autodownload (bool): Attempt to download dataset if not found locally. Default is False.

    Example:
        Download *.zip files from https://github.com/ultralytics/hub/tree/main/example_datasets
            i.e. https://github.com/ultralytics/hub/raw/main/example_datasets/coco8.zip for coco8.zip.
        ```python
        from ultralytics.data.utils import HUBDatasetStats

        stats = HUBDatasetStats("path/to/coco8.zip", task="detect")  # detect dataset
        stats = HUBDatasetStats("path/to/coco8-seg.zip", task="segment")  # segment dataset
        stats = HUBDatasetStats("path/to/coco8-pose.zip", task="pose")  # pose dataset
        stats = HUBDatasetStats("path/to/dota8.zip", task="obb")  # OBB dataset
        stats = HUBDatasetStats("path/to/imagenet10.zip", task="classify")  # classification dataset

        stats.get_json(save=True)
        stats.process_images()
        ```
    """

    def __init__(self, path='coco8.yaml', task='detect', autodownload=False):
        """Initialize class."""
        path = Path(path).resolve()
        LOGGER.info(f'Starting HUB dataset checks for {path}....')
        self.task = task
        if self.task == 'classify':
            unzip_dir = unzip_file(path)
            data = check_cls_dataset(unzip_dir)
            data['path'] = unzip_dir
        else:
            _, data_dir, yaml_path = self._unzip(Path(path))
            try:
                data = yaml_load(yaml_path)
                data['path'] = ''
                yaml_save(yaml_path, data)
                data = check_det_dataset(yaml_path, autodownload)
                data['path'] = data_dir
            except Exception as e:
                raise Exception('error/HUB/dataset_stats/init') from e
        self.hub_dir = Path(f"{data['path']}-hub")
        self.im_dir = self.hub_dir / 'images'
        self.stats = {'nc': len(data['names']), 'names': list(data['names'].values())}
        self.data = data

    @staticmethod
    def _unzip(path):
        """Unzip data.zip."""
        if not str(path).endswith('.zip'):
            return (False, None, path)
        unzip_dir = unzip_file(path, path=path.parent)
        assert unzip_dir.is_dir(), f'Error unzipping {path}, {unzip_dir} not found. path/to/abc.zip MUST unzip to path/to/abc/'
        return (True, str(unzip_dir), find_dataset_yaml(unzip_dir))

    def _hub_ops(self, f):
        """Saves a compressed image for HUB previews."""
        compress_one_image(f, self.im_dir / Path(f).name)

    def get_json(self, save=False, verbose=False):
        """Return dataset JSON for Ultralytics HUB."""

        def _round(labels):
            """Update labels to integer class and 4 decimal place floats."""
            if self.task == 'detect':
                coordinates = labels['bboxes']
            elif self.task in {'segment', 'obb'}:
                coordinates = [x.flatten() for x in labels['segments']]
            elif self.task == 'pose':
                n, nk, nd = labels['keypoints'].shape
                coordinates = np.concatenate((labels['bboxes'], labels['keypoints'].reshape(n, nk * nd)), 1)
            else:
                raise ValueError(f'Undefined dataset task={self.task}.')
            zipped = zip(labels['cls'], coordinates)
            return [[int(c[0]), *(round(float(x), 4) for x in points)] for c, points in zipped]
        for split in ('train', 'val', 'test'):
            self.stats[split] = None
            path = self.data.get(split)
            if path is None:
                continue
            files = [f for f in Path(path).rglob('*.*') if f.suffix[1:].lower() in IMG_FORMATS]
            if not files:
                continue
            if self.task == 'classify':
                from torchvision.datasets import ImageFolder
                dataset = ImageFolder(self.data[split])
                x = np.zeros(len(dataset.classes)).astype(int)
                for im in dataset.imgs:
                    x[im[1]] += 1
                self.stats[split] = {'instance_stats': {'total': len(dataset), 'per_class': x.tolist()}, 'image_stats': {'total': len(dataset), 'unlabelled': 0, 'per_class': x.tolist()}, 'labels': [{Path(k).name: v} for k, v in dataset.imgs]}
            else:
                from ultralytics.data import YOLODataset
                dataset = YOLODataset(img_path=self.data[split], data=self.data, task=self.task)
                x = np.array([np.bincount(label['cls'].astype(int).flatten(), minlength=self.data['nc']) for label in TQDM(dataset.labels, total=len(dataset), desc='Statistics')])
                self.stats[split] = {'instance_stats': {'total': int(x.sum()), 'per_class': x.sum(0).tolist()}, 'image_stats': {'total': len(dataset), 'unlabelled': int(np.all(x == 0, 1).sum()), 'per_class': (x > 0).sum(0).tolist()}, 'labels': [{Path(k).name: _round(v)} for k, v in zip(dataset.im_files, dataset.labels)]}
        if save:
            self.hub_dir.mkdir(parents=True, exist_ok=True)
            stats_path = self.hub_dir / 'stats.json'
            LOGGER.info(f'Saving {stats_path.resolve()}...')
            with open(stats_path, 'w') as f:
                json.dump(self.stats, f)
        if verbose:
            LOGGER.info(json.dumps(self.stats, indent=2, sort_keys=False))
        return self.stats

    def process_images(self):
        """Compress images for Ultralytics HUB."""
        from ultralytics.data import YOLODataset
        self.im_dir.mkdir(parents=True, exist_ok=True)
        for split in ('train', 'val', 'test'):
            if self.data.get(split) is None:
                continue
            dataset = YOLODataset(img_path=self.data[split], data=self.data)
            with ThreadPool(NUM_THREADS) as pool:
                for _ in TQDM(pool.imap(self._hub_ops, dataset.im_files), total=len(dataset), desc=f'{split} images'):
                    pass
        LOGGER.info(f'Done. All images saved to {self.im_dir}')
        return self.im_dir