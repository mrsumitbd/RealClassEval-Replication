import xml.etree.ElementTree as et

class XmlGenerator:

    def __init__(self):
        self.startTag = 'CGImage'
        self.endTag = '/>'

    def make_xml(self, startFrame: int=0, endFrame: int=1, filePrefix: str='', fileExtension: str='.png', padding: int=4, exportAsAnimation: bool=False, fps: int=30, step: int=1, withRoot: bool=True) -> et.ElementTree:
        """
            Generate multi-line xml thingy that you can insert into .caml file directly
            if you don't provide anything it'll just use the default
        """
        root = et.Element('root')
        if exportAsAnimation:
            totalDuration = (endFrame - startFrame) / fps / step
            animations = et.SubElement(root, 'animations')
            animation = et.SubElement(animations, 'animation', {'type': 'CAKeyframeAnimation', 'calculationMode': 'discrete', 'keyPath': 'contents', 'beginTime': '1e-100', 'duration': str(totalDuration), 'removedOnCompletion': '0', 'repeatCount': 'inf', 'repeatDuration': '0', 'speed': '1', 'timeOffset': '0'})
            values = et.SubElement(animation, 'values')
        si = startFrame
        for i in range(startFrame, int((endFrame + step) / step)):
            n = f'{si:0{padding}d}'
            si += step
            if exportAsAnimation:
                asset = et.SubElement(values, self.startTag)
            else:
                asset = et.SubElement(root, self.startTag)
            asset.set('src', f'assets/{filePrefix}{n}{fileExtension}')
        if withRoot:
            result = et.ElementTree(root)
        elif exportAsAnimation:
            animations_elem = root.find('animations')
            return et.ElementTree(animations_elem)
        else:
            new_root = et.Element('values')
            for child in list(root):
                new_root.append(child)
            return et.ElementTree(new_root)
        return result