import threading
from torch.utils.data import DataLoader
import traceback
from collections.abc import Callable, Iterator
from cosmos_predict2.datasets.watchdog import OperationWatchdog
import numpy as np

class CachedReplayDataLoader:
    """A DataLoader wrapper that asynchronously caches and replays data batches to
    mitigate slow loading issues. Assumes the underlying DataLoader is infinite.

    This class delegates all augmentation logic to an external augmentation function,
    which takes a batch from the data loader and returns multiple augmented versions.
    The class handles caching these augmented batches and optionally concatenating
    them when yielded.

    Attributes:
        data_loader (DataLoader): The underlying infinite DataLoader.
        cache_size (int): Maximum number of augmented batches to store in the cache.
        cache_augmentation_fn (Callable): Function to create multiple augmented versions of each batch.
        concat_size (int): Number of batches to concatenate when yielding from the iterator.
        rng (numpy.random.Generator): Controlled random number generator for deterministic behavior.
    """

    def __init__(self, data_loader: DataLoader, cache_size: int, cache_augmentation_fn: Callable[[dict], list[dict]], concat_size: int=1, name: str='cached_replay_dataloader') -> None:
        """Initialize the CachedReplayDataLoader.

        Args:
            data_loader (DataLoader): The infinite DataLoader to fetch data batches from.
            cache_size (int): Maximum number of augmented data batches to store in the cache.
            cache_augmentation_fn (Callable[[Dict], List[Dict]]): Function that takes a batch and returns
                a list of augmented batches.
            concat_size (int, optional): Number of batches to concatenate when yielding. Defaults to 1.
        """
        self.data_loader = data_loader
        self.cache_size = cache_size
        self.cache_augmentation_fn = cache_augmentation_fn
        self.concat_size = concat_size
        self.rng = np.random.default_rng(123)
        self._data_iter: Iterator = iter(self.data_loader)
        self._cache: list[dict] = []
        self._cache_cond = threading.Condition()
        self._stop_event = threading.Event()
        self._prefetch_exception = None
        self._watchdog = OperationWatchdog(warning_threshold=100, verbose_interval=600, name=name)
        self._prefetch_thread = threading.Thread(target=self._prefetch_loop, daemon=True, name=f'{name}_prefetch_thread')
        self._prefetch_thread.start()

    def _prefetch_loop(self) -> None:
        """Continuously fetch batches from the DataLoader, augment them, and store in the cache.

        If the cache is full (reaches `cache_size`), this loop waits until space is available.
        Catches exceptions and stores them for later propagation to the main thread.
        """
        try:
            while not self._stop_event.is_set():
                try:
                    with self._watchdog.watch('fetch raw batch', verbose_first_n=5):
                        batch = next(self._data_iter)
                except Exception as e:
                    self._set_exception(e, 'Error fetching batch from DataLoader')
                    break
                try:
                    with self._watchdog.watch('augmentation', verbose_first_n=5):
                        augmented_batches = self.cache_augmentation_fn(batch)
                except Exception as e:
                    self._set_exception(e, 'Error in augmentation function')
                    break
                try:
                    permutation = self.rng.permutation(len(augmented_batches))
                    augmented_batches = [augmented_batches[i] for i in permutation]
                    for aug_batch in augmented_batches:
                        with self._cache_cond:
                            while len(self._cache) >= self.cache_size and (not self._stop_event.is_set()):
                                self._cache_cond.wait(timeout=1.0)
                            if self._stop_event.is_set():
                                break
                            self._cache.append(aug_batch)
                            self._cache_cond.notify_all()
                except Exception as e:
                    self._set_exception(e, 'Error adding batch to cache')
                    break
        except Exception as e:
            self._set_exception(e, 'Unexpected error in prefetch thread')

    def _set_exception(self, exception: Exception, context: str='') -> None:
        """Store an exception from the background thread with context information.

        Args:
            exception (Exception): The exception that was raised
            context (str, optional): Additional context about where the error occurred
        """
        error_info = f'{context}: {exception!s}\n{traceback.format_exc()}'
        with self._cache_cond:
            self._prefetch_exception = RuntimeError(error_info)
            self._cache_cond.notify_all()

    def _check_for_errors(self) -> None:
        """Check if the background thread has encountered an error and raise it if so."""
        if self._prefetch_exception is not None:
            raise self._prefetch_exception

    def __iter__(self) -> Iterator[dict]:
        """Yield augmented data batches from the cache, optionally concatenated based on concat_size.

        This method starts the background prefetch thread if it hasn't been started yet.
        If concat_size > 1, it collects multiple batches and concatenates them.

        Raises:
            RuntimeError: If the background thread encountered an error
        """
        while not self._stop_event.is_set():
            if self.concat_size <= 1:
                with self._watchdog.watch('main thread fetch single batch', verbose_first_n=5):
                    with self._cache_cond:
                        while not self._cache and (not self._stop_event.is_set()) and (self._prefetch_exception is None):
                            self._cache_cond.wait(timeout=1.0)
                        self._check_for_errors()
                        if self._stop_event.is_set():
                            break
                        if not self._cache:
                            continue
                        idx = self.rng.integers(0, len(self._cache))
                        batch = self._cache.pop(idx)
                        self._cache_cond.notify_all()
                yield batch
            else:
                with self._watchdog.watch('main thread fetch smaples', verbose_first_n=5):
                    collected_batches = []
                    for _ in range(self.concat_size):
                        with self._cache_cond:
                            while not self._cache and (not self._stop_event.is_set()) and (self._prefetch_exception is None):
                                self._cache_cond.wait(timeout=1.0)
                            self._check_for_errors()
                            if self._stop_event.is_set():
                                break
                            if not self._cache:
                                continue
                            idx = self.rng.integers(0, len(self._cache))
                            batch = self._cache.pop(idx)
                            self._cache_cond.notify_all()
                        collected_batches.append(batch)
                if self._stop_event.is_set():
                    break
                if not collected_batches:
                    continue
                if len(collected_batches) < self.concat_size:
                    concat_batches = concatenate_batches(len(collected_batches), collected_batches)
                    yield concat_batches[0]
                else:
                    try:
                        concat_batches = concatenate_batches(self.concat_size, collected_batches)
                        yield concat_batches[0]
                    except Exception as e:
                        raise RuntimeError(f'Error concatenating batches: {e!s}') from e

    def __len__(self) -> int:
        """Return the length of the underlying DataLoader."""
        return len(self.data_loader)

    def close(self) -> None:
        """Stop the prefetch thread and clear the cache.
        Also checks for any errors in the background thread and raises them.
        """
        self._stop_event.set()
        with self._cache_cond:
            self._cache_cond.notify_all()
        if self._prefetch_thread is not None:
            self._prefetch_thread.join(timeout=5.0)
        with self._cache_cond:
            self._cache.clear()
        self._check_for_errors()