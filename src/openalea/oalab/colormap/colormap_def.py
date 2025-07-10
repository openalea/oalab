# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Cerutti <guillaume.cerutti@inria.fr>
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       TissueLab Website : http://virtualplants.github.io/
#
###############################################################################

from openalea.core.path import path as Path
from openalea.oalab.resources import resources_dir
import os

def list_colormaps():
    colormap_names = []
    f = resources_dir/'colormaps'/'grey.lut'
    f = os.path.expandvars(f)
    colormaps_path = Path(f).parent

    for colormap_file in colormaps_path.walkfiles('*.lut'):
        colormap_name = str(colormap_file.name[:-4])
        colormap_names.append(colormap_name)
    colormap_names.sort()
    return colormap_names


def load_colormaps():
    from openalea.oalab.colormap.colormap_utils import Colormap, colormap_from_file
    colormaps = {}
    f = resources_dir/'colormaps'/'grey.lut'
    f = os.path.expandvars(f)
    colormaps_path = Path(f).parent

    for colormap_file in colormaps_path.walkfiles('*.lut'):
        colormap_name = str(colormap_file.name[:-4])
        colormaps[colormap_name] = colormap_from_file(
            colormap_file, name=colormap_name)
    return colormaps
