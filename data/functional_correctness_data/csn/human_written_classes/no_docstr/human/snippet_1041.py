class Scenario:

    def __init__(self, xml, parameters=None):
        self.xml = xml
        self.parameters = parameters

    def __str__(self):
        return self.xml

    def __unicode__(self):
        return self.xml