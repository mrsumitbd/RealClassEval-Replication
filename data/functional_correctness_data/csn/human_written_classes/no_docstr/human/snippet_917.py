from typing import List

class Product:

    def __init__(self, id: int, name: str, buttons: bool, chain: bool, color: bool, extended_multizone: bool, hev: bool, infrared: bool, matrix: bool, multizone: bool, relays: bool, max_kelvin: int, min_kelvin: int, min_ext_mz_firmware: int, min_ext_mz_firmware_components: List[int], temperature_range: None):
        self.id = id
        self.name = name
        self.buttons = buttons
        self.chain = chain
        self.color = color
        self.extended_multizone = extended_multizone
        self.hev = hev
        self.infrared = infrared
        self.matrix = matrix
        self.multizone = multizone
        self.relays = relays
        self.max_kelvin = max_kelvin
        self.min_kelvin = min_kelvin
        self.min_ext_mz_firmware = min_ext_mz_firmware
        self.min_ext_mz_firmware_components = min_ext_mz_firmware_components
        self.temperature_range = temperature_range

    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', buttons={self.buttons}, chain={self.chain}, color={self.color}, extended_multizone={self.extended_multizone}, hev={self.hev}, infrared={self.infrared}, matrix={self.matrix}, multizone={self.multizone}, relays={self.relays}, max_kelvin={self.max_kelvin}, min_kelvin={self.min_kelvin}, min_ext_mz_firmware={self.min_ext_mz_firmware}, min_ext_mz_firmware_components={self.min_ext_mz_firmware_components}, temperature_range={self.temperature_range})"