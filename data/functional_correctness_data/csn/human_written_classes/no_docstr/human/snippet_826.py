class ThreadedMachine:

    def __init__(self, cfg, periphery_class, user_input_queue):
        self.cpu_thread = MachineThread(cfg, periphery_class, user_input_queue)
        self.cpu_thread.deamon = True
        self.cpu_thread.start()

    def quit(self):
        self.cpu_thread.quit()