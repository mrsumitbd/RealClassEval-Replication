
import os
import torch


class NunchakuIPAdapterLoader:
    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input types for the node.
        Returns a dictionary that can be used by the UI to build the input form.
        """
        return {
            "required": {
                "adapter_path": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": "Path to the IP adapter file (PyTorch .pt/.pth).",
                    },
                ),
            }
        }

    def load(self, model):
        """
        Loads an IP adapter from the path specified in the node's inputs.
        The loaded adapter is returned in a dictionary. The `model` argument
        is accepted for compatibility with the node interface but is not
        modified by this loader.
        """
        # Retrieve the adapter path from the instance attributes
        adapter_path = getattr(self, "adapter_path", "")

        if not adapter_path:
            raise ValueError(
                "No adapter_path provided for NunchakuIPAdapterLoader.")

        if not os.path.isfile(adapter_path):
            raise FileNotFoundError(f"Adapter file not found: {adapter_path}")

        try:
            adapter = torch.load(adapter_path, map_location="cpu")
        except Exception as e:
            raise RuntimeError(
                f"Failed to load adapter from {adapter_path}: {e}")

        return {"adapter": adapter}
