import torch

class VoiceActivityDetector:

    def __init__(self, threshold=0.5, frame_rate=16000):
        """
        Initializes the VoiceActivityDetector with a voice activity detection model and a threshold.

        Args:
            threshold (float, optional): The probability threshold for detecting voice activity. Defaults to 0.5.
        """
        self.model = VoiceActivityDetection()
        self.threshold = threshold
        self.frame_rate = frame_rate

    def __call__(self, audio_frame):
        """
        Determines if the given audio frame contains speech by comparing the detected speech probability against
        the threshold.

        Args:
            audio_frame (np.ndarray): The audio frame to be analyzed for voice activity. It is expected to be a
                                      NumPy array of audio samples.

        Returns:
            bool: True if the speech probability exceeds the threshold, indicating the presence of voice activity;
                  False otherwise.
        """
        speech_probs = self.model.audio_forward(torch.from_numpy(audio_frame.copy()), self.frame_rate)[0]
        return torch.any(speech_probs > self.threshold).item()