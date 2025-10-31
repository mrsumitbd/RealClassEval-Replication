
class S2Image:

    def extend(self, source, new_image_name, s2i_args=None):
        if not isinstance(source, str) or not isinstance(new_image_name, str):
            raise ValueError("source and new_image_name must be strings")
        if s2i_args is not None and not isinstance(s2i_args, dict):
            raise ValueError("s2i_args must be a dictionary or None")
        # Simulate extending the image
        self.last_extended = {
            'source': source,
            'new_image_name': new_image_name,
            's2i_args': s2i_args if s2i_args is not None else {}
        }
        return f"Image '{source}' extended to '{new_image_name}' with args {self.last_extended['s2i_args']}"

    def usage(self):
        return (
            "S2Image usage:\n"
            "  extend(source, new_image_name, s2i_args=None):\n"
            "    - source: str, the base image name\n"
            "    - new_image_name: str, the new image name\n"
            "    - s2i_args: dict (optional), additional arguments\n"
            "  Example:\n"
            "    s2i = S2Image()\n"
            "    s2i.extend('python:3.8', 'myapp:latest', {'env': 'prod'})"
        )
