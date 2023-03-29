import numpy as np

from phidl import Device, Layer, LayerSet, make_device
# from phidl import quickplot as qp # Rename "quickplot()" to the easier "qp()"
# import phidl.geometry as pg
# import phidl.routing as pr
# import phidl.utilities as pu

# import customed geolib
# import photonic as mn
import photonic as ph
import matplotlib.pyplot as plt

D = Device('tets')

D << ph.archimedes(angle_resolution=.5)

D.flatten().write_gds('view.gds')