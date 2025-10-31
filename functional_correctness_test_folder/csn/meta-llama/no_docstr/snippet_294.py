
import rospy
from rospy.topics import Subscriber
import pickle


class ListenerContainer:

    def __init__(self, topics=None, addresses=None, nameserver='localhost', services=''):
        self.topics = topics if topics is not None else []
        self.addresses = addresses if addresses is not None else []
        self.nameserver = nameserver
        self.services = services
        self.subscribers = []
        self.initialize_listeners()

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.initialize_listeners()

    def initialize_listeners(self):
        self.stop()
        for topic in self.topics:
            msg_type = rospy.get_published_topics(topic)
            if msg_type:
                msg_type = msg_type[0][1]
                self.subscribers.append(Subscriber(
                    topic, msg_type, self.callback))

    def callback(self, msg):
        # You need to implement the callback function according to your needs
        # For demonstration purposes, it just prints the received message
        print(msg)

    def restart_listener(self, topics):
        self.topics = topics
        self.initialize_listeners()

    def stop(self):
        for sub in self.subscribers:
            sub.unregister()
        self.subscribers = []
