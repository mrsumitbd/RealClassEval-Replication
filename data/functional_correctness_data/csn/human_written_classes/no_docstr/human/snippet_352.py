from math import sqrt
from glob import glob
import numpy as np
from precise.util import load_audio
from os.path import join, dirname, abspath, splitext

class NoiseData:

    def __init__(self, noise_folder: str):
        self.noise_data = [load_audio(file) for file in glob(join(noise_folder, '*.wav'))]
        self.noise_data_id = 0
        self.noise_pos = 0
        self.repeat_count = 0

    def get_fresh_noise(self, n: int) -> np.ndarray:
        noise_audio = np.empty(0)
        while len(noise_audio) < n:
            noise_source = self.noise_data[self.noise_data_id]
            noise_chunk = noise_source[self.noise_pos:self.noise_pos + n - len(noise_audio)]
            self.noise_pos += n - len(noise_audio)
            if self.noise_pos >= len(noise_source):
                self.noise_pos = 0
                self.noise_data_id += 1
                if self.noise_data_id >= len(self.noise_data):
                    self.noise_data_id = 0
                    self.repeat_count += 1
                    if self.repeat_count == 100:
                        print('Warning: Repeating noise 100+ times. Add more to prevent overfitting.')
            noise_audio = np.concatenate([noise_audio, noise_chunk])
        return noise_audio

    def noised_audio(self, audio: np.ndarray, noise_ratio: float) -> np.ndarray:
        noise_data = self.get_fresh_noise(len(audio))
        audio_volume = sqrt(sum(audio ** 2))
        noise_volume = sqrt(sum(noise_data ** 2))
        adjusted_noise = audio_volume * noise_data / noise_volume
        return noise_ratio * adjusted_noise + (1.0 - noise_ratio) * audio