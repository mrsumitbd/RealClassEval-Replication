class SubscribeConfig:

    class Recency:

        def __init__(self):
            pass
        OLDEST = 'Oldest'
        NEWEST = 'Newest'

    def __init__(self, subscriber_name='predix_py_subscriber', batching_enabled=False, auto_send_acks=False, batch_size=100, batch_interval_millis=10000, acks_enabled=False, recency=Recency.OLDEST, ack_duration_before_retry_seconds=30, ack_max_retries=10, ack_retry_interval_seconds=30, topics=None):
        """
        Subscribe Config
        :param subscriber_name: The name of the subscriber
        :param batching_enabled: Should the messages be delivered in batches
        :param batch_size: If batching, what should be the size of the batches
        :param batch_interval_millis: If batching, what should be the max interval
        :param acks_enabled: should the service be expecting acks on delivered messages
        :param ack_duration_before_retry_seconds:  How long should the service wait for an ack before it retry
        :param ack_max_retries: How many retries should the service wait for
        :param ack_retry_interval_seconds: after the initial retry, what should be the period of the message retry
        :param recency: What messages should be sent when connected, all messages in the queue or only new messages
        :param topics: What topics should be subscribed too
        """
        self.subscriber_name = subscriber_name
        self.batching_enabled = batching_enabled
        self.batch_size = batch_size
        self.batch_interval_millis = batch_interval_millis
        self.acks_enabled = acks_enabled
        self.recency = recency
        self.ack_duration_before_retry_seconds = ack_duration_before_retry_seconds
        self.ack_max_retries = ack_max_retries
        self.ack_retry_interval_seconds = ack_retry_interval_seconds
        self.topics = topics if topics is not None else []
        if topics is not None:
            raise