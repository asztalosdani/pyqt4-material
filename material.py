from PyQt4 import QtGui, QtCore

from material_shadow import MaterialShadowEffect

THEME_LIGHT = "light"
THEME_DARK = "dark"

PROPERTY_THEME = "theme"
PROPERTY_PRIMARY_COLOR = "primary_color"
PROPERTY_SECONDARY_COLOR = "secondary_color"
PROPERTY_CLASS = "class"


def _get_property(key, default):
    property_ = str(QtGui.QApplication.instance().property(key).toString())
    if not property_:
        property_ = default
    return property_


def _get_primary_color():
    return _get_property(PROPERTY_PRIMARY_COLOR, "#000099")


def _get_secondary_color():
    return _get_property(PROPERTY_SECONDARY_COLOR, "#FFFFFFF")


def _light_theme_selected():
    return _get_property(PROPERTY_THEME, THEME_LIGHT) == THEME_LIGHT


def _get_value_based_on_theme(light_value, dark_value):
    return light_value if _light_theme_selected() else dark_value


def _get_status_bar_color():
    return _get_value_based_on_theme("#E0E0E0", "#000000")


def _get_app_bar_color():
    return _get_value_based_on_theme("#F5F5F5", "#212121")


def _get_background_color():
    return _get_value_based_on_theme("#FAFAFA", "#303030")


def _get_card_color():
    return _get_value_based_on_theme("#FFFFFF", "#424242")


def _get_primary_text_color():
    return _get_value_based_on_theme("rgba(0, 0, 0, 87%)", "rgba(255, 255, 255, 100%)")


def _get_secondary_text_color():
    return _get_value_based_on_theme("rgba(0, 0, 0, 54%)", "rgba(255, 255, 255, 70%)")


def _get_disabled_or_hint_text_color():
    return _get_value_based_on_theme("rgba(0, 0, 0, 38%)", "rgba(255, 255, 255, 50%)")


def _get_disabled_button_text_color():
    return _get_value_based_on_theme("rgba(0, 0, 0, 26%)", "rgba(255, 255, 255, 30%)")


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
                       .replace("@primary_text_color", _get_primary_text_color())
                       .replace("@secondary_text_color", _get_secondary_text_color())
                       .replace("@disabled_or_hint_text_color", _get_disabled_or_hint_text_color())
                       .replace("@disabled_button_text_color", _get_disabled_button_text_color())
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
    def __init__(self, text):
        QtGui.QPushButton.__init__(self, text.upper())

        style_sheet = _get_stylesheet("flat_button.qss")
        self.setStyleSheet(style_sheet)


class Slider(QtGui.QSlider):
    # https://material.io/guidelines/components/sliders.html#sliders-continuous-slider
    # TODO implement Swatch color
    # TODO implement focus highlight
    # TODO implement zero value empty circle

    def __init__(self, *args):
        QtGui.QSlider.__init__(self, *args)

        style_sheet = _get_stylesheet("slider.qss")
        self.setStyleSheet(style_sheet)

    def mousePressEvent(self, event):
        QtGui.QSlider.mousePressEvent(self, event)
        self.repaint()  # forcing repaint, because the size of the handle changes, and Qt won't update the bounds

    def mouseReleaseEvent(self, event):
        QtGui.QSlider.mouseReleaseEvent(self, event)
        self.repaint()  # forcing repaint, because the size of the handle changes, and Qt won't update the bounds


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

    CLASS_TITLE = "title"
    CLASS_SUBTITLE = "subtitle"
    CLASS_SUPPORTING_TEXT = "supporting_text"

    DIRECTION_HORIZONTAL = 1
    DIRECTION_VERTICAL = 2

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        style_sheet = _get_stylesheet("card.qss")
        self.setStyleSheet(style_sheet)

        self.effect = MaterialShadowEffect(self.parent())
        self.setGraphicsEffect(self.effect)

        self._layout = QtGui.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

    def enterEvent(self, event):
        if self.isEnabled():
            self.effect.set_elevation(8)
        QtGui.QFrame.enterEvent(self, event)

    def leaveEvent(self, event):
        if self.isEnabled():
            self.effect.set_elevation(0)
        QtGui.QFrame.leaveEvent(self, event)

    def add_image(self, image):
        image_label = QtGui.QLabel()
        image_label.setPixmap(image)
        self._layout.addWidget(image_label)
        return image_label

    def add_title(self, title):
        title_label = QtGui.QLabel(title)
        title_label.setProperty(PROPERTY_CLASS, self.CLASS_TITLE)
        self._layout.addWidget(title_label)
        return title_label

    def add_subtitle(self, subtitle):
        subtitle_label = QtGui.QLabel(subtitle)
        subtitle_label.setProperty(PROPERTY_CLASS, self.CLASS_SUBTITLE)
        self._layout.addWidget(subtitle_label)
        return subtitle_label

    def add_supporting_text(self, supporting_text):
        supporting_text_label = QtGui.QLabel(supporting_text)
        supporting_text_label.setProperty(PROPERTY_CLASS, self.CLASS_SUPPORTING_TEXT)
        supporting_text_label.setWordWrap(True)
        self._layout.addWidget(supporting_text_label)
        return supporting_text_label

    def add_actions(self, actions, direction=DIRECTION_HORIZONTAL):
        if direction == self.DIRECTION_HORIZONTAL:
            button_layout = QtGui.QHBoxLayout()
        else:
            button_layout = QtGui.QVBoxLayout()

        self._layout.addLayout(button_layout)
        button_layout.setSpacing(8)
        button_layout.setContentsMargins(8, 8, 8, 8)

        for action in actions:
            if direction == self.DIRECTION_HORIZONTAL:
                button_layout.addWidget(action)
            else:
                row = QtGui.QHBoxLayout()
                row.addWidget(action)
                row.addStretch()
                button_layout.addLayout(row)

        if direction == self.DIRECTION_HORIZONTAL:
            button_layout.addStretch()


