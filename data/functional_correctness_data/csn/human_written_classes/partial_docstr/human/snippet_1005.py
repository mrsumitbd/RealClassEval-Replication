from dragonpy.Dragon32.MC6821_PIA import PIA
from dragonpy.Dragon32.MC6883_SAM import SAM

class Dragon32PeripheryBase:
    """
    GUI independent stuff
    """

    def __init__(self, cfg, cpu, memory, user_input_queue):
        self.cfg = cfg
        self.cpu = cpu
        self.memory = memory
        self.user_input_queue = user_input_queue
        self.kbd = 191
        self.display = None
        self.speaker = None
        self.cassette = None
        self.sam = SAM(cfg, cpu, memory)
        self.pia = PIA(cfg, cpu, memory, self.user_input_queue)
        self.memory.add_read_byte_callback(self.no_dos_rom, 49152)
        self.memory.add_read_word_callback(self.no_dos_rom, 49152)
        self.running = True

    def reset(self):
        self.sam.reset()
        self.pia.reset()
        self.pia.internal_reset()

    def no_dos_rom(self, cpu_cycles, op_address, address):
        log.error('%04x| TODO: DOS ROM requested. Send 0x00 back', op_address)
        return 0