import cairo
import os

class MovieFrame:

    def __init__(self, src='', time=None):
        self.src = src
        self.time = time
        if self.time:
            hg.cvSetCaptureProperty(self.src, hg.CV_CAP_PROP_POS_FRAMES, self.time)
        self.iplimage = hg.cvQueryFrame(self.src)
        self.width = self.iplimage.width
        self.height = self.iplimage.height
        self.image = opencv.cvCreateImage(opencv.cvGetSize(self.iplimage), 8, 4)
        opencv.cvCvtColor(self.iplimage, self.image, opencv.CV_BGR2BGRA)
        self.buffer = numpy.fromstring(self.image.imageData, dtype=numpy.uint32).astype(numpy.uint32)
        self.buffer.shape = (self.image.width, self.image.height)
        self.time = hg.cvGetCaptureProperty(self.src, hg.CV_CAP_PROP_POS_MSEC)

    def _data(self):
        return cairo.ImageSurface.create_for_data(self.buffer, cairo.FORMAT_RGB24, self.width, self.height, self.width * 4)
    data = property(_data)

    def detectObject(self, classifier):
        self.grayscale = opencv.cvCreateImage(opencv.cvGetSize(self.iplimage), 8, 1)
        opencv.cvCvtColor(self.iplimage, self.grayscale, opencv.CV_BGR2GRAY)
        self.storage = opencv.cvCreateMemStorage(0)
        opencv.cvClearMemStorage(self.storage)
        opencv.cvEqualizeHist(self.grayscale, self.grayscale)
        try:
            self.cascade = opencv.cvLoadHaarClassifierCascade(os.path.join(os.path.dirname(__file__), classifier + '.xml'), opencv.cvSize(1, 1))
        except:
            raise AttributeError('could not load classifier file')
        self.objects = opencv.cvHaarDetectObjects(self.grayscale, self.cascade, self.storage, 1.2, 2, opencv.CV_HAAR_DO_CANNY_PRUNING, opencv.cvSize(50, 50))
        return self.objects

    def _faces(self):
        classifier = 'haarcascade_frontalface_alt'
        return self.detectObject(classifier)
    faces = property(_faces)