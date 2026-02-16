"""Configuration file""" 

__license__ = "Cecill-C"
__revision__ = " $Id: $"


def get_version():

    from importlib.metadata import metadata
    meta = metadata("openalea.oalab")
    release = meta.get("version")
    
    return release

url = "http://openalea.rtfd.io"

def get_copyright():

    return "Copyright \xa9 2014-2026 inria/CIRAD/INRAE\n"
