

from qtpy import QtGui
from openalea.core.control.manager import ControlManager
from openalea.oalab.control.manager import ControlManagerWidget
from openalea.oalab.control.panel import ControlPanel
from openalea.core.service.control import new_control
from openalea.core.service.interface import interface_names, get_interface
from openalea.oalab.service import qt_control


def test_all_lpy_controls():
    from openalea.plantlab.lpycontrol import import_lpy_controls
    from openalea.deploy.shared_data import shared_data
    import openalea.lpy
    lpydir = shared_data(openalea.lpy.__path__, share_path='share/tutorial')
    for lpypath in lpydir.walkfiles('*.lpy'):
        import_lpy_controls(lpypath)


def test_all_interfaces():
    # Fill al
    for iname in interface_names():
        print(iname)
        for i, editor in enumerate(qt_control.qt_widget_plugins(iname)):
            print('  -', editor.name)
            name = editor.name.replace('Plugin', 'P.').replace('Widget', 'W.')
            name = '%s_%s' % (iname, name)
            c = new_control(name, iname)
#             cc1.add_control(c)


def sample_controls():
    cm = ControlManager()
#     cc1 = ControlContainer()
#     cc2 = ControlContainer()

    cmw = ControlManagerWidget()
#     cmw.model.set_manager(cc2)
    cp = ControlPanel()

    percent = get_interface('IInt', min=0, max=100)
    c = new_control('i', percent)
#     cc2.add_control(c)

    c = new_control('f', 'IFloat')
    cm.add_control(c)


def disp_controls():
    cm = ControlManager()
    import sys
    for k, v in list(cm.namespace().items()):
        print(k, v, file=sys.__stdout__)


if __name__ == '__main__':

    from openalea.oalab.testing.applet import TestMainWin
    instance = QtWidgets.QApplication.instance()

    if instance is None:
        app = QtWidgets.QApplication([])
    else:
        app = instance

    tests = [
        test_all_interfaces,
        test_all_lpy_controls,
        disp_controls,
        sample_controls
    ]

    layout = dict(children={0: [1, 2]},
                  parents={0: None, 1: 0, 2: 0},
                  properties={0: {'amount': 0.5, 'splitDirection': 1},
                              1: {'widget': {'applets': [{'name': 'ControlManager'}]}},
                              2: {'widget': {'applets': [{'name': 'ShellWidget'}]}},
                              }
                  )
    mw = TestMainWin(default_layout=layout, tests=tests,
                     layout_file='.test_control_manager.lay')

    mw.resize(1024, 768)
    mw.show()

    mw.initialize()

    if instance is None:
        app.exec_()
