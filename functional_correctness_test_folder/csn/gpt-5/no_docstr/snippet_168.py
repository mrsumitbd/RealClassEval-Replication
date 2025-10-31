class Gateway:

    def __init__(self, req):
        self.req = req

    def respond(self):
        try:
            req = self.req
            if callable(req):
                data = req()
            elif isinstance(req, dict):
                action = req.get('action')
                if action == 'ping':
                    data = 'pong'
                elif action == 'echo':
                    data = req.get('data')
                elif action == 'sum':
                    payload = req.get('data', [])
                    data = sum(payload) if hasattr(
                        payload, '__iter__') else payload
                else:
                    data = req
            elif isinstance(req, (list, tuple)) and all(isinstance(x, (int, float)) for x in req):
                data = sum(req)
            else:
                data = req
            return {'status': 'ok', 'data': data, 'error': None}
        except Exception as e:
            return {'status': 'error', 'data': None, 'error': str(e)}
