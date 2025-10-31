class Serial2ModbusClient:

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        if serial_w is None:
            raise ValueError("serial_w is required")
        if mbus_cli is None:
            raise ValueError("mbus_cli is required")
        if not isinstance(slave_addr, int) or not (0 <= slave_addr <= 247):
            raise ValueError("slave_addr must be an integer between 0 and 247")
        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = slave_addr
        self.allow_bcast = allow_bcast
        self._running = False

    def _handle_request(self, req=None):
        '''Request handler for SlaveSerialWorker'''
        if req is None:
            return None
        if not isinstance(req, (bytes, bytearray)):
            # Some workers pass (addr, pdu) tuple
            if isinstance(req, tuple) and len(req) == 2:
                addr, pdu = req
                if not isinstance(addr, int) or not isinstance(pdu, (bytes, bytearray)):
                    return None
            else:
                return None
        else:
            if len(req) < 1:
                return None
            addr = req[0]
            pdu = req[1:]

        # Address filtering
        if addr == 0:
            # Broadcast - no response should be sent back
            if not self.allow_bcast:
                return None
            # Forward to client if allowed but do not return a response
            try:
                self._forward_pdu(pdu, unit=0)
            except Exception:
                pass
            return None

        if addr != self.slave_addr:
            return None

        # Forward to Modbus client and return encapsulated ADU
        resp_pdu = self._forward_pdu(pdu, unit=addr)
        if resp_pdu is None:
            return None
        return bytes([addr]) + bytes(resp_pdu)

    def _forward_pdu(self, pdu, unit):
        # Try a variety of client interfaces to send raw PDU
        cli = self.mbus_cli

        # Preferred: execute_pdu(pdu: bytes, unit: int) -> bytes
        execute_pdu = getattr(cli, "execute_pdu", None)
        if callable(execute_pdu):
            return execute_pdu(bytes(pdu), unit=unit)

        # Fallback: execute(pdu, unit=...) -> bytes
        execute = getattr(cli, "execute", None)
        if callable(execute):
            return execute(bytes(pdu), unit=unit)

        # Fallback: transport-like object
        transport = getattr(cli, "transport", None)
        if transport is not None:
            send_pdu = getattr(transport, "send_pdu", None)
            if callable(send_pdu):
                return send_pdu(bytes(pdu), unit=unit)

        raise RuntimeError("mbus_cli does not support raw PDU execution")

    def run(self):
        self._running = True
        # Register request handler with various possible APIs
        registered = False
        try:
            if hasattr(self.serial_w, "register_request_handler"):
                self.serial_w.register_request_handler(self._handle_request)
                registered = True
            elif hasattr(self.serial_w, "set_request_handler"):
                self.serial_w.set_request_handler(self._handle_request)
                registered = True
            elif hasattr(self.serial_w, "on_request"):
                # Some APIs expose a property/callback
                try:
                    self.serial_w.on_request = self._handle_request
                    registered = True
                except Exception:
                    registered = False

            # Start/Run the worker
            if hasattr(self.serial_w, "serve_forever"):
                self.serial_w.serve_forever()
            elif hasattr(self.serial_w, "run"):
                self.serial_w.run()
            elif hasattr(self.serial_w, "start"):
                self.serial_w.start()
                if hasattr(self.serial_w, "join"):
                    self.serial_w.join()
            else:
                # Polling fallback API: expect recv()->request, send(response)
                # This is a minimal synchronous loop.
                while self._running:
                    if not hasattr(self.serial_w, "recv"):
                        break
                    req = self.serial_w.recv()
                    if req is None:
                        continue
                    resp = self._handle_request(req)
                    if resp is not None and hasattr(self.serial_w, "send"):
                        self.serial_w.send(resp)
        finally:
            self._running = False
            # Cleanup/close serial worker if possible
            for attr in ("close", "stop", "shutdown"):
                fn = getattr(self.serial_w, attr, None)
                if callable(fn):
                    try:
                        fn()
                    except Exception:
                        pass
