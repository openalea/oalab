from openalea.core.service.control import new_control

from openalea.core.interface import IInt

minterface = IInt(min=1, max=30, step=1)
mcontrol = new_control('step',minterface,15)

from openalea.core.interface import IStr

minterface = IStr()
mcontrol = new_control('x_label',minterface,'$x^2$')

minterface = IInt(min=1, max=50, step=1)
mcontrol = new_control('nb_step',minterface,10)

minterface = IStr()
mcontrol = new_control('y_label',minterface,'y_label')

minterface = IInt(min=1, max=10, step=1)
mcontrol = new_control('a',minterface,2)

minterface = IInt(min=1, max=100, step=10)
mcontrol = new_control('b',minterface,20)

