import sys
from PyQt4 import QtGui, QtCore

import material
from material_shadow import MaterialShadowEffect
from shadow import CustomShadowEffect


class Example(material.MainWindow):
    def __init__(self):
        material.MainWindow.__init__(self)

        self._init_ui()
        self._create_menu()

    def _init_ui(self):
        tab = material.TabWidget()
        self.setCentralWidget(tab)

        tab.addTab(self._create_page1(), "Page1")
        tab.addTab(self._create_page2(), "Page2")
        tab.addTab(self._create_page3(), "Page3")
        tab.setCurrentIndex(2)

        self.setMinimumSize(800, 600)

    def _create_page1(self):
        main_layout = QtGui.QVBoxLayout()

        label = QtGui.QLabel("Tooltip here")
        label.setToolTip("This is a tooltip")
        main_layout.addWidget(label)

        dropdown_layout = QtGui.QHBoxLayout()
        main_layout.addLayout(dropdown_layout)
        dropdown = material.Dropdown()
        dropdown.addItems(["Option{}".format(i + 1) for i in xrange(10)])
        dropdown_layout.addWidget(dropdown)
        dropdown_layout.addStretch()

        main_layout.addWidget(QtGui.QCheckBox('CheckBox'))
        text_field1 = material.TextField('Sajtoskorte')
        text_field2 = material.TextField('Disabled')
        text_field2.setDisabled(True)
        main_layout.addWidget(text_field1)
        main_layout.addWidget(text_field2)

        w = QtGui.QWidget()
        main_layout.addWidget(w)
        w.setFixedSize(30, 50)
        w.setStyleSheet("border: 1px solid red;")
        effect = CustomShadowEffect(self)
        # effect.set_elevation(4)
        w.setGraphicsEffect(effect)

        w = QtGui.QWidget()
        main_layout.addWidget(w)
        w.setFixedSize(30, 50)
        w.setStyleSheet("border: 1px solid red;")
        effect = MaterialShadowEffect(self)
        effect.set_elevation(12)
        w.setGraphicsEffect(effect)

        main_layout.addStretch()

        button_layout = QtGui.QHBoxLayout()
        main_layout.addLayout(button_layout)

        button_layout.addStretch()
        button_layout.addWidget(material.RaisedButton('BUTTON1'))
        button2 = material.RaisedButton('BUTTON2')
        button2.setDisabled(True)
        button_layout.addWidget(button2)
        button_layout.addWidget(material.RaisedButton('BUTTON3'))

        button_layout = QtGui.QHBoxLayout()
        main_layout.addLayout(button_layout)

        button_layout.addStretch()
        button_layout.addWidget(material.FlatButton('FLAT1'))
        button2 = material.FlatButton('FLAT2')
        button2.setDisabled(True)
        button_layout.addWidget(button2)

        page = QtGui.QWidget()
        page.setLayout(main_layout)
        return page

    def _create_page2(self):
        main_layout = QtGui.QVBoxLayout()

        table = material.TableView()
        main_layout.addWidget(table)
        table.setModel(ExampleTableModel())

        page = QtGui.QWidget()
        page.setLayout(main_layout)
        return page

    def _create_page3(self):
        main_layout = QtGui.QVBoxLayout()

        card1 = material.Card()
        # card1.setFixedSize(200, 200)
        main_layout.addWidget(card1)

        card2 = material.Card()
        card2.setFixedSize(200, 200)
        main_layout.addWidget(card2)

        page = QtGui.QWidget()
        page.setLayout(main_layout)
        return page

    def _create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(QtGui.QAction('Option 1', self))
        file_menu.addAction(QtGui.QAction('Option 2', self))
        file_menu.addAction(QtGui.QAction('Option 3', self))

        sub_menu = file_menu.addMenu('Sub menu')
        sub_menu.addAction(QtGui.QAction('Sub Option 1', self))
        sub_menu.addAction(QtGui.QAction('Sub Option 2', self))
        sub_menu.addAction(QtGui.QAction('Sub Option 3', self))


class ExampleTableModel(QtCore.QAbstractTableModel):
    def rowCount(self, parent):
        return 5

    def columnCount(self, parent):
        return 4

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return "alma"


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont(r'd:\python_projects\material_test\Roboto\Roboto-Regular.ttf')
    app.setFont(QtGui.QFont("Roboto"))
    app.setProperty(material.PROPERTY_THEME, material.THEME_DARK)
    app.setProperty(material.PROPERTY_PRIMARY_COLOR, "#2196f3")
    app.setProperty(material.PROPERTY_SECONDARY_COLOR, "#68efad")

    win = Example()
    win.show()
    sys.exit(app.exec_())
