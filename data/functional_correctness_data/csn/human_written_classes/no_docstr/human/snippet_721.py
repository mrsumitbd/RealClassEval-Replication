class Person:
    __dispatch__ = 'rest'

    def get(self):
        return 'Person details.'

    def post(self):
        return 'Create a child object.'

    def put(self):
        return 'Replace or create this person.'

    def delete(self):
        return 'Delete this person.'