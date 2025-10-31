from websockets.server import WebSocketServerProtocol

class Server:
    closing = False

    def register(self, ws: WebSocketServerProtocol) -> None:
        pass

    def unregister(self, ws: WebSocketServerProtocol) -> None:
        pass

    def is_serving(self) -> bool:
        return not self.closing