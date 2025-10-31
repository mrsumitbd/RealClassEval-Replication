from pyModbusTCP.constants import EXP_GATEWAY_PATH_UNAVAILABLE, EXP_GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND
import queue
from queue import Queue

class ModbusSerialWorker:
    """ A serial worker to manage I/O with RTU devices. """

    def __init__(self, port, timeout=1.0, end_of_frame=0.05):
        self.serial_port = port
        self.timeout = timeout
        self.end_of_frame = end_of_frame
        self.rtu_queries_q = Queue(maxsize=5)

    def loop(self):
        """Serial worker main loop."""
        while True:
            rtu_query = self.rtu_queries_q.get()
            self.serial_port.reset_input_buffer()
            self.serial_port.write(rtu_query.request.raw)
            self.serial_port.timeout = self.timeout
            rx_raw = self.serial_port.read(1)
            if rx_raw:
                self.serial_port.timeout = self.end_of_frame
                while True:
                    rx_chunk = self.serial_port.read(256)
                    if not rx_chunk:
                        break
                    else:
                        rx_raw += rx_chunk
            rtu_query.response.raw = rx_raw
            rtu_query.completed.set()
            self.rtu_queries_q.task_done()

    def srv_engine_entry(self, session_data):
        """Server engine entry point (pass request to serial worker queries queue).

        :param session_data: server session data
        :type session_data: ModbusServer.SessionData
        """
        rtu_query = RtuQuery()
        rtu_query.request.build(raw_pdu=session_data.request.pdu.raw, slave_ad=session_data.request.mbap.unit_id)
        try:
            self.rtu_queries_q.put(rtu_query, block=False)
            rtu_query.completed.wait()
            if rtu_query.response.is_valid:
                session_data.response.pdu.raw = rtu_query.response.pdu
                return
            exp_status = EXP_GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND
        except queue.Full:
            exp_status = EXP_GATEWAY_PATH_UNAVAILABLE
        func_code = rtu_query.request.function_code
        session_data.response.pdu.build_except(func_code=func_code, exp_status=exp_status)