import warnings
from qtpy.QtCore import QObject, QPoint, QRect, Qt, QSizeF, QRectF, QPointF, QThread
from qtpy.QtGui import QColor, QFont, QFontDatabase, QIcon, QIconEngine, QPainter, QPixmap, QTransform, QPalette, QRawFont, QImage

class CharIconPainter:
    """Char icon painter."""

    def paint(self, iconic, painter, rect, mode, state, options):
        """Main paint method."""
        for opt in options:
            self._paint_icon(iconic, painter, rect, mode, state, opt)

    def _paint_icon(self, iconic, painter, rect, mode, state, options):
        """Paint a single icon."""
        painter.save()
        color_options = {QIcon.On: {QIcon.Normal: (options['color_on'], options['on']), QIcon.Disabled: (options['color_on_disabled'], options['on_disabled']), QIcon.Active: (options['color_on_active'], options['on_active']), QIcon.Selected: (options['color_on_selected'], options['on_selected'])}, QIcon.Off: {QIcon.Normal: (options['color_off'], options['off']), QIcon.Disabled: (options['color_off_disabled'], options['off_disabled']), QIcon.Active: (options['color_off_active'], options['off_active']), QIcon.Selected: (options['color_off_selected'], options['off_selected'])}}
        color, char = color_options[state][mode]
        alpha = None
        if isinstance(color, tuple):
            alpha = color[1]
            color = color[0]
        qcolor = QColor(color)
        if alpha:
            qcolor.setAlpha(alpha)
        painter.setPen(qcolor)
        draw_size = round(0.875 * rect.height() * options['scale_factor'])
        prefix = options['prefix']
        animation = options.get('animation')
        if animation is not None:
            animation.setup(self, painter, rect)
        if 'offset' in options:
            rect = QRect(rect)
            rect.translate(round(options['offset'][0] * rect.width()), round(options['offset'][1] * rect.height()))
        x_center = rect.width() * 0.5
        y_center = rect.height() * 0.5
        transform = QTransform()
        transform.translate(+x_center, +y_center)
        if 'vflip' in options and options['vflip'] is True:
            transform.scale(1, -1)
        if 'hflip' in options and options['hflip'] is True:
            transform.scale(-1, 1)
        if 'rotated' in options:
            transform.rotate(options['rotated'])
        transform.translate(-x_center, -y_center)
        painter.setTransform(transform, True)
        painter.setOpacity(options.get('opacity', 1.0))
        draw = options.get('draw')
        if draw not in ('text', 'path', 'glyphrun', 'image'):
            draw = 'path' if animation is not None else 'text'

        def try_draw_rawfont():
            if draw == 'glyphrun' and animation is not None:
                rawfont = iconic.rawfont(prefix, draw_size, QFont.PreferNoHinting)
            else:
                rawfont = iconic.rawfont(prefix, draw_size)
            if not rawfont.fontTable('glyf'):
                return False
            glyph = rawfont.glyphIndexesForString(char)[0]
            advance = rawfont.advancesForGlyphIndexes((glyph,))[0]
            ascent = rawfont.ascent()
            size = QSizeF(abs(advance.x()), ascent + rawfont.descent())
            painter.translate(QRectF(rect).center())
            painter.translate(-size.width() / 2, -size.height() / 2)
            if draw == 'path':
                path = rawfont.pathForGlyph(glyph)
                path.translate(0, ascent)
                path.setFillRule(Qt.WindingFill)
                painter.setRenderHint(QPainter.Antialiasing, True)
                painter.fillPath(path, painter.pen().color())
            elif draw == 'glyphrun':
                if QGlyphRun:
                    glyphrun = QGlyphRun()
                    glyphrun.setRawFont(rawfont)
                    glyphrun.setGlyphIndexes((glyph,))
                    glyphrun.setPositions((QPointF(0, ascent),))
                    painter.drawGlyphRun(QPointF(0, 0), glyphrun)
                else:
                    warnings.warn('QGlyphRun is unavailable for the current Qt binding! QtAwesome will use the default draw values')
                    return False
            elif draw == 'image':
                image = rawfont.alphaMapForGlyph(glyph, QRawFont.PixelAntialiasing).convertToFormat(QImage.Format_ARGB32_Premultiplied)
                painter2 = QPainter(image)
                painter2.setCompositionMode(QPainter.CompositionMode_SourceIn)
                painter2.fillRect(image.rect(), painter.pen().color())
                painter2.end()
                brect = rawfont.boundingRect(glyph)
                brect.translate(0, ascent)
                painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
                painter.drawImage(brect.topLeft(), image)
            else:
                return False
            return True
        if draw == 'text' or not try_draw_rawfont():
            font = iconic.font(prefix, draw_size)
            if animation is not None:
                font.setHintingPreference(QFont.PreferNoHinting)
            painter.setFont(font)
            painter.drawText(rect, int(Qt.AlignCenter | Qt.AlignVCenter), char)
        painter.restore()