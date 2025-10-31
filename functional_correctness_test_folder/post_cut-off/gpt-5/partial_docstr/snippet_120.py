class NunchakuIPAdapterLoader:

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
            },
            "optional": {
            },
            "tooltips": {
                "": "Automatically loads or retrieves an IP-Adapter pipeline from the provided Nunchaku model."
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
            raise ValueError("model must not be None")

        # If already present, return it.
        for attr_name in ("ip_adapter", "ip_adapter_pipeline", "ip_adapter_pipe"):
            if hasattr(model, attr_name):
                adapter = getattr(model, attr_name)
                if adapter is not None:
                    return model, adapter

        # Try to obtain/build via known method names.
        import inspect

        candidate_methods = [
            "get_ip_adapter",
            "ip_adapter",
            "load_ip_adapter",
            "attach_ip_adapter",
            "build_ip_adapter",
            "create_ip_adapter",
            "ensure_ip_adapter",
            "init_ip_adapter",
        ]

        adapter = None
        for name in candidate_methods:
            if not hasattr(model, name):
                continue
            meth = getattr(model, name)
            if not callable(meth):
                continue
            try:
                sig = None
                try:
                    sig = inspect.signature(meth)
                except (ValueError, TypeError):
                    sig = None

                # Determine how to call based on signature arity (excluding self)
                if sig is None:
                    # Fallback: try no-arg first, then with model
                    try:
                        adapter = meth()
                    except TypeError:
                        adapter = meth(model)
                else:
                    params = [
                        p for p in sig.parameters.values()
                        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
                    ]
                    # Exclude 'self' if present
                    if params and params[0].name == "self":
                        params = params[1:]

                    if len(params) == 0:
                        adapter = meth()
                    elif len(params) == 1:
                        adapter = meth(model)
                    else:
                        # Try calling with no args first, then with model
                        try:
                            adapter = meth()
                        except TypeError:
                            adapter = meth(model)
                if adapter is not None:
                    break
            except Exception:
                continue

        # If still not found, try lazy attribute access patterns that compute on first get
        if adapter is None:
            for attr_name in ("ip_adapter", "ip_adapter_pipeline", "ip_adapter_pipe"):
                try:
                    if hasattr(model, attr_name):
                        adapter = getattr(model, attr_name)
                        if adapter is not None:
                            break
                except Exception:
                    continue

        if adapter is None:
            raise RuntimeError(
                "Unable to load or retrieve IP-Adapter from the provided model.")

        # Cache under a common attribute for future calls
        try:
            if not hasattr(model, "ip_adapter") or getattr(model, "ip_adapter", None) is None:
                setattr(model, "ip_adapter", adapter)
        except Exception:
            pass

        return model, adapter
