
import weakref
from qtpy import QtGui, QtCore, QtWidgets


class WidgetSwitcher(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)
        self._previous = None

        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        p = QtWidgets.QSizePolicy

    def set_widget(self, widget_class, *args, **kwargs):
        """
        This method switch attribute dele
        """
        if self._previous:
            previous = self._previous()
            self._layout.removeWidget(previous)
            previous.setParent(None)
            previous.close()
            self._previous = None
            del previous

        widget = widget_class(*args, **kwargs)
        p = QtWidgets.QSizePolicy
        widget.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))
        widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self._layout.addWidget(widget)
        self._previous = weakref.ref(widget)
