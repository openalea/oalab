from openalea.core.control import Control

controls = []
from openalea.core.interface import IBool

minterface = IBool()
mcontrol = Control('FLAKE', minterface, True)
controls.append(mcontrol)

