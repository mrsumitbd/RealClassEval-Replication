from sen.tui.ui import get_app_in_loop
from sen.docker_backend import DockerBackend
import threading
from sen.tui.commands.display import DisplayListingCommand
from sen.tui.commands.base import Commander, SameThreadPriority
from sen.tui.constants import PALETTE
from sen.exceptions import NotifyError

class Application:

    def __init__(self, yolo=False):
        self.d = DockerBackend()
        self.loop, self.ui = get_app_in_loop(PALETTE)
        self.ui.yolo = yolo
        self.ui.commander = Commander(self.ui, self.d)
        self.rt_thread = threading.Thread(target=self.realtime_updates, daemon=True)
        self.rt_thread.start()

    def run(self):
        self.ui.run_command(DisplayListingCommand.name, queue=SameThreadPriority())
        self.loop.run()

    def realtime_updates(self):
        """
        fetch realtime events from docker and pass them to buffers

        :return: None
        """
        logger.info('starting receiving events from docker')
        it = self.d.realtime_updates()
        while True:
            try:
                event = next(it)
            except NotifyError as ex:
                self.ui.notify_message('error when receiving realtime events from docker: %s' % ex, level='error')
                return
            logger.debug('pass event to current buffer %s', self.ui.current_buffer)
            try:
                self.ui.current_buffer.process_realtime_event(event)
            except Exception as ex:
                logger.error('error while processing runtime event: %r', ex)