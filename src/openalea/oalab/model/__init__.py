"""
Quick Start
===========

Here we suppose that we have a model named *sum_int* that do the sum between two integers. The classical use of this model is:

  - Get the project **(not necessary if you are working inside OpenAleaLab)**:
      >>> from openalea.core.project import ProjectManager
      >>> from openalea.oalab.data import data_dir as oalab_dir
      >>> from openalea import oalab
      >>> pm = ProjectManager()
      >>> pm.discover()
      >>> proj = pm.load("sum", oalab_dir)

"""