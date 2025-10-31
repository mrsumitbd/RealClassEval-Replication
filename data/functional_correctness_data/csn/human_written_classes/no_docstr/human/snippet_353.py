from precise.params import pr, inject_params
import attr

@attr.s()
class Metric:
    chunk_size = attr.ib()
    seconds = attr.ib(0.0)
    activated_chunks = attr.ib(0)
    activations = attr.ib(0)
    activation_sum = attr.ib(0.0)

    @property
    def days(self):
        return self.seconds / (60 * 60 * 24)

    def add(self, other):
        self.seconds += other.seconds
        self.activated_chunks += other.activated_chunks
        self.activations += other.activations
        self.activation_sum += other.activation_sum

    @property
    def chunks(self):
        return self.seconds * pr.sample_rate / self.chunk_size

    def info_string(self, title):
        return '=== {title} ===\nHours: {hours:.2f}\nActivations / Day: {activations_per_day:.2f}\nActivated Chunks / Day: {chunks_per_day:.2f}\nAverage Activation (*100): {average_activation:.2f}'.format(title=title, hours=self.days * 24, activations_per_day=self.activations / self.days, chunks_per_day=self.activated_chunks / self.days, average_activation=100.0 * self.activation_sum / self.chunks)