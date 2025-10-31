import datetime
import os

class Retention:

    @staticmethod
    def retention_count(logs, number):

        def key_log(log):
            return (-os.stat(log).st_mtime, log)
        for log in sorted(logs, key=key_log)[number:]:
            os.remove(log)

    @staticmethod
    def retention_age(logs, seconds):
        t = datetime.datetime.now().timestamp()
        for log in logs:
            if os.stat(log).st_mtime <= t - seconds:
                os.remove(log)