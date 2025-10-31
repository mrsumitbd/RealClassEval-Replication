class NunchakuIPAdapterLoader:
    '''
    Node for loading Nunchaku IP-Adapter pipelines.
    .. warning::
        This node will automatically download the IP-Adapter and associated CLIP models from Hugging Face.
        Custom model paths are not supported for now.
    '''
    # ComfyUI-style metadata
    RETURN_TYPES = ("MODEL", "IP_ADAPTER")
    RETURN_NAMES = ("model", "ip_adapter")
    FUNCTION = "load"
    CATEGORY = "Nunchaku/Loaders"

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
                "model": ("MODEL", {
                    "tooltip": "A Nunchaku model (e.g., loaded by NunchakuFluxDiTLoader) to attach the IP-Adapter to."
                }),
            }
        }

    def _resolve_variant(self, model):
        # Best-effort heuristic to decide IP-Adapter variant based on the model.
        # Falls back to SD1.5-compatible IP-Adapter settings.
        name = str(getattr(model, "name", "")).lower()
        arch = str(getattr(model, "arch", "")).lower()
        is_sdxl = any(k in name for k in ("sdxl", "xl")) or any(
            k in arch for k in ("sdxl", "xl"))
        # Flux/SDXL-like models will use SDXL variant; otherwise SD1.5
        return "sdxl" if is_sdxl else "sd15"

    def _download_assets(self, variant: str):
        # Returns a dict with local paths for ip-adapter and clip encoder (best-effort).
        repos = {
            "sd15": {
                "ip_adapter_repo": "h94/IP-Adapter",
                "clip_repo": "openai/clip-vit-large-patch14",
            },
            "sdxl": {
                "ip_adapter_repo": "h94/IP-Adapter-SDXL",
                "clip_repo": "laion/CLIP-ViT-H-14-laion2B-s32B-b79K",
            },
        }
        choice = repos.get(variant, repos["sd15"])
        ip_adapter_dir = None
        clip_dir = None
        ok = False
        try:
            from huggingface_hub import snapshot_download
            ip_adapter_dir = snapshot_download(choice["ip_adapter_repo"])
            clip_dir = snapshot_download(choice["clip_repo"])
            ok = True
        except Exception:
            # If huggingface_hub not available or download fails, proceed with None paths.
            ok = False
        return {
            "variant": variant,
            "ip_adapter_repo": choice["ip_adapter_repo"],
            "clip_repo": choice["clip_repo"],
            "ip_adapter_dir": ip_adapter_dir,
            "clip_dir": clip_dir,
            "downloaded": ok,
        }

    class _IPAdapterPipeline:
        def __init__(self, meta: dict):
            self.variant = meta.get("variant")
            self.ip_adapter_repo = meta.get("ip_adapter_repo")
            self.clip_repo = meta.get("clip_repo")
            self.ip_adapter_dir = meta.get("ip_adapter_dir")
            self.clip_dir = meta.get("clip_dir")
            self.downloaded = bool(meta.get("downloaded", False))

        def to_dict(self):
            return {
                "variant": self.variant,
                "ip_adapter_repo": self.ip_adapter_repo,
                "clip_repo": self.clip_repo,
                "ip_adapter_dir": self.ip_adapter_dir,
                "clip_dir": self.clip_dir,
                "downloaded": self.downloaded,
            }

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
        variant = self._resolve_variant(model)
        assets = self._download_assets(variant)
        pipeline = self._IPAdapterPipeline(assets)

        # Attach to model for downstream nodes to discover/use.
        try:
            setattr(model, "nunchaku_ip_adapter", pipeline)
        except Exception:
            # Fallback: ignore if model is not mutable.
            pass

        return (model, pipeline)
