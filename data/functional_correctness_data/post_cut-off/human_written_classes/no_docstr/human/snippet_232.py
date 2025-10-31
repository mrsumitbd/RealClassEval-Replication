class MaiThinkingManager:

    def __init__(self):
        self.mai_think_list = []

    def get_mai_think(self, chat_id):
        for mai_think in self.mai_think_list:
            if mai_think.chat_id == chat_id:
                return mai_think
        mai_think = MaiThinking(chat_id)
        self.mai_think_list.append(mai_think)
        return mai_think