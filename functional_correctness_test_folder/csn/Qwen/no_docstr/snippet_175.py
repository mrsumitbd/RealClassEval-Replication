
class S2Image:

    def extend(self, source, new_image_name, s2i_args=None):
        if s2i_args is None:
            s2i_args = {}
        # Assuming s2i is a command-line tool and we are simulating its usage
        command = f"s2i build {source} {self.base_image} {new_image_name}"
        if s2i_args:
            command += " " + \
                " ".join([f"--{k}={v}" for k, v in s2i_args.items()])
        print(f"Executing: {command}")
        # Here you would typically execute the command using subprocess or similar
        # For this example, we'll just print the command

    def usage(self):
        usage_text = """
Usage: s2i build <source> <base_image> <new_image_name> [options]

Options:
  -e, --environment <file>     Specify environment file
  -c, --context-dir <dir>      Specify context directory inside source
  -i, --incremental            Perform an incremental build
"""
        print(usage_text)

    def __init__(self, base_image):
        self.base_image = base_image
