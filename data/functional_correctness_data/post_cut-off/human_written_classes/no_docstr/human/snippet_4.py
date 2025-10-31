class Chat:

    def __init__(self, sessionId: str='', summary: str='', title: str='', createTime: str='') -> None:
        self.session_id = sessionId
        self.summary = summary
        self.title = title
        self.create_time = createTime

    def __str__(self):
        chat_statement = '---\n'
        chat_statement += f'[Action] User had a chat\n'
        if self.create_time:
            chat_statement += f'[Create Time]: {self.create_time}\n'
        if self.title:
            chat_statement += f'[Title]: {self.title}\n'
        if self.summary:
            chat_statement += f'{self.summary}\n'
        return chat_statement