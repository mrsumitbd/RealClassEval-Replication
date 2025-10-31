from torch_sim.state import SimState, concatenate_states
from itertools import chain
from torch_sim.models.interface import ModelInterface
from collections.abc import Callable, Iterator
from torch_sim.typing import MemoryScaling

class BinningAutoBatcher:
    """Batcher that groups states into bins of similar computational cost.

    Divides a collection of states into batches that can be processed efficiently
    without exceeding GPU memory. States are grouped based on a memory scaling
    metric to maximize GPU utilization. This approach is ideal for scenarios where
    all states need to be evolved the same number of steps.

    To avoid a slow memory estimation step, set the `max_memory_scaler` to a
    known value.

    Attributes:
        model (ModelInterface): Model used for memory estimation and processing.
        memory_scales_with (str): Metric type used for memory estimation.
        max_memory_scaler (float): Maximum memory metric allowed per system.
        max_atoms_to_try (int): Maximum number of atoms to try when estimating memory.
        return_indices (bool): Whether to return original indices with batches.
        state_slices (list[SimState]): Individual states to be batched.
        memory_scalers (list[float]): Memory scaling metrics for each state.
        index_to_scaler (dict): Mapping from state index to its scaling metric.
        index_bins (list[list[int]]): Groups of state indices that can be batched
            together.
        batched_states (list[list[SimState]]): Grouped states ready for batching.
        current_state_bin (int): Index of the current batch being processed.

    Example::

        # Create a batcher with a Lennard-Jones model
        batcher = BinningAutoBatcher(
            model=lj_model, memory_scales_with="n_atoms", max_memory_scaler=1000.0
        )

        # Load states and process them in batches
        batcher.load_states(states)
        final_states = []
        for batch in batcher:
            final_states.append(evolve_batch(batch))

        # Restore original order
        ordered_final_states = batcher.restore_original_order(final_states)
    """

    def __init__(self, model: ModelInterface, *, memory_scales_with: MemoryScaling='n_atoms_x_density', max_memory_scaler: float | None=None, return_indices: bool=False, max_atoms_to_try: int=500000, memory_scaling_factor: float=1.6, max_memory_padding: float=1.0) -> None:
        """Initialize the binning auto-batcher.

        Args:
            model (ModelInterface): Model to batch for, used to estimate memory
                requirements.
            memory_scales_with ("n_atoms" | "n_atoms_x_density"): Metric to use
                for estimating memory requirements:
                - "n_atoms": Uses only atom count
                - "n_atoms_x_density": Uses atom count multiplied by number density
                Defaults to "n_atoms_x_density".
            max_memory_scaler (float | None): Maximum metric value allowed per system. If
                None, will be automatically estimated. Defaults to None.
            return_indices (bool): Whether to return original indices along with batches.
                Defaults to False.
            max_atoms_to_try (int): Maximum number of atoms to try when estimating
                max_memory_scaler. Defaults to 500,000.
            memory_scaling_factor (float): Factor to multiply batch size by in each
                iteration. Larger values will get a batch size more quickly, smaller
                values will get a more accurate limit. Must be greater than 1. Defaults
                to 1.6.
            max_memory_padding (float): Multiply the autodetermined max_memory_scaler
                by this value to account for fluctuations in max memory. Defaults to 1.0.
        """
        self.max_memory_scaler = max_memory_scaler
        self.max_atoms_to_try = max_atoms_to_try
        self.memory_scales_with = memory_scales_with
        self.return_indices = return_indices
        self.model = model
        self.memory_scaling_factor = memory_scaling_factor
        self.max_memory_padding = max_memory_padding

    def load_states(self, states: list[SimState] | SimState) -> float:
        """Load new states into the batcher.

        Processes the input states, computes memory scaling metrics for each,
        and organizes them into optimal batches using a bin-packing algorithm
        to maximize GPU utilization.

        Args:
            states (list[SimState] | SimState): Collection of states to batch. Either a
                list of individual SimState objects or a single batched SimState that
                will be split into individual states. Each SimState has shape
                information specific to its instance.

        Returns:
            float: Maximum memory scaling metric that fits in GPU memory.

        Raises:
            ValueError: If any individual state has a memory scaling metric greater
                than the maximum allowed value.

        Example::

            # Load individual states
            batcher.load_states([state1, state2, state3])

            # Or load a batched state that will be split
            batcher.load_states(batched_state)

        Notes:
            This method resets the current state bin index, so any ongoing iteration
            will be restarted when this method is called.
        """
        self.state_slices = states.split() if isinstance(states, SimState) else states
        self.memory_scalers = [calculate_memory_scaler(state_slice, self.memory_scales_with) for state_slice in self.state_slices]
        if not self.max_memory_scaler:
            self.max_memory_scaler = estimate_max_memory_scaler(self.model, self.state_slices, self.memory_scalers, max_atoms=self.max_atoms_to_try, scale_factor=self.memory_scaling_factor)
            self.max_memory_scaler = self.max_memory_scaler * self.max_memory_padding
        max_metric_value = max(self.memory_scalers)
        max_metric_idx = self.memory_scalers.index(max_metric_value)
        if max_metric_value > self.max_memory_scaler:
            raise ValueError(f'Max metric of system with index {max_metric_idx} in states: {max(self.memory_scalers)} is greater than max_metric {self.max_memory_scaler}, please set a larger max_metric or run smaller systems metric.')
        self.index_to_scaler = dict(enumerate(self.memory_scalers))
        self.index_bins = to_constant_volume_bins(self.index_to_scaler, max_volume=self.max_memory_scaler)
        self.batched_states = []
        for index_bin in self.index_bins:
            self.batched_states.append([self.state_slices[i] for i in index_bin])
        self.current_state_bin = 0
        return self.max_memory_scaler

    def next_batch(self, *, return_indices: bool=False) -> SimState | tuple[SimState, list[int]] | None:
        """Get the next batch of states.

        Returns batches sequentially until all states have been processed. Each batch
        contains states grouped together to maximize GPU utilization without exceeding
        memory constraints.

        Args:
            return_indices (bool): Whether to return original indices along with the
                batch. Overrides the value set during initialization. Defaults to False.

        Returns:
            SimState | tuple[SimState, list[int]] | None:
                - If return_indices is False: A concatenated SimState containing the next
                  batch of states, or None if no more batches.
                - If return_indices is True: Tuple of (concatenated SimState, indices),
                  where indices are the original positions of the states, or None if no
                  more batches.

        Example::

            # Get batches one by one
            all_converged_state, convergence = [], None
            while (result := batcher.next_batch(state, convergence))[0] is not None:
                state, converged_states = result
                all_converged_states.extend(converged_states)

                evolve_batch(state)
                convergence = convergence_criterion(state)
            else:
                all_converged_states.extend(result[1])

        """
        if self.current_state_bin < len(self.batched_states):
            state_bin = self.batched_states[self.current_state_bin]
            state = concatenate_states(state_bin)
            self.current_state_bin += 1
            if return_indices:
                return (state, self.index_bins[self.current_state_bin - 1])
            return state
        return None

    def __iter__(self) -> Iterator[SimState | tuple[SimState, list[int]]]:
        """Return self as an iterator.

        Allows using the batcher in a for loop to iterate through all batches.
        Resets the current state bin index to start iteration from the beginning.

        Returns:
            Iterator[SimState | tuple[SimState, list[int]]]: Self as an iterator.

        Example::

            # Iterate through all batches
            for batch in batcher:
                process_batch(batch)

        """
        return self

    def __next__(self) -> SimState | tuple[SimState, list[int]]:
        """Get the next batch for iteration.

        Implements the iterator protocol to allow using the batcher in a for loop.
        Automatically includes indices if return_indices was set to True during
        initialization.

        Returns:
            SimState | tuple[SimState, list[int]]: The next batch of states,
                potentially with indices.

        Raises:
            StopIteration: When there are no more batches.
        """
        next_batch = self.next_batch(return_indices=self.return_indices)
        if next_batch is None:
            raise StopIteration
        return next_batch

    def restore_original_order(self, batched_states: list[SimState]) -> list[SimState]:
        """Reorder processed states back to their original sequence.

        Takes states that were processed in batches and restores them to the
        original order they were provided in. This is essential after batch
        processing to ensure results correspond to the input states.

        Args:
            batched_states (list[SimState]): State batches to reorder. These can be
                either concatenated batch states that will be split, or already
                split individual states.

        Returns:
            list[SimState]: States in their original order, with shape information
                matching the original input states.

        Raises:
            ValueError: If the number of states doesn't match the number of
                original indices.

        Example::

            # Process batches and restore original order
            results = []
            for batch in batcher:
                results.append(process_batch(batch))
            ordered_results = batcher.restore_original_order(results)

        """
        state_bins = [state.split() for state in batched_states]
        all_states = list(chain.from_iterable(state_bins))
        original_indices = list(chain.from_iterable(self.index_bins))
        if len(all_states) != len(original_indices):
            raise ValueError(f'Number of states ({len(all_states)}) does not match number of original indices ({len(original_indices)})')
        indexed_states = list(zip(original_indices, all_states, strict=True))
        return [state for _, state in sorted(indexed_states, key=lambda x: x[0])]