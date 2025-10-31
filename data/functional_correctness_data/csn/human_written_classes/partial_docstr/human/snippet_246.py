import time

class EventNotifyHandlerBase:
    """Base class for `soco.events.EventNotifyHandler` and
    `soco.events_twisted.EventNotifyHandler`.
    """

    def handle_notification(self, headers, content):
        """Handle a ``NOTIFY`` request by building an `Event` object and
        sending it to the relevant Subscription object.

        A ``NOTIFY`` request will be sent by a Sonos device when a state
        variable changes. See the `UPnP Spec §4.3 [pdf]
        <http://upnp.org/specs/arch/UPnP-arch
        -DeviceArchitecture-v1.1.pdf>`_  for details.

        Args:
            headers (dict): A dict of received headers.
            content (str): A string of received content.
        Note:
            Each of the :py:mod:`soco.events` and the
            :py:mod:`soco.events_twisted` modules has a **subscriptions_map**
            object which keeps a record of Subscription objects. The
            *get_subscription* method of the **subscriptions_map** object is
            used to look up the subscription to which the event relates. When
            the Event Listener runs in a thread (the default), a lock is
            used by this method for thread safety. The *send_event*
            method of the relevant Subscription will first check to see
            whether the *callback* variable of the Subscription has been
            set. If it has been and is callable, then the *callback*
            will be called with the `Event` object. Otherwise, the `Event`
            object will be sent to the event queue of the Subscription
            object. The *callback* variable of the Subscription object is
            intended for use only if :py:mod:`soco.events_twisted` is being
            used, as calls to it are not threadsafe.

            This method calls the log_event method, which must be overridden
            in the class that inherits from this class.
        """
        timestamp = time.time()
        seq = headers['seq']
        sid = headers['sid']
        subscription = self.subscriptions_map.get_subscription(sid)
        if subscription:
            service = subscription.service
            self.log_event(seq, service.service_id, timestamp)
            log.debug('Event content: %s', content)
            variables = parse_event_xml(content)
            event = Event(sid, seq, service, timestamp, variables)
            service._update_cache_on_event(event)
            subscription.send_event(event)
        else:
            log.info('No service registered for %s', sid)

    def log_event(self, seq, service_id, timestamp):
        raise NotImplementedError