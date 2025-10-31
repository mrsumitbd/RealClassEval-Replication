import subprocess

class CLIDockerClient:
    """Wrapper around Docker CLI to manage Docker containers, images, and projects.

    Initializes a new instance of the current Docker state from the
    perspective of Tesseracts, while mimicking the interface of Docker-Py, with additional
    features for the convenience of Tesseract usage.

    Most calls to CLIDockerClient could be replaced by official Docker-Py Client. However,
    CLIDockerClient by default only sees Tesseract relevant images, containers, and projects;
    the flag `tesseract_only` must be set to False to see non-Tesseract images, containers, and projects.
    """

    def __init__(self) -> None:
        self.containers = Containers()
        self.images = Images()
        self.volumes = Volumes()

    @staticmethod
    def info() -> tuple:
        """Wrapper around docker info call."""
        docker = _get_docker_executable()
        try:
            result = subprocess.run([*docker, 'info'], check=True, capture_output=True)
            return (result.stdout, result.stderr)
        except subprocess.CalledProcessError as ex:
            raise APIError() from ex