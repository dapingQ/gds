from __future__ import division, print_function, absolute_import
import numpy as np

from phidl import Device, Layer, LayerSet, make_device
from phidl import quickplot as qp # Rename "quickplot()" to the easier "qp()"
import phidl.geometry as pg
import phidl.routing as pr
import phidl.utilities as pu

# import customed geolib
import mine as mn
import matplotlib.pyplot as plt

wgL = 8e3 # mm
wgW = 1
rgW = 1.5
rgR = 200

D = Device()

gap = np.arange(6)*0.05+0.2

WG1 = D << mn.waveguide(length=wgL, width=wgW)
WG2 = D << mn.waveguide(length=wgL, width=wgW).movey(450)
WG3 = D << mn.waveguide(length=wgL, width=wgW).movey(500)
WG4 = D << mn.waveguide(length=wgL, width=wgW).movey(950)

RG = pg.ring(rgR, rgW)
RG.ymin = WG1.ymax + gap[0]
RG.movex(4e3)
D << RG

RG = pg.ring(rgR, rgW).movex(450)
RG.ymax = WG2.ymin - gap[1]
RG.movex(4e3)
D << RG

RG = pg.ring(rgR, rgW)
RG.ymin = WG3.ymax + gap[2]
RG.movex(4e3)
D << RG

RG = pg.ring(rgR, rgW).movex(450)
RG.ymax = WG4.ymin - gap[3]
RG.movex(4e3)
D << RG

D.flatten()
qp(D)

D_out = pg.outline(D, distance = 14)
# D.write_gds('view.gds')
D_out.write_gds('view_out.gds')
