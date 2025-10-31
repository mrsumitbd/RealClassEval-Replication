from datetime import datetime, timedelta
from openeoCharger import openeoChargerClass
import re
import json

class databufferClass:
    databuffer = {}

    def __str__(self):
        return json.dumps(self.databuffer, default=str)

    def get_plotly(self, since=None, seriesList=None, subplot_index=None):
        myData = self.get_data(since, seriesList)
        using_subplots = False
        if seriesList is not None:
            for index, series in enumerate(seriesList):
                if re.search(':', series):
                    seriesList[index] = series.split(':')
                    using_subplots = True
        series = []
        if not using_subplots:
            for key, value in myData.items():
                if key != 'time' and (seriesList is None or key in seriesList):
                    if key == 'eo_charger_state_id':
                        text = []
                        last_datum = None
                        for datum in value:
                            if datum == last_datum:
                                text.append(None)
                            else:
                                text.append(openeoChargerClass.CHARGER_STATES[datum])
                            last_datum = datum
                        series.append({'type': 'line', 'line': {'shape': 'hv'}, 'mode': 'lines+text', 'name': self.seriesDict[key], 'key': key, 'stackgroup': None, 'x': myData['time'], 'y': value, 'textposition': 'top center', 'text': text, 'legend': f'legend1' if subplot_index is None else f'legend{subplot_index}', 'legendgroup': '1' if subplot_index is None else f'{subplot_index}', 'xaxis': 'x' if subplot_index is None else f'x{subplot_index}', 'yaxis': 'y' if subplot_index is None else f'y{subplot_index}'})
                    else:
                        series.append({'type': 'line', 'mode': 'lines', 'name': self.seriesDict[key], 'key': key, 'stackgroup': None, 'x': myData['time'], 'y': value, 'legend': f'legend1' if subplot_index is None else f'legend{subplot_index}', 'legendgroup': '1' if subplot_index is None else f'{subplot_index}', 'xaxis': 'x' if subplot_index is None else f'x{subplot_index}', 'yaxis': 'y' if subplot_index is None else f'y{subplot_index}'})
        else:
            for index, subplot in enumerate(seriesList):
                series.extend(self.get_plotly(since, subplot, index + 1))
        return series

    def get_data(self, since=None, seriesList=None):
        i = None
        if since == None:
            i = 0
            while i < len(self.databuffer['time']) and self.databuffer['time'][i] == None:
                i = i + 1
            i = len(self.databuffer['time']) - i
        else:
            i = len(self.databuffer['time']) - 1
            while i >= 0 and self.databuffer['time'][i] != None and (self.databuffer['time'][i] > since):
                i = i - 1
            i = i - 1
            i = len(self.databuffer['time']) - i - 1
        newdatabuffer = {}
        for key, value in self.databuffer.items():
            if seriesList is None or key in seriesList or key == 'time':
                newdatabuffer[key] = [] if i == 0 else value[-i:]
        return newdatabuffer

    def push(self, datapoint):
        modulus = self.count % self.ratio
        deletion_index = (self.count % self.ratio != 0) * self.resolution_boundary
        for key in self.databuffer:
            if key == 'time':
                self.databuffer['time'].append(datetime.now())
                del self.databuffer['time'][deletion_index]
            elif key in datapoint and isinstance(datapoint[key], (int, float)):
                self.databuffer[key].append(datapoint[key])
                del self.databuffer[key][deletion_index]
            else:
                self.databuffer[key].append(None)
                del self.databuffer[key][deletion_index]
        self.count = self.count + 1

    def __init__(self, config, seriesDict):
        self.config = config
        self.seriesDict = seriesDict
        datapoints = round(config['hires_maxage'] / config['hires_interval']) + round((config['lowres_maxage'] - config['hires_maxage']) / config['lowres_interval'])
        self.databuffer['time'] = [None] * datapoints
        for series in seriesDict:
            self.databuffer[series] = [None] * datapoints
        self.ratio = self.config['lowres_interval'] / self.config['hires_interval']
        self.resolution_boundary = datapoints - int(self.config['hires_maxage'] / self.config['hires_interval'])
        self.count = 0