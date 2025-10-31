from pyModbusTCP.constants import EXP_GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND
import struct

class Serial2ModbusClient:
    """ Customize a slave serial worker for map a modbus TCP client. """

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        """Serial2ModbusClient constructor.

        :param serial_w: a SlaveSerialWorker instance
        :type serial_w: SlaveSerialWorker
        :param mbus_cli: a ModbusClient instance
        :type mbus_cli: ModbusClient
        :param slave_addr: modbus slave address
        :type slave_addr: int
        :param allow_bcast: allow processing broadcast frames (slave @0)
        :type allow_bcast: bool
        """
        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = slave_addr
        self.allow_bcast = allow_bcast
        self.serial_w.handle_request = self._handle_request

    def _handle_request(self):
        """Request handler for SlaveSerialWorker"""
        if self.serial_w.request.slave_addr == 0 and self.allow_bcast:
            self.mbus_cli.custom_request(self.serial_w.request.pdu)
        elif self.serial_w.request.slave_addr == self.slave_addr:
            resp_pdu = self.mbus_cli.custom_request(self.serial_w.request.pdu)
            if resp_pdu:
                self.serial_w.response.build(raw_pdu=resp_pdu, slave_addr=self.serial_w.request.slave_addr)
            else:
                exp_pdu = struct.pack('BB', self.serial_w.request.function_code + 128, EXP_GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND)
                self.serial_w.response.build(raw_pdu=exp_pdu, slave_addr=self.serial_w.request.slave_addr)

    def run(self):
        """Start serial processing."""
        self.serial_w.run()