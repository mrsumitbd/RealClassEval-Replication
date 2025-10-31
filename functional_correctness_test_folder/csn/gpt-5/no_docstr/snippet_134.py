class Serial2ModbusClient:

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        self.ser = serial_w
        self.cli = mbus_cli
        self.def_unit = slave_addr
        self.allow_bcast = allow_bcast
        self._alive = True

    def _write_json(self, obj):
        try:
            import json
            data = (json.dumps(obj, separators=(
                ",", ":")) + "\n").encode("utf-8")
        except Exception:
            # Fallback minimal encoding
            data = (str(obj) + "\n").encode("utf-8", "ignore")
        try:
            self.ser.write(data)
        except Exception:
            pass

    def _read_line(self):
        # Support file-like .readline or fallback to reading bytes until newline
        try:
            line = self.ser.readline()
            if isinstance(line, bytes):
                return line.decode("utf-8", "ignore")
            return line
        except AttributeError:
            # Fallback manual read
            buf = bytearray()
            while True:
                ch = self.ser.read(1)
                if not ch:
                    # Non-blocking or EOF
                    if buf:
                        break
                    return ""
                if isinstance(ch, str):
                    ch = ch.encode("utf-8", "ignore")
                if ch == b"\n":
                    break
                buf.extend(ch)
            return buf.decode("utf-8", "ignore")
        except Exception:
            return ""

    def _parse_tokens(self, line):
        # Split respecting commas for value lists
        parts = line.strip().split()
        return parts

    def _as_bool(self, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(int(v))
        s = str(v).strip().lower()
        if s in ("1", "true", "t", "on", "yes", "y"):
            return True
        if s in ("0", "false", "f", "off", "no", "n"):
            return False
        return bool(int(s))

    def _parse_values_list(self, token):
        # Accept comma-separated values
        vals = []
        for t in str(token).split(","):
            t = t.strip()
            if t == "":
                continue
            if t.lower() in ("true", "false", "t", "f", "on", "off", "1", "0", "yes", "no", "y", "n"):
                vals.append(self._as_bool(t))
            else:
                vals.append(int(t, 0))
        return vals

    def _resp_ok(self, data=None):
        return {"ok": True, "data": data}

    def _resp_err(self, msg):
        return {"ok": False, "error": str(msg)}

    def _unwrap_pymodbus(self, resp):
        # Handle pymodbus style responses
        try:
            if hasattr(resp, "isError") and resp.isError():
                return None, str(resp)
            if hasattr(resp, "bits"):
                return list(resp.bits), None
            if hasattr(resp, "registers"):
                return list(resp.registers), None
            # Write responses might have .value or no payload
            if hasattr(resp, "value"):
                return resp.value, None
            return None, None
        except Exception as e:
            return None, str(e)

    def _do_read(self, cmd, unit, addr, qty):
        try:
            if cmd in ("read_coils", "rc"):
                resp = self.cli.read_coils(addr, qty, unit=unit)
            elif cmd in ("read_discrete_inputs", "rdi"):
                resp = self.cli.read_discrete_inputs(addr, qty, unit=unit)
            elif cmd in ("read_holding_registers", "rhr"):
                resp = self.cli.read_holding_registers(addr, qty, unit=unit)
            elif cmd in ("read_input_registers", "rir"):
                resp = self.cli.read_input_registers(addr, qty, unit=unit)
            else:
                return self._resp_err("unsupported read")
        except Exception as e:
            return self._resp_err(e)
        data, err = self._unwrap_pymodbus(resp)
        if err:
            return self._resp_err(err)
        return self._resp_ok(data)

    def _do_write(self, cmd, unit, addr, vals):
        # Deny broadcast unless allowed, and only for writes
        if unit in (0, "0"):
            if not self.allow_bcast:
                return self._resp_err("broadcast not allowed")
            unit = 0
        try:
            if cmd in ("write_single_coil", "wsc"):
                v = self._as_bool(vals[0])
                resp = self.cli.write_coil(addr, v, unit=unit)
            elif cmd in ("write_single_register", "wsr"):
                v = int(vals[0])
                resp = self.cli.write_register(addr, v, unit=unit)
            elif cmd in ("write_multiple_coils", "wmc"):
                bools = [self._as_bool(v) for v in vals]
                resp = self.cli.write_coils(addr, bools, unit=unit)
            elif cmd in ("write_multiple_registers", "wmr"):
                regs = [int(v) for v in vals]
                resp = self.cli.write_registers(addr, regs, unit=unit)
            else:
                return self._resp_err("unsupported write")
        except Exception as e:
            return self._resp_err(e)
        data, err = self._unwrap_pymodbus(resp)
        if err:
            return self._resp_err(err)
        return self._resp_ok(data)

    def _handle_request(self):
        line = self._read_line()
        if not line:
            return None
        line = line.strip()
        if not line:
            return None
        # Commands:
        # READS: rc|rdi|rhr|rir [unit] address qty
        # WRITES:
        #  wsc|wsr [unit] address value
        #  wmc|wmr [unit] address v1,v2,...
        # Special: unit 'bcast' or 0 to broadcast (writes only, if allowed)
        # Special: quit / stop
        tokens = self._parse_tokens(line)
        if not tokens:
            return None
        cmd = tokens[0].lower()
        if cmd in ("quit", "exit", "stop"):
            self._alive = False
            return self._resp_ok("stopping")
        # Determine if next token is unit
        idx = 1
        unit = self.def_unit
        if len(tokens) > 3:
            # Likely unit provided
            try:
                unit = int(
                    tokens[idx], 0) if tokens[idx].lower() != "bcast" else 0
                idx += 1
            except Exception:
                pass
        # Address
        if len(tokens) <= idx:
            return self._resp_err("missing address")
        try:
            addr = int(tokens[idx], 0)
        except Exception as e:
            return self._resp_err(f"bad address: {e}")
        idx += 1
        # Handle reads
        if cmd in ("read_coils", "rc", "read_discrete_inputs", "rdi", "read_holding_registers", "rhr", "read_input_registers", "rir"):
            if len(tokens) <= idx:
                return self._resp_err("missing quantity")
            try:
                qty = int(tokens[idx], 0)
            except Exception as e:
                return self._resp_err(f"bad quantity: {e}")
            # Disallow broadcast for reads
            if unit == 0:
                return self._resp_err("broadcast reads not allowed")
            return self._do_read(cmd, unit, addr, qty)
        # Handle writes
        if cmd in ("write_single_coil", "wsc", "write_single_register", "wsr"):
            if len(tokens) <= idx:
                return self._resp_err("missing value")
            vals = [tokens[idx]]
            return self._do_write(cmd, unit, addr, vals)
        if cmd in ("write_multiple_coils", "wmc", "write_multiple_registers", "wmr"):
            if len(tokens) <= idx:
                return self._resp_err("missing values")
            vals = self._parse_values_list(tokens[idx])
            if not vals:
                return self._resp_err("no values")
            return self._do_write(cmd, unit, addr, vals)
        return self._resp_err("unknown command")

    def run(self):
        self._alive = True
        while self._alive:
            resp = self._handle_request()
            if resp is None:
                continue
            self._write_json(resp)
