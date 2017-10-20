from PyQt4.QtCore import *
from PyQt4.QtGui import *

AMBIENT_SHADOW_OPACITY = 255 * 0.08
KEY_SHADOW_OPACITY = 255 * 0.26


class MaterialShadowEffect(QGraphicsEffect):
    def __init__(self, parent):
        super(MaterialShadowEffect, self).__init__(parent)
        self._elevation = 0

    def set_elevation(self, elevation):
        self._elevation = elevation
        self.updateBoundingRect()

    def _key_offset(self):
        return self._elevation * 0.9166846071 + 0.0001808396125

    def _key_blur(self):
        return self._elevation * 0.5

    def _ambient_blur(self):
        return self._elevation * 0.6874949051 - 0.00003362708332

    def draw(self, painter):
        if self._elevation == 0:
            self.drawSource(painter)
            return

        mode = QGraphicsEffect.PadToEffectiveBoundingRect
        px, offset = self.sourcePixmap(Qt.DeviceCoordinates, mode)

        # return if no source
        if px.isNull():
            return

        # save world transform
        restore_transform = painter.worldTransform()
        painter.setWorldTransform(QTransform())

        # key shadow
        _draw_shadow(painter, px, offset, self._key_offset(), self._key_blur(), KEY_SHADOW_OPACITY)
        # ambient shadow
        _draw_shadow(painter, px, offset, 0, self._ambient_blur(), AMBIENT_SHADOW_OPACITY)

        # draw the actual pixmap
        painter.drawPixmap(offset, px, QRectF())

        painter.setWorldTransform(restore_transform)

    def boundingRectFor(self, rect):
        b_max = max([self._ambient_blur(), self._key_blur()])
        return rect.adjusted(-b_max, -b_max, b_max, b_max + self._key_offset())


def _draw_shadow(painter, px, offset, y_offset, blur, opacity):
    # Calculate size for the background image
    szi = QSize(px.size().width(), px.size().height())

    tmp = QImage(szi, QImage.Format_ARGB32_Premultiplied)
    scaled = QPixmap(px.scaled(szi))
    tmp.fill(0)

    tmp_painter = QPainter(tmp)
    tmp_painter.setCompositionMode(QPainter.CompositionMode_Source)
    tmp_painter.drawPixmap(QPointF(-blur, -blur + y_offset / 2.0), scaled)
    tmp_painter.end()

    # apply blur
    blur_effect = QGraphicsBlurEffect()
    blur_effect.setBlurRadius(blur)
    blurred = apply_effect_to_image(tmp, blur_effect, blur)

    tmp = blurred

    # blacken the image
    tmp_painter.begin(tmp)
    tmp_painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    tmp_painter.fillRect(tmp.rect(), QColor(0, 0, 0, opacity))
    tmp_painter.end()

    # draw the blurred shadow
    painter.drawImage(offset, tmp)


def apply_effect_to_image(src, effect, extent=0.0):
    if src.isNull():
        return QImage()
    if not effect:
        return src
    scene = QGraphicsScene()
    item = QGraphicsPixmapItem()
    item.setPixmap(QPixmap.fromImage(src))
    item.setGraphicsEffect(effect)
    scene.addItem(item)
    res = QImage(src.size() + QSize(extent * 2, extent * 2), QImage.Format_ARGB32)
    res.fill(Qt.transparent)
    ptr = QPainter(res)
    scene.render(ptr, QRectF(), QRectF(-extent, -extent, src.width() + extent * 2, src.height() + extent * 2))
    return res
