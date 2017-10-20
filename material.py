from PyQt4 import QtGui, QtCore

from material_shadow import MaterialShadowEffect

THEME_LIGHT = "light"
THEME_DARK = "dark"

PROPERTY_THEME = "theme"
PROPERTY_PRIMARY_COLOR = "primary_color"
PROPERTY_SECONDARY_COLOR = "secondary_color"


def _get_property(key, default):
    property_ = str(QtGui.QApplication.instance().property(key).toString())
    if not property_:
        property_ = default
    return property_


def _get_primary_color():
    return _get_property(PROPERTY_PRIMARY_COLOR, "#000099")


def _get_secondary_color():
    return _get_property(PROPERTY_SECONDARY_COLOR, "#FFFFFFF")


def _get_status_bar_color():
    return "#E0E0E0" if _get_property(PROPERTY_THEME, THEME_LIGHT) == THEME_LIGHT else "#000000"


def _get_app_bar_color():
    return "#F5F5F5" if _get_property(PROPERTY_THEME, THEME_LIGHT) == THEME_LIGHT else "#212121"


def _get_background_color():
    return "#FAFAFA" if _get_property(PROPERTY_THEME, THEME_LIGHT) == THEME_LIGHT else "#303030"


def _get_card_color():
    return "#FFFFFF" if _get_property(PROPERTY_THEME, THEME_LIGHT) == THEME_LIGHT else "#424242"


def _get_stylesheet(file_name):
    # TODO cache these
    primary_color = _get_primary_color()
    secondary_color = _get_secondary_color()
    c = QtGui.QColor(primary_color)
    primary_rgb = "{r},{g},{b}".format(r=c.red(), g=c.green(), b=c.blue())
    background_color = _get_background_color()
    card_color = _get_card_color()

    with open(file_name) as f:
        raw_style_sheet = f.read()
        style_sheet = (raw_style_sheet.replace("@background_color", background_color)
                       .replace("@card_color", card_color)
                       .replace("@primary_color", primary_color)
                       .replace("@primary_rgb", primary_rgb)
                       .replace("@secondary_color", secondary_color))
    return style_sheet


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        style_sheet = _get_stylesheet("main_window.qss")
        self.setStyleSheet(style_sheet)


class RaisedButton(QtGui.QPushButton):
    def __init__(self, *__args):
        QtGui.QPushButton.__init__(self, *__args)

        style_sheet = _get_stylesheet("raised_button.qss")
        self.setStyleSheet(style_sheet)

        # self.effect = QtGui.QGraphicsDropShadowEffect(self.parent())
        self.effect = MaterialShadowEffect(self.parent())
        # self.effect.setOffset(2)
        # self.effect.setBlurRadius(2)
        # self.effect.setEnabled(False)
        self.setGraphicsEffect(self.effect)
        self.setMouseTracking(True)
        self.setMinimumWidth(88)

    def enterEvent(self, event):
        if self.isEnabled():
            self.effect.set_elevation(2)
        QtGui.QPushButton.enterEvent(self, event)

    def leaveEvent(self, event):
        if self.isEnabled():
            self.effect.set_elevation(0)
        QtGui.QPushButton.leaveEvent(self, event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.effect.set_elevation(8)
        super(RaisedButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.effect.set_elevation(2)
        super(RaisedButton, self).mouseReleaseEvent(event)


class FlatButton(QtGui.QPushButton):
    def __init__(self, *__args):
        QtGui.QPushButton.__init__(self, *__args)

        style_sheet = _get_stylesheet("flat_button.qss")
        self.setStyleSheet(style_sheet)


class TextField(QtGui.QLineEdit):
    def __init__(self, *__args):
        QtGui.QLineEdit.__init__(self, *__args)

        style_sheet = _get_stylesheet("text_field.qss")
        self.setStyleSheet(style_sheet)

        # layout = QtGui.QHBoxLayout()
        # self.setLayout(layout)
        # layout.addWidget(QtGui.QLabel('sajt'))


class TabWidget(QtGui.QTabWidget):
    def __init__(self):
        QtGui.QTabWidget.__init__(self)

        style_sheet = _get_stylesheet("tab_widget.qss")
        self.setStyleSheet(style_sheet)

        # self.tabBar().setCursor(QtCore.Qt.PointingHandCursor)

    def addTab(self, page, *args):

        _args = list(args)
        if _args:
            _args[-1] = str(_args[-1]).upper()
        return QtGui.QTabWidget.addTab(self, page, *_args)


class TableView(QtGui.QTableView):
    def __init__(self, parent=None):
        QtGui.QTableView.__init__(self, parent)

        style_sheet = _get_stylesheet("table_view.qss")
        self.setStyleSheet(style_sheet)


class Dropdown(QtGui.QComboBox):
    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)

        style_sheet = _get_stylesheet("dropdown.qss")
        self.setStyleSheet(style_sheet)

        # Qt wtf
        # See https://stackoverflow.com/a/13313676
        item_delegate = QtGui.QStyledItemDelegate()
        self.setItemDelegate(item_delegate)


class Card(QtGui.QFrame):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        style_sheet = _get_stylesheet("card.qss")
        self.setStyleSheet(style_sheet)

        self.effect = MaterialShadowEffect(self.parent())
        self.setGraphicsEffect(self.effect)

    def enterEvent(self, event):
        if self.isEnabled():
            self.effect.set_elevation(8)
        QtGui.QFrame.enterEvent(self, event)

    def leaveEvent(self, event):
        if self.isEnabled():
            self.effect.set_elevation(0)
        QtGui.QFrame.leaveEvent(self, event)


# class ShadowStuff(QtGui.QGraphicsDropShadowEffect):
#     def draw(self, painter):
#         if self.blurRadius() <= 0 and self.offset().isNull():
#             self.drawSource(painter)
#             return
#
#         mode = QtGui.QGraphicsDropShadowEffect.PadToEffectiveBoundingRect
#         if painter.paintEngine().type() == QtGui.QPaintEngine.OpenGL2:
#             mode = QtGui.QGraphicsDropShadowEffect.NoPad
#
#         # Draw pixmap in device coordinates to avoid pixmap scaling.
#         offset = QtCore.QPoint()
#         pixmap = self.sourcePixmap(QtCore.Qt.DeviceCoordinates, mode=mode)
#         if not pixmap:
#             return
#
#         restore_transform = painter.worldTransform()
#         painter.setWorldTransform(QtGui.QTransform())
#         self.filter.draw(painter, offset, pixmap)
#         painter.setWorldTransform(restore_transform)
