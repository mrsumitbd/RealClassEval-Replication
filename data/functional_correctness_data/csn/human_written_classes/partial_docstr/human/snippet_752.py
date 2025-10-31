import numpy as np

class MultiPlotter:
    """NetPyNE object to generate line plots on multiple axes"""

    def __init__(self, data, kind, metafig=None, **kwargs):
        self.kind = kind
        self.data = data
        numLines = len(self.data['y'])
        if metafig is None:
            metafig = MetaFigure(kind=kind, subplots=numLines, **kwargs)
        self.metafig = metafig

    def plot(self, **kwargs):
        x = np.array(self.data.get('x'))
        y = np.array(self.data.get('y'))
        color = self.data.get('color')
        marker = self.data.get('marker')
        markersize = self.data.get('markersize')
        linewidth = self.data.get('linewidth')
        alpha = self.data.get('alpha')
        label = self.data.get('label')
        if len(np.shape(y)) == 1:
            numLines = 1
            y = [y]
        else:
            numLines = len(y)
        if type(color) != list:
            colors = [color for line in range(numLines)]
        else:
            colors = color
        if type(marker) != list:
            markers = [marker for line in range(numLines)]
        else:
            markers = marker
        if type(markersize) != list:
            markersizes = [markersize for line in range(numLines)]
        else:
            markersizes = markersize
        if type(linewidth) != list:
            linewidths = [linewidth for line in range(numLines)]
        else:
            linewidths = linewidth
        if type(alpha) != list:
            alphas = [alpha for line in range(numLines)]
        else:
            alphas = alpha
        if label is None:
            labels = [None for line in range(numLines)]
        else:
            labels = label
        for index, line in enumerate(y):
            curAx = self.metafig.ax[index]
            curData = {}
            curData['x'] = x
            curData['y'] = [y[index]]
            curData['color'] = colors[index]
            curData['marker'] = markers[index]
            curData['markersize'] = markersizes[index]
            curData['linewidth'] = linewidths[index]
            curData['alpha'] = alphas[index]
            curData['label'] = labels[index]
            curPlotter = LinesPlotter(data=curData, kind='LFPPSD', axis=curAx, **kwargs)
            curPlotter.plot(**kwargs)
        self.metafig.finishFig(**kwargs)
        if 'returnPlotter' in kwargs and kwargs['returnPlotter']:
            return self.metafig
        else:
            return self.metafig.fig