def has_ipython():
    """
    Check if User can use IPython shell embeded in OpenAlea.

    Check only IPython without is dependencies(zmq, pygments)

    :return: True if user can use IPython. Else False.
    """
    if has_new_ipython():
        return True
    else:
        return has_deprecated_ipython()

def has_deprecated_ipython():
    """
    Check if User can has IPython 1.0dev deprecated.

    :return: True if user can use IPython. Else False.
    """
    try:
        from IPython.kernel.inprocess.ipkernel import InProcessKernel
        from IPython.frontend.qt.console.rich_ipython_widget import RichIPythonWidget
        from IPython.frontend.qt.inprocess_kernelmanager import QtInProcessKernelManager
        return True
    except ImportError:
        return False


def has_new_ipython():
    """
    Check if User can has IPython 1.0dev not deprecated.

    :return: True if user can use IPython. Else False.
    """
    try:
        from ipykernel.inprocess import InProcessKernelClient
        from qtconsole.rich_jupyter_widget import RichJupyterWidget
        from qtconsole.inprocess import QtInProcessKernelManager
        return True
    except ImportError:
        return False
