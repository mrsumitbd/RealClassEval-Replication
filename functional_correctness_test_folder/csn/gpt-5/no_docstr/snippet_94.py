from typing import Mapping, Any


class CmdStep:

    def __init__(self, name: str, context: "Context", is_shell: bool = False) -> None:
        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string")
        if context is None:
            raise ValueError("context must not be None")
        self.name = name
        self.context = context
        self.is_shell = bool(is_shell)

    def create_command(self, cmd_input: Mapping) -> "Command":
        if not isinstance(cmd_input, Mapping):
            raise TypeError("cmd_input must be a Mapping")
        # Prefer a direct factory on context
        if hasattr(self.context, "create_command") and callable(getattr(self.context, "create_command")):
            return self.context.create_command(cmd_input, shell=self.is_shell)
        # Try a generic factory attribute
        factory = getattr(self.context, "command_factory", None)
        if callable(factory):
            return factory(cmd_input, shell=self.is_shell)
        # Try a Command class on context
        command_cls = getattr(self.context, "Command", None)
        if command_cls is not None:
            return command_cls(cmd_input, shell=self.is_shell)
        raise RuntimeError(
            "No available way to create a Command from the provided context")

    def run_step(self) -> None:
        # Retrieve input for this step from context
        if hasattr(self.context, "get_step_input") and callable(getattr(self.context, "get_step_input")):
            cmd_input = self.context.get_step_input(self.name)
        elif hasattr(self.context, "get") and callable(getattr(self.context, "get")):
            cmd_input = self.context.get(self.name)
        elif hasattr(self.context, "inputs") and isinstance(getattr(self.context, "inputs"), Mapping):
            cmd_input = self.context.inputs.get(self.name)
        else:
            raise RuntimeError("Context does not provide step input accessors")
        if cmd_input is None:
            raise ValueError(
                f"No command input found in context for step '{self.name}'")

        cmd = self.create_command(cmd_input)

        # Execute the command
        if hasattr(cmd, "run") and callable(getattr(cmd, "run")):
            result = cmd.run()
        elif hasattr(cmd, "execute") and callable(getattr(cmd, "execute")):
            result = cmd.execute()
        else:
            raise RuntimeError(
                "Command object does not provide a run/execute method")

        # Store result back into context (best-effort)
        if hasattr(self.context, "set_step_result") and callable(getattr(self.context, "set_step_result")):
            self.context.set_step_result(self.name, result)
        elif hasattr(self.context, "set") and callable(getattr(self.context, "set")):
            self.context.set(f"{self.name}.result", result)
        elif hasattr(self.context, "results") and isinstance(getattr(self.context, "results"), dict):
            self.context.results[self.name] = result
        # If no suitable sink exists, silently do nothing beyond execution
