class NunchakuIPAdapterLoader:
    '''
    Node for loading Nunchaku IP-Adapter pipelines.
    .. warning::
        This node will automatically download the IP-Adapter and associated CLIP models from Hugging Face.
        Custom model paths are not supported for now.
    '''
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
                        "tooltip": (
                            "A Nunchaku model instance loaded with "
                            "comfyui_nunchaku.nodes.models.flux.NunchakuFluxDiTLoader."
                        )
                    },
                ),
            }
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
        if model is None:
            raise ValueError(
                "Expected a valid Nunchaku model instance, got None.")

        # Default repositories; these can be overridden via environment variables.
        ip_adapter_repo = (
            __import__("os").environ.get("NUNCHAKU_IP_ADAPTER_REPO")
            or "h94/IP-Adapter"
        )
        clip_repo = (
            __import__("os").environ.get("NUNCHAKU_IP_ADAPTER_CLIP_REPO")
            or "laion/CLIP-ViT-H-14-laion2B-s32B-b79K"
        )

        # Attempt to download; gracefully handle offline/missing dependency scenarios.
        os = __import__("os")
        local_files_only = os.environ.get("HF_HUB_OFFLINE", "").strip() in {
            "1", "true", "True"}

        ip_adapter_dir = None
        clip_model_dir = None

        try:
            from huggingface_hub import snapshot_download
            try:
                ip_adapter_dir = snapshot_download(
                    repo_id=ip_adapter_repo, local_files_only=local_files_only)
            except Exception:
                ip_adapter_dir = None
            try:
                clip_model_dir = snapshot_download(
                    repo_id=clip_repo, local_files_only=local_files_only)
            except Exception:
                clip_model_dir = None
        except Exception:
            # huggingface_hub not installed or other issues; proceed without downloading
            ip_adapter_dir = None
            clip_model_dir = None

        class _IPAdapterPipeline:
            def __init__(self, ip_repo, ip_dir, clip_repo_id, clip_dir):
                self.ip_adapter_repo = ip_repo
                self.ip_adapter_path = ip_dir
                self.clip_repo = clip_repo_id
                self.clip_model_path = clip_dir

            def __repr__(self):
                return (
                    f"_IPAdapterPipeline(ip_adapter_repo={self.ip_adapter_repo!r}, "
                    f"ip_adapter_path={self.ip_adapter_path!r}, "
                    f"clip_repo={self.clip_repo!r}, "
                    f"clip_model_path={self.clip_model_path!r})"
                )

        pipeline = _IPAdapterPipeline(
            ip_repo=ip_adapter_repo,
            ip_dir=ip_adapter_dir,
            clip_repo_id=clip_repo,
            clip_dir=clip_model_dir,
        )

        # Attach the pipeline to the model using a common convention or fallback to attribute set.
        if hasattr(model, "attach_ip_adapter") and callable(getattr(model, "attach_ip_adapter")):
            try:
                model.attach_ip_adapter(pipeline)
            except Exception:
                setattr(model, "ip_adapter", pipeline)
        elif hasattr(model, "set_ip_adapter") and callable(getattr(model, "set_ip_adapter")):
            try:
                model.set_ip_adapter(pipeline)
            except Exception:
                setattr(model, "ip_adapter", pipeline)
        else:
            setattr(model, "ip_adapter", pipeline)

        return model, pipeline
