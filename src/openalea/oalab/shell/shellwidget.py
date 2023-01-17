from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager
from .streamredirection import GraphicalStreamRedirection


class ShellWidget(RichJupyterWidget, GraphicalStreamRedirection):

    """
    ShellWidget is an IPython shell.
    """


    def __init__(self, interpreter=None, message="", log='', parent=None):
        """
        :param interpreter : InteractiveInterpreter in which
        the code will be executed

        :param message: welcome message string

        :param  parent: specifies the parent widget.
        If no parent widget has been specified, it is possible to
        exit the interpreter by Ctrl-D.
        """
        RichJupyterWidget.__init__(self, parent)

        if interpreter is None:
            from openalea.core.service.ipython import interpreter
            interpreter = interpreter()
        # Set interpreter
        self.interpreter = interpreter


        # Set kernel manager
        km = QtInProcessKernelManager()
        km.start_kernel(show_banner=False)
        self.kernel_manager = km


        #km.kernel = self.interpreter
        #km.kernel.gui = 'qt4'

        self.kernel = self.kernel_manager.kernel
        self.kernel.gui = 'qt'
        #self.interpreter = self.kernel

        self.shell = self.kernel.shell

        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()

        self.kernel.locals = self.kernel.shell.user_ns

        # For Debug Only
        # self.interpreter.locals['shell'] = self

        # Compatibility with visualea
        self.runsource = self.interpreter.run_cell
        self.runcode = self.interpreter.runcode
        self.loadcode = self.interpreter.loadcode

        # Write welcome message
        self.interpreter.widget = self
        #self.write(message)
        # Multiple Stream Redirection
        GraphicalStreamRedirection.__init__(self, self.kernel.stdout, self.kernel.stderr)

    def read(self, *args, **kwargs):
        self.kernel_client.stdin_channel.input(*args, **kwargs)

    def readline(self, size=None):
        from openalea.oalab.utils import raw_input_dialog
        txt = raw_input_dialog()
        self.write(str(txt))
        return txt

    def get_interpreter(self):
        """
        :return: the interpreter object
        """
        return self

    def write(self, txt):
        """
        Write a text in the stdout of the shell and flush it.
        :param txt: String to write.
        """
        self.shell.write(str(txt))
        #self.interpreter.stdout.flush()

    def push(self, var):
        """
        Push variables in the namespace.
        :param var: dict of objects
        """
        if var is not None:
            for v in var:
                self.interpreter.locals += v

    def initialize(self):
        if not hasattr(self.interpreter, "shell"):
            self.interpreter.shell = self.interpreter
        if hasattr(self.interpreter.shell, "events"):
            self.interpreter.shell.events.register("post_execute", self.add_to_history)
        else:
            print("You need ipython >= 2.0 to use history.")

    def add_to_history(self, *args, **kwargs):
        """
        Send the last sent of history to the components that display history
        """
        from openalea.oalab.service.history import display_history
        records = self.interpreter.shell.history_manager.get_range()

        input_ = ''
        # loop all elements in iterator to get last one.
        # TODO: search method returning directly last input
        for session, line, input_ in records:
            pass
        display_history(input_)


def main():
    from openalea.vpltk.qt import QtGui
    import sys

    app = QtGui.QApplication(sys.argv)

    from openalea.core.service.ipython import interpreter
    interpreter = interpreter()

    interpreter.user_ns['interp'] = interpreter
    # Set Shell Widget
    shellwdgt = ShellWidget(interpreter=interpreter)
    interpreter.user_ns['shell'] = shellwdgt

    mainWindow = QtGui.QMainWindow()
    mainWindow.setCentralWidget(shellwdgt)
    mainWindow.show()

    app.exec_()


if(__name__ == "__main__"):
    main()
