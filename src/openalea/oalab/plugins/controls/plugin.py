
class ControlWidgetPlugin():
    controls = []
    name = 'ControlWidget'
    icon_path = None

    edit_shape = [] # ['large', 'line', 'small']
    view_shape = [] # ['large', 'line', 'small']
    create_shape = [] # ['large', 'line', 'small']
    paint = False

    @classmethod
    def load(cls):
        raise NotImplementedError

