from module.logger import logger

class RemoteAccess:

    @staticmethod
    def keep_ssh_alive():
        task_handler: TaskHandler
        task_handler = (yield)
        while True:
            if _ssh_thread is not None and _ssh_thread.is_alive():
                yield
                continue
            logger.info('Remote access service is not running, starting now')
            try:
                start_remote_access_service()
            except ParseError as e:
                logger.exception(e)
                task_handler.remove_current_task()
            yield

    @staticmethod
    def kill_ssh_process():
        if RemoteAccess.is_alive():
            _ssh_process.kill()

    @staticmethod
    def is_alive():
        return _ssh_thread is not None and _ssh_thread.is_alive() and (_ssh_process is not None) and (_ssh_process.poll() is None)

    @staticmethod
    def get_state():
        if RemoteAccess.is_alive():
            if address is not None:
                return 1
            else:
                return 2
        elif _ssh_notfound:
            return 3
        else:
            return 0

    @staticmethod
    def get_entry_point():
        return address if RemoteAccess.is_alive() else None