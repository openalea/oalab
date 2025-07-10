
from openalea.core.plugin import PluginDef
import os

@PluginDef
class Tutorial(object):
    implement = "ProjectRepositoryList"
    label = "OpenAleaLab examples"

    def __call__(self):
        from openalea.core.path import path
        try:
            from openalea import oalab
            from openalea.oalab.data import data_dir
        except ImportError:
            return []
        else:
            f = os.path.expandvars(data_dir)
            return [path(f)]
