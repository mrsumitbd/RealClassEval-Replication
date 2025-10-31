class LineProps:
    """ abstraction for Line2D properties, closely related to a
    MatPlotlib Line2D.  used to set internal line properties, and
    to  make the matplotlib calls to set the Line2D properties
    """
    REPRFMT = "LineProps(color='{color:s}', style='{style:s}', linewidth={linewidth:.1f},\n          label='{label:s}', zorder={zorder:d}, drawstyle='{drawstyle:s}', alpha={alpha:3f},\n          marker='{marker:s}', markersize={markersize:.1f}, markercolor={markercolor:s})"

    def __init__(self, color='black', style='solid', drawstyle='default', linewidth=2, marker='no symbol', markersize=4, markercolor=None, fill=False, alpha=1.0, zorder=1, label='', mpline=None, yaxes=1):
        self.color = color
        self.alpha = alpha
        self.style = style
        self.drawstyle = drawstyle
        self.fill = fill
        self.linewidth = linewidth
        self.marker = marker
        self.markersize = markersize
        if markercolor is None:
            markercolor = color
        self.markercolor = markercolor
        self.label = label
        self.zorder = zorder
        self.mpline = mpline
        self.yaxes = yaxes

    def __repr__(self):
        if self.zorder is None:
            self.zorder = 30
        return self.REPRFMT.format(**self.__dict__)

    def set(self, color=None, style=None, drawstyle=None, linewidth=None, marker=None, markersize=None, markercolor=None, zorder=None, label=None, fill=False, alpha=None, yaxes=None):
        self.color = ifnot_none(color, self.color)
        self.style = ifnot_none(style, self.style)
        self.drawstyle = ifnot_none(drawstyle, self.drawstyle)
        self.fill = ifnot_none(fill, self.fill)
        self.linewidth = ifnot_none(linewidth, self.linewidth)
        self.marker = ifnot_none(marker, self.marker)
        self.markersize = ifnot_none(markersize, self.markersize)
        self.markercolor = ifnot_none(markercolor, self.markercolor)
        self.label = ifnot_none(label, self.label)
        self.zorder = ifnot_none(zorder, self.zorder)
        self.alpha = ifnot_none(alpha, self.alpha)
        self.yaxes = ifnot_none(yaxes, self.yaxes)

    def asdict(self):
        """as dictionary"""
        return {'color': self.color, 'style': self.style, 'linewidth': self.linewidth, 'zorder': self.zorder, 'fill': self.fill, 'label': self.label, 'yaxes': self.yaxes, 'drawstyle': self.drawstyle, 'alpha': self.alpha, 'marker': self.marker, 'markersize': self.markersize, 'markercolor': self.markercolor}