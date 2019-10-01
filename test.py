# from __future__ import division, print_function, absolute_import
# %matplotlib inline
import numpy as np

from phidl import Device, Layer, LayerSet, make_device
from phidl import quickplot as qp # Rename "quickplot()" to the easier "qp()"
import phidl.geometry as pg
import phidl.routing as pr
import phidl.utilities as pu

# import customed geolib
import mine as mn
import matplotlib.pyplot as plt


# create trenches to test etching rate
D = Device('trench')

w_l = [0.2,0.3,0.4,0.6,1,2,5,10]

mx = 0
for i in range(len(w_l)):
    mx += (w_l[i] + 5)
#     print(mx)
    D << mn.waveguide(width=w_l[i],length=15e3, layer=1).movey(mx)

qp(D)
# plt.show()
