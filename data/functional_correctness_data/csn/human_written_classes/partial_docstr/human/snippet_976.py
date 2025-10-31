import numpy as np
import warnings
from stsci.image.numcombine import numCombine, num_combine
from scipy import signal

class minmed:
    """ **DEPRECATED** Create a median array, rejecting the highest pixel and
    computing the lowest valid pixel after mask application

        # In this case we want to calculate two things:
        #   1) the median array, rejecting the highest pixel (thus running
        #      imcombine with nlow=0, nhigh=1, nkeep=1, using the masks)
        #   2) the lowest valid pixel after applying the masks (thus running
        #      imcombine with nlow=0, nhigh=3, nkeep=1, using the masks)
        #
        # We also calculate the sum of the weight files (to produce the total
        # effective exposure time for each pixel).
        #
        # The total effective background in the final image is calculated as follows:
        #   - convert background for each input image to counts/s (divide by exptime)
        #   - multiply this value by the weight image, to obtain the effective background
        #     counts (in DN) for each pixel, for each image
        #   - Add these images together, to obtain the total effective background
        #     for the combined image.
        #
        # Once we've made these two files, then calculate the SNR based on the
        # median-pixel image, and compare with the minimum.

    In this version of the mimmed algorithm we assume that the units of all
    input data is electons.
    """

    def __init__(self, imageList, weightImageList, readnoiseList, exposureTimeList, backgroundValueList, weightMaskList=None, combine_grow=1, combine_nsigma1=4, combine_nsigma2=3, fillval=False):
        warnings.warn("The 'minmed' class is deprecated and may be removed in a future version. Use 'min_med()' instead.", DeprecationWarning)
        self._imageList = imageList
        self._weightImageList = weightImageList
        self._weightMaskList = weightMaskList
        self._exposureTimeList = exposureTimeList
        self._readnoiseList = readnoiseList
        self._backgroundValueList = backgroundValueList
        self._numberOfImages = len(self._imageList)
        self._combine_grow = combine_grow
        self._combine_nsigma1 = combine_nsigma1
        self._combine_nsigma2 = combine_nsigma2
        if fillval:
            combtype_mean = 'imean'
            combtype_median = 'imedian'
        else:
            combtype_mean = 'mean'
            combtype_median = 'median'
        median_file = np.zeros(self._imageList[0].shape, dtype=self._imageList[0].dtype)
        if self._numberOfImages == 2:
            tmp = numCombine(self._imageList, numarrayMaskList=self._weightMaskList, combinationType=combtype_mean, nlow=0, nhigh=0, nkeep=1, upper=None, lower=None)
            median_file = tmp.combArrObj
        else:
            tmp = numCombine(self._imageList, numarrayMaskList=self._weightMaskList, combinationType=combtype_median, nlow=0, nhigh=1, nkeep=1, upper=None, lower=None)
            median_file = tmp.combArrObj
            if self._weightMaskList in [None, []]:
                self._weightMaskList = [np.zeros(self._imageList[0].shape, dtype=self._imageList[0].dtype)] * len(self._imageList)
            tmpList = []
            for image in range(len(self._imageList)):
                tmp = np.where(self._weightMaskList[image] == 1, 0, self._imageList[image])
                tmpList.append(tmp)
            maskSum = self._sumImages(self._weightMaskList)
            sciSum = self._sumImages(tmpList)
            del tmpList
            median_file = np.where(maskSum == self._numberOfImages - 1, sciSum, median_file)
        if self._weightMaskList in [None, []]:
            self._weightMaskList = [np.zeros(self._imageList[0].shape, dtype=self._imageList[0].dtype)] * len(self._imageList)
        maskSum = self._sumImages(self._weightMaskList)
        maxValue = -1000000000.0
        for image in self._imageList:
            newMax = image.max()
            if newMax > maxValue:
                maxValue = newMax
        for image in range(len(self._imageList)):
            self._imageList[image] = np.where(self._weightMaskList[image] == 1, maxValue + 1, self._imageList[image])
        tmp = numCombine(self._imageList, numarrayMaskList=None, combinationType=combtype_median, nlow=0, nhigh=self._numberOfImages - 1, nkeep=1, upper=None, lower=None)
        minimum_file = tmp.combArrObj
        minimum_file = np.where(maskSum == self._numberOfImages, 0, minimum_file)
        backgroundFileList = []
        for image in range(len(self._weightImageList)):
            tmp = self._weightImageList[image] * (self._backgroundValueList[image] / self._exposureTimeList[image])
            backgroundFileList.append(tmp)
        bkgd_file = self._sumImages(backgroundFileList)
        del backgroundFileList
        readnoiseFileList = []
        for image in range(len(self._weightMaskList)):
            tmp = np.logical_not(self._weightMaskList[image]) * (self._readnoiseList[image] * self._readnoiseList[image])
            readnoiseFileList.append(tmp)
        readnoise_file = self._sumImages(readnoiseFileList)
        del readnoiseFileList
        weight_file = self._sumImages(self._weightImageList)
        minimum_file_weighted = minimum_file * weight_file
        median_file_weighted = median_file * weight_file
        del weight_file
        rms_file2 = np.fmax(median_file_weighted + bkgd_file + readnoise_file, np.zeros_like(median_file_weighted))
        rms_file = np.sqrt(rms_file2)
        del bkgd_file
        del readnoise_file
        median_rms_file = median_file_weighted - rms_file * self._combine_nsigma1
        if self._combine_grow != 0:
            minimum_flag_file = np.where(np.less(minimum_file_weighted, median_rms_file), 1, 0)
            boxsize = int(2 * self._combine_grow + 1)
            boxshape = (boxsize, boxsize)
            minimum_grow_file = np.zeros(self._imageList[0].shape, dtype=self._imageList[0].dtype)
            if boxsize <= 0:
                errormsg1 = '############################################################\n'
                errormsg1 += "# The boxcar convolution in minmed has failed.  The 'grow' #\n"
                errormsg1 += '# parameter must be greater than or equal to zero. You     #\n'
                errormsg1 += "# specified an input value for the 'grow' parameter of:    #\n"
                errormsg1 += '        combine_grow: ' + str(self._combine_grow) + '\n'
                errormsg1 += '############################################################\n'
                raise ValueError(errormsg1)
            if boxsize > self._imageList[0].shape[0]:
                errormsg2 = '############################################################\n'
                errormsg2 += "# The boxcar convolution in minmed has failed.  The 'grow' #\n"
                errormsg2 += '# parameter specified has resulted in a boxcar kernel that #\n'
                errormsg2 += '# has dimensions larger than the actual image.  You        #\n'
                errormsg2 += "# specified an input value for the 'grow' parameter of:    #\n"
                errormsg2 += '        combine_grow: ' + str(self._combine_grow) + '\n'
                errormsg2 += '############################################################\n'
                print(self._imageList[0].shape)
                raise ValueError(errormsg2)
            ker = np.ones(boxshape) / float(boxsize ** 2)
            minimum_grow_file = signal.convolve2d(minimum_flag_file, ker, boundary='fill', mode='same')
            del minimum_flag_file
            temp1 = median_file_weighted - rms_file * self._combine_nsigma1
            temp2 = median_file_weighted - rms_file * self._combine_nsigma2
            median_rms2_file = np.where(np.equal(minimum_grow_file, 0), temp1, temp2)
            del temp1
            del temp2
            del rms_file
            del minimum_grow_file
            self.combArrObj = np.where(np.less(minimum_file_weighted, median_rms2_file), minimum_file, median_file)
        else:
            self.combArrObj = np.where(np.less(minimum_file_weighted, median_rms_file), minimum_file, median_file)
        self.combArrObj = np.where(maskSum == self._numberOfImages, 0, self.combArrObj)

    def _sumImages(self, numarrayObjectList):
        """ Sum a list of numarray objects. """
        if numarrayObjectList in [None, []]:
            return None
        tsum = np.zeros(numarrayObjectList[0].shape, dtype=numarrayObjectList[0].dtype)
        for image in numarrayObjectList:
            tsum += image
        return tsum