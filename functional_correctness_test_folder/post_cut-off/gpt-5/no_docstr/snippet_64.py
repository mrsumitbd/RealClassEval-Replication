class BaseTool:
    def __init__(
        self,
        tool_name=None,
        tool_description=None,
        tool_version=None,
        input_types=None,
        output_type=None,
        demo_commands=None,
        output_dir=None,
        user_metadata=None,
        model_string=None,
    ):
        self.tool_name = None
        self.tool_description = None
        self.tool_version = None
        self.input_types = None
        self.output_type = None
        self.demo_commands = None
        self.user_metadata = {}
        self.output_dir = None
        self.model_string = None
        self._metadata = {}

        if any(
            v is not None
            for v in [
                tool_name,
                tool_description,
                tool_version,
                input_types,
                output_type,
                demo_commands,
                user_metadata,
            ]
        ):
            self.set_metadata(
                tool_name=tool_name,
                tool_description=tool_description,
                tool_version=tool_version,
                input_types=input_types,
                output_type=output_type,
                demo_commands=demo_commands,
                user_metadata=user_metadata,
            )

        if output_dir is not None:
            self.set_custom_output_dir(output_dir)

        if model_string is not None:
            self.set_llm_engine(model_string)

    def set_metadata(
        self,
        tool_name,
        tool_description,
        tool_version,
        input_types,
        output_type,
        demo_commands,
        user_metadata=None,
    ):
        # Basic normalization
        if input_types is None:
            input_types = []
        if demo_commands is None:
            demo_commands = []
        if user_metadata is None:
            user_metadata = {}

        # Type checks (lightweight)
        if tool_name is not None and not isinstance(tool_name, str):
            raise TypeError("tool_name must be a string or None")
        if tool_description is not None and not isinstance(tool_description, str):
            raise TypeError("tool_description must be a string or None")
        if tool_version is not None and not isinstance(tool_version, (str, int, float)):
            raise TypeError("tool_version must be str/int/float or None")
        if not isinstance(input_types, (list, tuple)):
            raise TypeError("input_types must be a list or tuple")
        if output_type is not None and not isinstance(output_type, str):
            raise TypeError("output_type must be a string or None")
        if not isinstance(demo_commands, (list, tuple)):
            raise TypeError("demo_commands must be a list or tuple")
        if not isinstance(user_metadata, dict):
            raise TypeError("user_metadata must be a dict")

        # Assign
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_version = str(
            tool_version) if tool_version is not None else None
        self.input_types = list(input_types)
        self.output_type = output_type
        self.demo_commands = list(demo_commands)
        self.user_metadata = dict(user_metadata)

        # Snapshot metadata
        self._metadata = {
            "tool_name": self.tool_name,
            "tool_description": self.tool_description,
            "tool_version": self.tool_version,
            "input_types": list(self.input_types) if self.input_types is not None else None,
            "output_type": self.output_type,
            "demo_commands": list(self.demo_commands) if self.demo_commands is not None else None,
            "user_metadata": dict(self.user_metadata) if self.user_metadata is not None else None,
            "output_dir": self.output_dir,
            "model_string": self.model_string,
        }
        return self

    def get_metadata(self):
        if not self._metadata:
            # ensure consistency if set_metadata wasn't called yet
            meta = {
                "tool_name": self.tool_name,
                "tool_description": self.tool_description,
                "tool_version": self.tool_version,
                "input_types": list(self.input_types) if self.input_types is not None else None,
                "output_type": self.output_type,
                "demo_commands": list(self.demo_commands) if self.demo_commands is not None else None,
                "user_metadata": dict(self.user_metadata) if self.user_metadata is not None else None,
                "output_dir": self.output_dir,
                "model_string": self.model_string,
            }
            return meta
        # return a shallow copy to avoid external mutation
        meta = dict(self._metadata)
        # keep latest output_dir and model_string
        meta["output_dir"] = self.output_dir
        meta["model_string"] = self.model_string
        return meta

    def set_custom_output_dir(self, output_dir):
        if output_dir is None:
            self.output_dir = None
            if self._metadata:
                self._metadata["output_dir"] = None
            return self

        if not isinstance(output_dir, str):
            raise TypeError("output_dir must be a string or None")

        import os

        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
        if self._metadata:
            self._metadata["output_dir"] = output_dir
        return self

    def set_llm_engine(self, model_string):
        if model_string is not None and not isinstance(model_string, str):
            raise TypeError("model_string must be a string or None")
        self.model_string = model_string
        if self._metadata:
            self._metadata["model_string"] = model_string
        return self

    def execute(self, *args, **kwargs):
        raise NotImplementedError(
            "execute must be implemented by subclasses of BaseTool")
