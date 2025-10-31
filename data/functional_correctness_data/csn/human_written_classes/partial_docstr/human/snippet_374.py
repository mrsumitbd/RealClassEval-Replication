import aiohttp
from gns3server.utils import macaddress_to_int, int_to_macaddress

class StandardPortFactory:
    """
    Create ports for standard device
    """

    def __new__(cls, properties, port_by_adapter, first_port_name, port_name_format, port_segment_size, custom_adapters):
        ports = []
        adapter_number = interface_number = segment_number = 0
        if 'ethernet_adapters' in properties:
            ethernet_adapters = properties['ethernet_adapters']
        else:
            ethernet_adapters = properties.get('adapters', 1)
        for adapter_number in range(adapter_number, ethernet_adapters + adapter_number):
            custom_adapter_settings = {}
            for custom_adapter in custom_adapters:
                if custom_adapter['adapter_number'] == adapter_number:
                    custom_adapter_settings = custom_adapter
                    break
            for port_number in range(0, port_by_adapter):
                if first_port_name and adapter_number == 0:
                    port_name = custom_adapter_settings.get('port_name', first_port_name)
                    port = PortFactory(port_name, segment_number, adapter_number, port_number, 'ethernet', short_name=port_name)
                else:
                    try:
                        port_name = port_name_format.format(interface_number, segment_number, adapter=adapter_number, **cls._generate_replacement(interface_number, segment_number))
                    except (IndexError, ValueError, KeyError) as e:
                        raise aiohttp.web.HTTPConflict(text='Invalid port name format {}: {}'.format(port_name_format, str(e)))
                    port_name = custom_adapter_settings.get('port_name', port_name)
                    port = PortFactory(port_name, segment_number, adapter_number, port_number, 'ethernet')
                    interface_number += 1
                    if port_segment_size:
                        if interface_number % port_segment_size == 0:
                            segment_number += 1
                            interface_number = 0
                    else:
                        segment_number += 1
                port.adapter_type = custom_adapter_settings.get('adapter_type', properties.get('adapter_type', None))
                mac_address = custom_adapter_settings.get('mac_address')
                if not mac_address and 'mac_address' in properties:
                    mac_address = int_to_macaddress(macaddress_to_int(properties['mac_address']) + adapter_number)
                port.mac_address = mac_address
                ports.append(port)
        if len(ports):
            adapter_number += 1
        if 'serial_adapters' in properties:
            for adapter_number in range(adapter_number, properties['serial_adapters'] + adapter_number):
                for port_number in range(0, port_by_adapter):
                    ports.append(PortFactory('Serial{}/{}'.format(segment_number, port_number), segment_number, adapter_number, port_number, 'serial'))
                segment_number += 1
        return ports

    @staticmethod
    def _generate_replacement(interface_number, segment_number):
        """
        This will generate replacement string for
        {port0} => {port9}
        {segment0} => {segment9}
        """
        replacements = {}
        for i in range(0, 9):
            replacements['port' + str(i)] = interface_number + i
            replacements['segment' + str(i)] = segment_number + i
        return replacements