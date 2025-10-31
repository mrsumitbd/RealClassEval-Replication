from xrd import XRD, Link, Element

class BaseHostMeta:

    def __init__(self, *args, **kwargs):
        self.xrd = XRD()

    def render(self):
        return self.xrd.to_xml().toprettyxml(indent='  ', encoding='UTF-8')