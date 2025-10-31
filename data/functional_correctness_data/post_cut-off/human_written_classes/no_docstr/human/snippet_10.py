class Todo:

    def __init__(self, todoId: int=0, content: str='', deadlineTime: str='', createTime: str='', status: str='Done') -> None:
        self.todo_id = todoId
        self.content = content
        self.deadline_time = deadlineTime
        self.create_time = createTime
        self.status = status

    def __str__(self):
        todo_statement = '---\n'
        todo_statement += f'[Action] User have a Plan\n'
        if self.content:
            todo_statement += f'[Content]: {self.content}\n'
        if self.create_time:
            todo_statement += f'[Create Time]: {self.create_time}\n'
        if self.deadline_time:
            todo_statement += f'[Deadline Time]: {self.deadline_time}\n'
        if self.status:
            todo_statement += f'[Status]: {self.status}\n'
        return todo_statement