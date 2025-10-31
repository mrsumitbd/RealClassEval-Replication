from toytree.core import Canvas, Cartesian
import numpy as np
from typing import List
from dataclasses import dataclass, field

@dataclass
class Grid:
    nrows: int
    ncols: int
    width: int
    height: int
    layout: str
    margin: int
    padding: int
    scale_bar: bool
    canvas: Canvas = field(default=None, init=False)
    axes: List[Cartesian] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.get_canvas()
        self.get_axes()

    def get_axes(self) -> None:
        """Set .axes attribute with Cartesian and set margin.
        """
        nplots = self.nrows * self.ncols
        grid = np.arange(nplots).reshape((self.nrows, self.ncols))
        for idx in range(nplots):
            if self.margin is not None:
                margin = self.margin
            else:
                if self.nrows == 1:
                    margin = [50, 10, 50, 30]
                else:
                    margin = [30, 30, 30, 30]
                    row, _ = np.where(grid == idx)
                    if row == 0:
                        margin[0] += 10
                        margin[2] -= 10
                    if row == self.nrows - 1:
                        margin[2] += 10
                        margin[0] -= 10
                if self.scale_bar:
                    if self.layout in 'du':
                        margin[3] += 20
                    elif self.layout in 'lr':
                        margin[2] += 20
                margin = tuple(margin)
            axes = self.canvas.cartesian(grid=(self.nrows, self.ncols, idx), padding=self.padding, margin=margin)
            axes.margin = margin
            self.axes.append(axes)

    def get_canvas(self) -> None:
        """set the canvas with user supplied height width else estimated"""
        if self.layout in ('d', 'u'):
            minx = 225
            miny = 250
            self.width = self.width if self.width else min(750, minx * self.ncols)
            self.height = self.height if self.height else min(750, miny * self.nrows)
        else:
            minx = 250
            miny = 225
            self.height = self.height if self.height else min(750, minx * self.nrows)
            self.width = self.width if self.width else min(750, miny * self.ncols)
        self.canvas = Canvas(height=self.height, width=self.width)