from PyQt4.QtCore import *
from PyQt4.QtGui import *

class CustomShadowEffect(QGraphicsEffect):
    def __init__(self, parent):
        super(CustomShadowEffect, self).__init__(parent)
        self._distance = 0
        self._blurRadius = 2
        self._color = QColor(0, 0, 0, 80)

    # def boundingRectFor(rect):
    #     pass

    def set_distance(self, distance):
        self._distance = distance

    # def distance(self):
    #     return self._distance

    def set_blur_radius(self, blur_radius):
        self._blurRadius = blur_radius

    # def blurRadius(self):
    #     return self._blurRadius

    def set_color(self, color):
        self._color = color

    # def color(self):
    #     return self._color

    def draw(self, painter):
        # if (self._blurRadius + self._distance) <= 0:
        #     self.drawSource(painter)
        #     return

        mode = QGraphicsEffect.PadToEffectiveBoundingRect
        px, offset = self.sourcePixmap(Qt.DeviceCoordinates, mode)

        # return if no source
        if px.isNull():
            return

        # save world transform
        restoreTransform = painter.worldTransform()
        painter.setWorldTransform(QTransform())

        # Calculate size for the background image
        szi = QSize(px.size().width() + 2 * self._distance, px.size().height() + 2 * self._distance)

        tmp = QImage(szi, QImage.Format_ARGB32_Premultiplied)
        scaled = QPixmap(px.scaled(szi))
        tmp.fill(0)

        tmpPainter = QPainter(tmp)
        tmpPainter.setCompositionMode(QPainter.CompositionMode_Source)
        tmpPainter.drawPixmap(QPointF(-self._distance, -self._distance), scaled)
        tmpPainter.end()

        # apply blur
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(self._blurRadius)
        blurred = apply_effect_to_image(tmp, blur_effect, self._distance)

        tmp = blurred

        # blacken the image
        tmpPainter.begin(tmp)
        tmpPainter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        tmpPainter.fillRect(tmp.rect(), self._color)
        tmpPainter.end()

        # draw the blurred shadow
        painter.drawImage(offset, tmp)

        # draw the actual pixmap
        painter.drawPixmap(offset, px, QRectF())

    def boundingRectFor(self, rect):
        return rect.adjusted(-self._blurRadius, -self._blurRadius, self._blurRadius, self._blurRadius)


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
