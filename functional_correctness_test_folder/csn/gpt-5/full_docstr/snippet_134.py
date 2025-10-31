class Serial2ModbusClient:
    ''' Customize a slave serial worker for map a modbus TCP client. '''

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        '''Serial2ModbusClient constructor.
        :param serial_w: a SlaveSerialWorker instance
        :type serial_w: SlaveSerialWorker
        :param mbus_cli: a ModbusClient instance
        :type mbus_cli: ModbusClient
        :param slave_addr: modbus slave address
        :type slave_addr: int
        :param allow_bcast: allow processing broadcast frames (slave @0)
        :type allow_bcast: bool
        '''
        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = int(slave_addr)
        self.allow_bcast = bool(allow_bcast)

        # Try to propagate broadcast policy to worker if it supports it
        try:
            setattr(self.serial_w, "allow_bcast", self.allow_bcast)
        except Exception:
            pass

        # Register our handler if the worker exposes a hook
        if hasattr(self.serial_w, "set_request_handler") and callable(getattr(self.serial_w, "set_request_handler")):
            self.serial_w.set_request_handler(self._handle_request)
        elif hasattr(self.serial_w, "req_handler"):
            try:
                setattr(self.serial_w, "req_handler", self._handle_request)
            except Exception:
                pass

    def _get_pending_request(self):
        # Try several ways to fetch an incoming request from the worker
        # Expected to return tuple (unit_id, request_pdu) or (None, None) if nothing.
        w = self.serial_w
        # Method returning tuple
        for name in ("get_request", "pop_request", "read_request", "recv_request"):
            meth = getattr(w, name, None)
            if callable(meth):
                try:
                    req = meth()
                    if isinstance(req, tuple) and len(req) == 2:
                        return req[0], req[1]
                except Exception:
                    pass
        # Attributes carrying last request
        unit = getattr(w, "request_slave", None)
        pdu = getattr(w, "request_pdu", None)
        if unit is not None and pdu is not None:
            return unit, pdu
        return None, None

    def _send_response(self, unit_id, response_pdu):
        # Try several ways to send a response back to the worker
        w = self.serial_w
        for name in ("send_response", "put_response", "write_response", "set_response"):
            meth = getattr(w, name, None)
            if callable(meth):
                try:
                    # Prefer (unit_id, pdu) signature; fallback to (pdu,)
                    try:
                        return meth(unit_id, response_pdu)
                    except TypeError:
                        return meth(response_pdu)
                except Exception:
                    pass
        # As a last resort, try setting attributes the worker might read
        try:
            setattr(w, "response_slave", unit_id)
            setattr(w, "response_pdu", response_pdu)
        except Exception:
            pass

    def _ensure_client_open(self):
        cli = self.mbus_cli
        try:
            is_open = getattr(cli, "is_open", None)
            if callable(is_open):
                if not is_open():
                    open_m = getattr(cli, "open", None)
                    if callable(open_m):
                        open_m()
            else:
                # Some clients expose .open() without .is_open()
                open_m = getattr(cli, "open", None)
                if callable(open_m):
                    try:
                        open_m()
                    except Exception:
                        pass
        except Exception:
            pass

    def _proxy_custom_request(self, request_pdu, unit_id):
        cli = self.mbus_cli
        # Prefer custom_request if available
        custom = getattr(cli, "custom_request", None)
        if callable(custom):
            # pyModbusTCP custom_request(request_pdu, unit_id=1)
            try:
                return custom(request_pdu, unit_id=unit_id)
            except TypeError:
                # Some variants use slave/unit as positional second arg
                return custom(request_pdu, unit_id)
        # No raw PDU path available
        return None

    def _handle_request(self):
        '''Request handler for SlaveSerialWorker'''
        unit_id, req_pdu = self._get_pending_request()
        if req_pdu is None:
            return

        # Drop broadcasts if not allowed
        if unit_id == 0 and not self.allow_bcast:
            return

        # Ensure TCP client is connected if it supports it
        self._ensure_client_open()

        resp_pdu = None
        try:
            resp_pdu = self._proxy_custom_request(
                req_pdu, unit_id if unit_id else self.slave_addr)
        except Exception:
            resp_pdu = None

        # Do not respond to broadcast requests
        if unit_id == 0:
            return

        if resp_pdu is not None:
            self._send_response(unit_id, resp_pdu)

    def run(self):
        '''Start serial processing.'''
        # Prefer worker-managed loop if provided
        w = self.serial_w

        # If worker accepts our handler, call a run/looping method
        for name in ("run", "start", "serve_forever", "process_forever", "loop"):
            meth = getattr(w, name, None)
            if callable(meth):
                return meth()

        # Fallback: simple polling loop if worker provides a process/step method
        step = None
        for name in ("process", "step", "poll"):
            meth = getattr(w, name, None)
            if callable(meth):
                step = meth
                break

        if step is None:
            # Last resort: manually poll for requests and handle them
            import time
            while True:
                try:
                    self._handle_request()
                except Exception:
                    pass
                time.sleep(0.01)
        else:
            import time
            while True:
                try:
                    step()
                    self._handle_request()
                except Exception:
                    pass
                time.sleep(0.001)
