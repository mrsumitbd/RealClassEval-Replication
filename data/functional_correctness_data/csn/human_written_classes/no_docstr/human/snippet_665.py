class Camera:

    def __init__(self, cam=0, width=None, height=None):
        self.path = cam
        self.video = hg.cvCreateCameraCapture(self.path)
        if width:
            hg.cvSetCaptureProperty(self.video, hg.CV_CAP_PROP_FRAME_WIDTH, width)
        if height:
            hg.cvSetCaptureProperty(self.video, hg.CV_CAP_PROP_FRAME_HEIGHT, height)

    def frame(self, t=None):
        frame = MovieFrame(src=self.video, time=None)
        return frame