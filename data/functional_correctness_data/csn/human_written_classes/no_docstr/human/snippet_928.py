class ConditionalFormat:

    def __init__(self, **kwargs):
        self.background_color = kwargs.pop('background_color', kwargs.pop('backgroundColor', None))
        self.bold = kwargs.pop('bold', None)
        self.filter = kwargs.pop('filter', None)
        self.italic = kwargs.pop('italic', None)
        self.strike_through = kwargs.pop('strike_through', kwargs.pop('strikethrough', None))
        self.text_color = kwargs.pop('text_color', kwargs.pop('textColor', None))

    def to_json(self):
        data = {'backgroundcolor': self.background_color, 'bold': self.bold, 'filter': self.filter, 'italic': self.italic, 'strikethrough': self.strike_through, 'textcolor': self.text_color}
        return data