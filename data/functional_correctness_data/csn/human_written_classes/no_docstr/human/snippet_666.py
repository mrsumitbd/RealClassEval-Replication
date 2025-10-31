class Movie:

    def __init__(self, path, start=0, stop=None):
        self.path = path
        self.video = hg.cvCreateFileCapture(self.path)
        if self.video is None:
            raise SBVideoError(f'Could not open stream {self.path}')
        hg.cvSetCaptureProperty(self.video, hg.CV_CAP_PROP_POS_FRAMES, start)

    def frame(self, t=None):
        frame = MovieFrame(src=self.video, time=t)
        return frame