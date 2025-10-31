class Topic:

    def __init__(self, topics):
        self.topic = {'general': ''}
        self.topics = topics

    def __setitem__(self, key, value):
        value = value.strip()
        if value and value[0] == '.':
            index = 1
            current_topic = self.topic[key].split('.')
            while value[index] == '.':
                index += 1
                current_topic.pop()
            current_topic.append(value[index:])
            value = '.'.join(current_topic)
        self.topic[key] = value

    def __getitem__(self, key):
        topic = self.topic[key]
        if topic in self.topics():
            return topic
        return ''