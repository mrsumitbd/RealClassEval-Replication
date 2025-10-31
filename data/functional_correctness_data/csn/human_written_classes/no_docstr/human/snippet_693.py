class ReportTemplate:

    def __init__(self, isGlobal, id, last_update, template_type, title, type, user):
        self.isGlobal = int(isGlobal)
        self.id = int(id)
        self.last_update = str(last_update).replace('T', ' ').replace('Z', '').split(' ')
        self.template_type = template_type
        self.title = title
        self.type = type
        self.user = user.LOGIN

    def __repr__(self):
        return f'qualys_id: {self.id}, title: {self.title}'