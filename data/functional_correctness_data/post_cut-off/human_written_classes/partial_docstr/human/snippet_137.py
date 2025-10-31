from typing import Dict, Optional

class InferenceEngineDetector:
    """
    Main class for detecting inference engine availability.
    """

    def __init__(self):
        self.oga_detector = OGADetector()
        self.llamacpp_detector = LlamaCppDetector()
        self.transformers_detector = TransformersDetector()

    def detect_engines_for_device(self, device_type: str, device_name: str) -> Dict[str, Dict]:
        """
        Detect all available inference engines for a specific device type.

        Args:
            device_type: "cpu", "amd_igpu", "amd_dgpu", or "npu"

        Returns:
            dict: Engine availability information
        """
        engines = {}
        oga_info = self.oga_detector.detect_for_device(device_type)
        if oga_info:
            engines['oga'] = oga_info
        llamacpp_info = self.llamacpp_detector.detect_for_device(device_type, device_name, 'vulkan')
        if llamacpp_info:
            engines['llamacpp-vulkan'] = llamacpp_info
        llamacpp_info = self.llamacpp_detector.detect_for_device(device_type, device_name, 'rocm')
        if llamacpp_info:
            engines['llamacpp-rocm'] = llamacpp_info
        transformers_info = self.transformers_detector.detect_for_device(device_type)
        if transformers_info:
            engines['transformers'] = transformers_info
        return engines