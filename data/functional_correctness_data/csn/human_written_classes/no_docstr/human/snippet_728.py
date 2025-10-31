class MessagesStore:
    __messages = []

    @staticmethod
    def pending_messages():
        messages = MessagesStore.__messages
        MessagesStore.__messages = []
        return messages

    @staticmethod
    def write_message(message):
        MessagesStore.__messages.append(str(message))

    @staticmethod
    def clear():
        MessagesStore.__messages = []