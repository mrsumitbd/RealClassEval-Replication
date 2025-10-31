from demosys.loaders.texture import t2d
import base64
from demosys.resources.meta import SceneDescription, TextureDescription
from PIL import Image
import io

class GLTFImage:
    """
    Represent texture data.
    May be a file, embedded data or pointer to data in bufferview
    """

    def __init__(self, data):
        self.uri = data.get('uri')
        self.bufferViewId = data.get('bufferView')
        self.bufferView = None
        self.mimeType = data.get('mimeType')

    def load(self, path):
        if self.bufferView is not None:
            image = Image.open(io.BytesIO(self.bufferView.read_raw()))
        elif self.uri and self.uri.startswith('data:'):
            data = self.uri[self.uri.find(',') + 1:]
            image = Image.open(io.BytesIO(base64.b64decode(data)))
        else:
            path = path / self.uri
            print('Loading:', self.uri)
            image = Image.open(path)
        texture = t2d.Loader(TextureDescription(label='gltf', image=image, flip=False, mipmap=True)).load()
        return texture