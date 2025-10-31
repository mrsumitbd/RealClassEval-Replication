import struct
import gzip

class CacheWriter:

    def __init__(self, file_name, wavefront):
        self.file_name = file_name
        self.wavefront = wavefront
        self.meta = Meta()

    def write(self):
        logger.info('%s creating cache', self.file_name)
        self.meta.mtllibs = self.wavefront.mtllibs
        offset = 0
        fd = gzip.open(cache_name(self.file_name), 'wb')
        for mat in self.wavefront.materials.values():
            if len(mat.vertices) == 0:
                continue
            self.meta.add_vertex_buffer(mat.name, mat.vertex_format, offset, len(mat.vertices) * 4)
            offset += len(mat.vertices) * 4
            fd.write(struct.pack('{}f'.format(len(mat.vertices)), *mat.vertices))
        fd.close()
        self.meta.write(meta_name(self.file_name))