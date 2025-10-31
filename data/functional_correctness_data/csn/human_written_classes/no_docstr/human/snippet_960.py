from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
from typing import TYPE_CHECKING, Optional, Callable, List, Any, Tuple, Type

class Server:

    def __init__(self, path: str, repaint: Optional['Repaint']=None, port: int=8000) -> None:
        self.path = path
        self.port = port
        self.repaint = repaint
        self.httpd = HTTPServer(self.path, ('', self.port), repaint)

    def serve(self) -> None:
        self.httpd.serve_forever()