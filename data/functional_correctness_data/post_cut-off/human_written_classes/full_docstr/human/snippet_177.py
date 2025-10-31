import torch
from collections.abc import Callable
from torch_sim.state import SimState

class CorrelationCalculator:
    """Efficient on-the-fly correlation function calculator.

    Manage the calculation of time correlation functions during
    simulation, with support for both autocorrelation and cross-correlation
    of arbitrary properties. It maintains a sliding window of historical data
    and performs efficient updates.

    Attributes:
        window_size: Number of steps to keep in memory
        properties: Map of property names to their calculators
        buffers: Circular buffers for storing historical data
        correlations: Current correlation results
        device: Device where calculations are performed

    Example:
    Computing correlation function in loop::

        corr_calc = CorrelationCalculator(
            window_size=100,
            properties={"velocity": lambda state: state.velocities},
        )

        for step in range(n_steps):
            state = integrator.step(state)
            # Call update at desired frequency
            if step % 10 == 0:  # Sample every 10 steps
                corr_calc.update(state)

            # Periodically retrieve correlation functions
            if step % 1000 == 0:
                acfs = corr_calc.get_auto_correlations()
                # Process or save acfs...
    """

    def __init__(self, *, window_size: int, properties: dict[str, Callable[[SimState], torch.Tensor]], device: torch.device, normalize: bool=True) -> None:
        """Initialize a correlation calculator.

        Args:
            window_size: Number of steps to keep in memory
            properties: Dictionary mapping names to functions that calculate
                       properties from a SimState
            device: Device for tensor storage and computation
            normalize: Whether to normalize correlation functions to [0,1]
        """
        self.window_size = window_size
        self.properties = properties or {}
        self.device = device
        self.normalize = normalize
        self.buffers = {name: CircularBuffer(window_size, device=device) for name in self.properties}
        self.correlations: dict[str, torch.Tensor] = {}
        self.cross_correlations: dict[tuple[str, str], torch.Tensor] = {}

    def add_property(self, name: str, calculator: Callable[[SimState], torch.Tensor]) -> None:
        """Track a new simulation property.

        Args:
            name: Name of the property
            calculator: Function that calculates property from a SimState
        """
        if name in self.properties:
            raise ValueError(f'Property {name} already exists')
        self.properties[name] = calculator
        self.buffers[name] = CircularBuffer(self.window_size, device=self.device)

    def update(self, state: SimState) -> None:
        """Update correlation calculations with new state data.

        Args:
            state: Current simulation state
        """
        buffer_count = 0
        buffer_total = len(self.buffers)
        for name, calc in self.properties.items():
            value = calc(state)
            self.buffers[name].append(value)
            if self.buffers[name].count > 1:
                buffer_count += 1
        if buffer_count == buffer_total and buffer_total > 0:
            self._compute_correlations()

    def _compute_correlations(self) -> None:
        """Compute correlation functions using FFT for efficiency."""
        for name, buf in self.buffers.items():
            data = buf.get_array()
            if len(data) == 0:
                continue
            original_shape = data.shape
            if len(original_shape) > 1:
                data = data.reshape(original_shape[0], -1)
            n_dims = data.shape[1] if len(data.shape) > 1 else 1
            if n_dims > 1:
                acf = torch.zeros((original_shape[0], n_dims), device=self.device, dtype=data.dtype)
                data_centered = data - data.mean(dim=0, keepdim=True)
                if data_centered.shape[1] <= 128:
                    data_batch = data_centered.T
                    n_fft = 2 * data_batch.shape[1]
                    fft_batch = torch.fft.rfft(data_batch, n=n_fft)
                    power_batch = torch.abs(fft_batch) ** 2
                    corr_batch = torch.fft.irfft(power_batch)[:, :data_batch.shape[1]]
                    corr_batch = corr_batch.T
                    if self.normalize:
                        norms = corr_batch[0].clone()
                        mask = norms > 1e-10
                        if mask.any():
                            corr_batch[:, mask] = corr_batch[:, mask] / norms[mask].unsqueeze(0)
                    acf = corr_batch.reshape(original_shape)
                else:
                    for i in range(n_dims):
                        dim_data = data_centered[:, i]
                        n_fft = 2 * len(dim_data)
                        fft = torch.fft.rfft(dim_data, n=n_fft)
                        power = torch.abs(fft) ** 2
                        corr = torch.fft.irfft(power)[:len(dim_data)]
                        if self.normalize and corr[0] > 1e-10:
                            corr = corr / corr[0]
                        acf[:, i] = corr
                    acf = acf.reshape(original_shape)
            else:
                dim_data = data - data.mean()
                n_fft = 2 * len(dim_data)
                fft = torch.fft.rfft(dim_data, n=n_fft)
                power = torch.abs(fft) ** 2
                corr = torch.fft.irfft(power)[:len(dim_data)]
                if self.normalize and corr[0] > 1e-10:
                    corr = corr / corr[0]
                acf = corr
            self.correlations[name] = acf
        names = list(self.buffers)
        for i, name1 in enumerate(names):
            for name2 in names[i + 1:]:
                data1 = self.buffers[name1].get_array()
                data2 = self.buffers[name2].get_array()
                if len(data1) == 0 or len(data2) == 0:
                    continue
                min_len = min(len(data1), len(data2))
                data1 = data1[:min_len]
                data2 = data2[:min_len]
                if len(data1.shape) > 1 or len(data2.shape) > 1:
                    if len(data1.shape) > 1:
                        non_time_dims = tuple(range(1, len(data1.shape)))
                        data1 = torch.mean(data1, dim=non_time_dims)
                    if len(data2.shape) > 1:
                        non_time_dims = tuple(range(1, len(data2.shape)))
                        data2 = torch.mean(data2, dim=non_time_dims)
                data1 = data1 - data1.mean()
                data2 = data2 - data2.mean()
                n_fft = 2 * min_len
                fft1 = torch.fft.rfft(data1, n=n_fft)
                fft2 = torch.fft.rfft(data2, n=n_fft)
                ccf = torch.fft.irfft(fft1 * fft2.conj())[:min_len]
                if self.normalize and torch.abs(ccf[0]) > 1e-10:
                    ccf = ccf / ccf[0]
                self.cross_correlations[name1, name2] = ccf

    def get_auto_correlations(self) -> dict[str, torch.Tensor]:
        """Get autocorrelation results.

        Returns:
            Dictionary mapping property names to their correlation tensors
        """
        return self.correlations

    def get_cross_correlations(self) -> dict[tuple[str, str], torch.Tensor]:
        """Get cross-correlation results.

        Returns:
            Dictionary mapping pairs of property names to their
            cross-correlation tensors
        """
        return self.cross_correlations

    def reset(self) -> None:
        """Reset all buffers and correlations."""
        self.buffers = {name: CircularBuffer(self.window_size, device=self.device) for name in self.properties}
        self.correlations = {}
        self.cross_correlations = {}

    def to(self, device: torch.device) -> 'CorrelationCalculator':
        """Move calculator to specified device.

        Args:
            device: Target device

        Returns:
            Self, for method chaining
        """
        if self.device == device:
            return self
        self.device = device
        new_buffers = {}
        for name, buf in self.buffers.items():
            new_buf = CircularBuffer(self.window_size, device=device)
            if buf.buffer is not None:
                data = buf.get_array().to(device)
                if len(data) > 100:
                    batch_size = 20
                    for i in range(0, len(data), batch_size):
                        batch = data[i:min(i + batch_size, len(data))]
                        for j in range(len(batch)):
                            new_buf.append(batch[j])
                else:
                    for i in range(len(data)):
                        new_buf.append(data[i])
            new_buffers[name] = new_buf
        self.buffers = new_buffers
        if self.correlations:
            self.correlations = {name: corr.to(device) for name, corr in self.correlations.items()}
        if self.cross_correlations:
            self.cross_correlations = {names: corr.to(device) for names, corr in self.cross_correlations.items()}
        return self