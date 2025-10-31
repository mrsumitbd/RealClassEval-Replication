class NunchakuIPAdapterLoader:
    '''
    Node for loading Nunchaku IP-Adapter pipelines.
    .. warning::
        This node will automatically download the IP-Adapter and associated CLIP models from Hugging Face.
        Custom model paths are not supported for now.
    '''
    RETURN_TYPES = ("NUNCHAKU_MODEL", "IPADAPTER_PIPELINE")
    RETURN_NAMES = ("model", "ip_adapter")
    FUNCTION = "load"
    CATEGORY = "Nunchaku/Loaders"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("NUNCHAKU_MODEL", {
                    "tooltip": "The Nunchaku model (loaded by NunchakuFluxDiTLoader) to attach the IP-Adapter to."
                }),
            }
        }

    def _download_from_hf(self, repo_id, allow_patterns=None):
        try:
            from huggingface_hub import snapshot_download
        except Exception as e:
            raise RuntimeError(
                "huggingface_hub is required to download IP-Adapter assets. "
                "Install it with: pip install huggingface_hub"
            ) from e

        kwargs = {
            "repo_id": repo_id,
            "revision": None,
            "local_files_only": False,
            "allow_patterns": allow_patterns,
        }
        return snapshot_download(**kwargs)

    def load(self, model):
        if model is None:
            raise ValueError(
                "Expected a valid Nunchaku model instance, got None.")

        ip_repo = "h94/IP-Adapter"
        clip_repo = "laion/CLIP-ViT-H-14-laion2B-s32B-b79K"

        ip_adapter_dir = self._download_from_hf(
            ip_repo,
            allow_patterns=[
                "models/*",
                "sd15/*",
                "image_encoder/*",
                "ip-adapter*",
                "*.json",
                "*.bin",
                "*.safetensors",
                "*.pth",
            ],
        )
        clip_dir = self._download_from_hf(
            clip_repo,
            allow_patterns=[
                "*",
            ],
        )

        ip_adapter_info = {
            "ip_adapter_repo": ip_repo,
            "clip_repo": clip_repo,
            "ip_adapter_dir": ip_adapter_dir,
            "clip_dir": clip_dir,
        }

        # Try to attach to model if it exposes an attachment API
        try:
            if hasattr(model, "attach_ip_adapter") and callable(getattr(model, "attach_ip_adapter")):
                model.attach_ip_adapter(
                    ip_adapter_dir=ip_adapter_dir, clip_dir=clip_dir)
            elif hasattr(model, "set_ip_adapter") and callable(getattr(model, "set_ip_adapter")):
                model.set_ip_adapter(ip_adapter_dir, clip_dir)
            else:
                # Fallback: store paths on the model for downstream nodes
                setattr(model, "ip_adapter_dir", ip_adapter_dir)
                setattr(model, "ip_adapter_clip_dir", clip_dir)
        except Exception as e:
            raise RuntimeError(
                f"Failed to attach IP-Adapter to the provided model: {e}") from e

        return (model, ip_adapter_info)
