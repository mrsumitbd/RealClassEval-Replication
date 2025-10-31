import time

class retry:

    def __call__(self, func):

        def replacement(*args, **kwargs):
            max_count = MAX_RETRY_COUNT
            count = 0
            while True:
                count += 1
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if count >= max_count:
                        raise
                    else:
                        time.sleep(RETRY_SLEEP_TIME)
                        continue
        return replacement