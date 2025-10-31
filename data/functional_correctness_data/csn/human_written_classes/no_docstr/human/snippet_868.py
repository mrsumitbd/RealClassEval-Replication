class ManagerDescriptions:

    def __init__(self):
        self.descriptions = {}

    def add(self, manager_description):
        manager_name = manager_description.manager_name
        if manager_name in self.descriptions:
            raise Exception('Problem configuring job managers, multiple managers with name %s' % manager_name)
        self.descriptions[manager_name] = manager_description