from openalea.mtg.data import data_dir as data
import openalea.mtg
from openalea.mtg import *


g = MTG(data/'noylum2.mtg')

dressing_data = dresser.DressingData(DiameterUnit=10)
pf = PlantFrame(g,TopDiameter='TopDia',DressingData = dressing_data)

world['lpy_scene'] = pf.plot(gc=True, display=False)

def init():
    if 'lpy_scene' in world:
        del world['lpy_scene']

