from sglang.srt.entrypoints.http_server import launch_server
from sglang.srt.utils import kill_process_tree
import os
from sglang.srt.server_args import prepare_server_args, ServerArgs

class SGLangServer:

    def __init__(self, server_args: ServerArgs):
        self.server_args = server_args

    def run_server(self) -> None:
        try:
            launch_server(self.server_args)
        finally:
            kill_process_tree(os.getpid(), include_parent=False)