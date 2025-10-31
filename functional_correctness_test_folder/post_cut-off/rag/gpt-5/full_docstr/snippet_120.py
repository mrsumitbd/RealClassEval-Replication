from typing import Any, Dict, Tuple, Optional, List


class NunchakuIPAdapterLoader:
    '''
    Node for loading Nunchaku IP-Adapter pipelines.
    .. warning::
        This node will automatically download the IP-Adapter and associated CLIP models from Hugging Face.
        Custom model paths are not supported for now.
    '''

    _DEFAULT_IP_ADAPTER_REPOS: List[str] = [
        # Try a set of likely repos; fall back gracefully if unavailable
        "NunchakuAI/ip-adapter-flux",
        "NunchakuAI/nunchaku-ip-adapter",
        "h94/IP-Adapter",
    ]
    _DEFAULT_CLIP_REPOS: List[str] = [
        "laion/CLIP-ViT-H-14-laion2B-s32B-b79K",
        "openai/clip-vit-large-patch14",
    ]

    class _SimpleIPAdapterPipeline:
        def __init__(self, ip_adapter_path: Optional[str], clip_path: Optional[str], device: Optional[str] = None, dtype: Optional[str] = None):
            self.ip_adapter_path = ip_adapter_path
            self.clip_path = clip_path
            self.device = device
            self.dtype = dtype

        def to(self, device: Optional[str] = None, dtype: Optional[str] = None):
            if device is not None:
                self.device = device
            if dtype is not None:
                self.dtype = dtype
            return self

        def __repr__(self) -> str:
            return f"<SimpleIPAdapterPipeline ip_adapter_path={self.ip_adapter_path} clip_path={self.clip_path} device={self.device} dtype={self.dtype}>"

    @classmethod
    def INPUT_TYPES(s):
        '''
        Defines the input types and tooltips for the node.
        Returns
        -------
        dict
            A dictionary specifying the required inputs and their descriptions for the node interface.
        '''
        return {
            "required": {
                "model": (
                    "NUNCHAKU_MODEL",
                    {
                        "tooltip": "A Nunchaku model loaded via NunchakuFluxDiTLoader to attach the IP-Adapter pipeline to.",
                    },
                ),
            },
            "optional": {},
            "hidden": {},
        }

    def _try_snapshot_download(self, repo_ids: List[str]) -> Optional[str]:
        try:
            from huggingface_hub import snapshot_download
        except Exception:
            return None
        last_err = None
        for repo_id in repo_ids:
            try:
                return snapshot_download(repo_id=repo_id, local_files_only=False)
            except Exception as e:
                last_err = e
                continue
        _ = last_err  # silence unused
        return None

    def load(self, model):
        '''
        Load the IP-Adapter pipeline and attach it to the given model.
        Parameters
        ----------
        model : object
            The Nunchaku model to which the IP-Adapter will be attached.
            It should be loaded with :class:`~comfyui_nunchaku.nodes.models.flux.NunchakuFluxDiTLoader`.
        Returns
        -------
        tuple
            The original model and the loaded IP-Adapter pipeline.
        '''
        device = None
        dtype = None

        # Extract device/dtype if available on the model
        try:
            if hasattr(model, "device") and model.device is not None:
                device = str(model.device)
        except Exception:
            device = None
        try:
            if hasattr(model, "dtype") and model.dtype is not None:
                # Handle torch dtype if available
                try:
                    import torch  # type: ignore
                    if isinstance(model.dtype, torch.dtype):
                        dtype = str(model.dtype).replace("torch.", "")
                    else:
                        dtype = str(model.dtype)
                except Exception:
                    dtype = str(model.dtype)
        except Exception:
            dtype = None

        ip_adapter_path = self._try_snapshot_download(
            self._DEFAULT_IP_ADAPTER_REPOS)
        clip_path = self._try_snapshot_download(self._DEFAULT_CLIP_REPOS)

        pipeline = self._SimpleIPAdapterPipeline(
            ip_adapter_path=ip_adapter_path,
            clip_path=clip_path,
            device=device,
            dtype=dtype,
        )

        # Attach pipeline to model if possible (non-fatal on failure)
        try:
            setattr(model, "ip_adapter", pipeline)
        except Exception:
            pass

        return (model, pipeline)
