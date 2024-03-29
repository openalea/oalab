
import weakref
from qtpy import QtGui, QtCore, QtWidgets

from openalea.core.service.interface import interface_label
from openalea.oalab.service.qt_control import qt_widget_plugins
from openalea.core.control import Control
from openalea.deploy.shared_data import shared_data
import openalea.oalab


class QtControlEditor(QtWidgets.QWidget):

    def __init__(self, control=None):
        QtWidgets.QWidget.__init__(self)
        self.set_control(control)

        self._layout = QtWidgets.QVBoxLayout(self)
        self._qt_editor = None

    def set_control(self, control=None):
        self._control = control


def widget_label(widget):
    if hasattr(widget, 'label'):
        return widget.label
    elif hasattr(widget, 'name'):
        return str(widget.name)
    else:
        return str(widget)

from openalea.visualea.qt.designer import generate_pyfile_from_uifile
generate_pyfile_from_uifile(__name__)
from openalea.oalab.control.designer._editor import Ui_ControlEditor


class ControlEditor(QtWidgets.QWidget, Ui_ControlEditor):
    counters = {}

    def __init__(self, name='default'):
        QtWidgets.QWidget.__init__(self)
        Ui_ControlEditor.__init__(self)
        self.setupUi(self)

        self._interfaces = []
        self._constraints = None

        self.cb_preview.setChecked(False)
        self.box_preview.setVisible(False)

        self.e_name.setText(name)
        self._autoname = True
        self.e_name.textEdited.connect(self.on_user_edit)

        self.tooltips = {}

        self.label_to_iname = {}

        self.label_to_wname = {}
        self.widget_to_label = {}

        plugins = qt_widget_plugins()
        for iname in plugins:
            label = interface_label(iname)
            self.label_to_iname[label] = iname
            self.tooltips[iname] = '<b>%s</b><br />Interface name:%s' % (label, iname)

        for label in sorted(self.label_to_iname):
            iname = self.label_to_iname[label]
            self._interfaces.append(iname)
            tooltip = self.tooltips[iname]

            item = QtGui.QListWidgetItem(label)
            item.setToolTip(tooltip)
            item.setStatusTip(tooltip)

            self.cb_interface.addItem(label)

        self.cb_interface.currentIndexChanged.connect(self.refresh)
        self.cb_widget.currentIndexChanged.connect(self.on_widget_changed)

        self.refresh()

    def on_user_edit(self):
        self._autoname = False

    def on_widget_changed(self):
        widget = None
        if self.cb_widget.currentIndex() == -1:
            return
        widget_name = self.widget_plugins[self.cb_widget.currentIndex()].name
        iname = self._interfaces[self.cb_interface.currentIndex()]

        icon_path = None
        for plugin in qt_widget_plugins(iname):
            if widget_name == plugin.name:
                widget = plugin.implementation
                if hasattr(plugin, 'icon_path'):
                    icon_path = plugin.icon_path
                    if icon_path and not icon_path.exists():
                        icon_path = None
                else:
                    icon_path = None
                if icon_path is None:
                    icon_path = shared_data(openalea.oalab, 'icons/preview_%s.png' % iname)
                    if icon_path and not icon_path.exists():
                        icon_path = None
                break

        if icon_path:
            pixmap = QtGui.QPixmap(icon_path)
            if pixmap.width() >= 400 or pixmap.height() >= 400:
                pixmap = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
            self.widget_preview.setPixmap(pixmap)
            self.l_widget.setToolTip('<b>%s</b><br /><img src="%s" width="200" />' % (widget_label(plugin), icon_path))
        else:
            self.widget_preview.setText("No preview")

        if self._constraints:
            widget_constraints = self._constraints()
            self._layout_constraints.removeWidget(widget_constraints)
            widget_constraints.close()
            self._constraints = None
#             self.l_constraints.hide()

        if widget and hasattr(widget, 'edit_constraints'):
            widget_constraints = widget.edit_constraints()
            widget_constraints.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self._layout_constraints.addWidget(widget_constraints)
#             self.l_constraints.show()

            self._constraints = weakref.ref(widget_constraints)

    def refresh(self):
        iname = self._interfaces[self.cb_interface.currentIndex()]
        if self._autoname:
            i = self.__class__.counters.setdefault(iname, 0)
            self.e_name.setText('%s_%d' % (iname[1:].lower(), i))
        self.l_type.setToolTip(self.tooltips[iname])

        self.cb_widget.clear()
        self.widget_plugins = []

        self.label_to_wname = {}

        editors = qt_widget_plugins(iname)
        for widget in editors:
            self.widget_plugins.append(widget)
            label = widget_label(widget)
            self.label_to_wname[label] = widget.name
            self.cb_widget.addItem(label)

    def control(self):
        iname = self._interfaces[self.cb_interface.currentIndex()]
        control = Control(self.e_name.text(), iname,
                          widget=self.label_to_wname[self.cb_widget.currentText()],
                          constraints=self.constraints())
        self.__class__.counters[iname] = self.__class__.counters.setdefault(iname, 0) + 1
        return control

    def constraints(self):
        if self._constraints:
            return self._constraints().constraints()
        else:
            return {}
