class SegmentSorter:

    def __init__(self, segments):
        self._segments = segments
        self._sorted = False

    @property
    def segments(self):
        if not self._sorted:
            self._sort_segments()
        return self._segments

    def _sort_segments(self):
        self._segments.sort(key=self.segment_key)
        self._sorted = True

    @staticmethod
    def segment_key(segment_tuple):
        segment_data = segment_tuple[1]
        return (segment_data['syl'], segment_data['son'], segment_data['cons'], segment_data['cont'], segment_data['delrel'], segment_data['lat'], segment_data['nas'], segment_data['strid'], segment_data['voi'], segment_data['sg'], segment_data['cg'], segment_data['ant'], segment_data['cor'], segment_data['distr'], segment_data['lab'], segment_data['hi'], segment_data['lo'], segment_data['back'], segment_data['round'], segment_data['velaric'], segment_data['tense'], segment_data['long'], segment_data['hitone'], segment_data['hireg'])