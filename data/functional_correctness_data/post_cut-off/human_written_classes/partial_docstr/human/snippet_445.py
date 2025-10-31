from unilabos.utils.log import info, debug, warning, error, critical, logger

class ROSLoggerAdapter:
    """同时向自定义日志和ROS2日志发送消息的适配器"""

    @property
    def identifier(self):
        return f'{self.namespace}'

    def __init__(self, ros_logger, namespace):
        """
        初始化日志适配器

        Args:
            ros_logger: ROS2日志记录器
            namespace: 命名空间
        """
        self.ros_logger = ros_logger
        self.namespace = namespace
        self.level_2_logger_func = {'info': info, 'debug': debug, 'warning': warning, 'error': error, 'critical': critical}

    def _log(self, level, msg, *args, **kwargs):
        """实际执行日志记录的内部方法"""
        msg = f'[{self.identifier}] {msg}'
        ros_log_func = getattr(self.ros_logger, 'debug')
        ros_log_func(msg)
        self.level_2_logger_func[level](msg, *args, stack_level=1, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """记录DEBUG级别日志"""
        self._log('debug', msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """记录INFO级别日志"""
        self._log('info', msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """记录WARNING级别日志"""
        self._log('warning', msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """记录ERROR级别日志"""
        self._log('error', msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """记录CRITICAL级别日志"""
        self._log('critical', msg, *args, **kwargs)