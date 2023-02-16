# -*- coding: utf-8 -*-
# -*- python -*-
#
#       Copyright © 2011 Pierre Raybaut
#       Copyright © 2012-2013 pyLot - andheo
#       Copyright © 2015 INRIA - CIRAD - INRA
#
#       File author(s): Pierre Raybaut
#
#       File contributor(s): Guillaume Baty
#           Christophe Pradal
#
#       Licensed under the terms of the MIT License
#       (see spyderlib/__init__.py for details)
#       Spyderlib WebSite : https://github.com/spyder-ide/spyder
#
###############################################################################

"""
spyderlib.qt.compat
-------------------

Transitional module providing compatibility functions intended to help
migrating from PyQt to PySide.

This module should be fully compatible with:
    * PyQt >=v4.4
    * both PyQt API #1 and API #2
    * PySide
"""

import os
import sys
from qtpy import PYQT5_API, PYQT6_API, PYSIDE2_API, PYSIDE6_API, QT_API, QtCore
from qtpy.QtWidgets import QFileDialog, QTabWidget

try:
    from openalea.core.path import path as Path
except ImportError:
    FilePath = DirPath = Path = str
else:
    FilePath = DirPath = Path

# I think this is valid for PyQt and PySide according to doc
_tab_position = {
    0: QTabWidget.North,
    1: QTabWidget.South,
    2: QTabWidget.West,
    3: QTabWidget.East,
}
# if os.environ[QT_API] in [PYQT5_API, PYQT6_API]:
#     _tab_position = {
#         0: QTabWidget.North,
#         1: QTabWidget.South,
#         2: QTabWidget.West,
#         3: QTabWidget.East,
#     }
# elif os.environ[QT_API] in [PYSIDE2_API, PYSIDE6_API]:
#     _tab_position = {
#         0: QTabWidget.TabPosition.North,
#         1: QTabWidget.TabPosition.South,
#         2: QTabWidget.TabPosition.West,
#         3: QTabWidget.TabPosition.East,
#     }
#     for idx, position in _tab_position.items():
#         setattr(QTabWidget, position.name, position)


def arrange_path(path, path_class=Path):
    """
    Return a Path, FilePath or DirPath dependings on path nature.
    Path is used for special path like device "files" or path not existing on disk.
    If path is empty, returns None.

    If path do not exist on disk or is not file nor directory
    (like /dev/xyz on linux),it returns a path_class.
    """
    if not path:
        return None
    path = Path(str(path))
    if path.isfile():
        return FilePath(path)
    elif path.isdir():
        return DirPath(path)
    else:
        return path_class(path)

def getexistingdirectory(parent=None, caption='', basedir='',
                         options=None):
    """Wrapper around QtGui.QFileDialog.getExistingDirectory static method
    Compatible with PyQt >=v4.4 (API #1 and #2) and PySide >=v1.0"""
    if options is None:
        options = QFileDialog.ShowDirsOnly

    # Calling QFileDialog static method
    if sys.platform == "win32":
        # On Windows platforms: redirect standard outputs
        _temp1, _temp2 = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = None, None
    try:
        result = QFileDialog.getExistingDirectory(parent, caption, basedir,
                                                  options)
    finally:
        if sys.platform == "win32":
            # On Windows platforms: restore standard outputs
            sys.stdout, sys.stderr = _temp1, _temp2
    if not isinstance(result, str):
        # PyQt API #1
        result = arrange_path(result, path_class=Path)
    return result


def _qfiledialog_wrapper(attr, parent = None, caption = '', basedir = '',
                         filters = '', selectedfilter = '', options = None):
    # from the last https://github.com/spyder-ide/qtpy/blob/master/qtpy/compat.py
    # without PyQt4
    if options is None:
        options = QFileDialog.Option(0)

    func = getattr(QFileDialog, attr)

    # Calling QFileDialog static method
    if sys.platform == "win32":
        # On Windows platforms: redirect standard outputs
        _temp1, _temp2 = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = None, None
    result = func(parent, caption, basedir, filters, selectedfilter, options)
    if sys.platform == "win32":
        # On Windows platforms: restore standard outputs
        sys.stdout, sys.stderr = _temp1, _temp2

    output, selectedfilter = result

    # Always returns the tuple (output, selectedfilter)
    return output, selectedfilter


def getopenfilename(parent=None, caption='', basedir='', filters='',
                    selectedfilter='', options=None):
    """Wrapper around QtGui.QFileDialog.getOpenFileName static method
    Returns a tuple (filename, selectedfilter) -- when dialog box is canceled,
    returns a tuple of empty strings
    Compatible with PyQt >=v4.4 (API #1 and #2) and PySide >=v1.0"""
    return _qfiledialog_wrapper('getOpenFileName', parent=parent,
                                caption=caption, basedir=basedir,
                                filters=filters, selectedfilter=selectedfilter,
                                options=options, path_class=FilePath)


def getopenfilenames(parent=None, caption='', basedir='', filters='',
                     selectedfilter='', options=None):
    """Wrapper around QtGui.QFileDialog.getOpenFileNames static method
    Returns a tuple (filenames, selectedfilter) -- when dialog box is canceled,
    returns a tuple (empty list, empty string)
    Compatible with PyQt >=v4.4 (API #1 and #2) and PySide >=v1.0"""
    return _qfiledialog_wrapper('getOpenFileNames', parent=parent,
                                caption=caption, basedir=basedir,
                                filters=filters, selectedfilter=selectedfilter,
                                options=options, path_class=FilePath)


def getsavefilename(parent=None, caption='', basedir='', filters='',
                    selectedfilter='', options=None):
    """Wrapper around QtGui.QFileDialog.getSaveFileName static method
    Returns a tuple (filename, selectedfilter) -- when dialog box is canceled,
    returns a tuple of empty strings
    Compatible with PyQt >=v4.4 (API #1 and #2) and PySide >=v1.0"""
    return _qfiledialog_wrapper('getSaveFileName', parent=parent,
                                caption=caption, basedir=basedir,
                                filters=filters, selectedfilter=selectedfilter,
                                options=options, path_class=FilePath)


def tabposition_qt(value):
    if isinstance(value, int):
        return _tab_position[value]
    else:
        return value


def tabposition_int(value):
    if isinstance(value, int):
        return value
    else:
        for idx, pos in list(_tab_position.items()):
            if pos == value:
                return idx


def orientation_qt(value):
    if value == 1:
        return QtCore.Qt.Horizontal
    elif value == 2:
        return QtCore.Qt.Vertical
    else:
        return value


def orientation_int(value):
    if isinstance(value, int):
        return value
    else:
        if value == QtCore.Qt.Horizontal:
            return 1
        elif value == QtCore.Qt.Vertical:
            return 2
        else:
            return 0
