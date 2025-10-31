import queue
from dragonpy.utils.simple_debugger import print_exc_plus

class MachineGUI:

    def __init__(self, cfg):
        self.cfg = cfg
        self.user_input_queue = queue.Queue()

    def run(self, PeripheryClass, GUI_Class):
        log.log(99, "Startup '%s' machine...", self.cfg.MACHINE_NAME)
        log.critical('init GUI')
        gui = GUI_Class(self.cfg, self.user_input_queue)
        log.critical('init machine')
        machine = Machine(self.cfg, PeripheryClass, gui.display_callback, self.user_input_queue)
        try:
            gui.mainloop(machine)
        except Exception as err:
            log.critical('GUI exception: %s', err)
            print_exc_plus()
        machine.quit()
        log.log(99, ' --- END ---')