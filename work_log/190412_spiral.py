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

def semi_spiral(bend=20,shift=10,width=1,layer=1, n=4, angle_resolution=1):
    D = Device('semi_spiral')
    inn = pg.arc(radius=(2*bend-shift)/4,start_angle=0,theta=180,width=width).rotate(180).movex(-(2*bend-shift)/4)
    D << pg.copy(inn).rotate(180)
    D << inn
    for i in range(n):
#         radius = bend + i*shift
        out = pg.arc(radius=bend+shift*i,start_angle=0,theta=180,width=width).movex(shift/2)
        D << out
    for i in range(n):
        out = pg.arc(radius=bend+shift*i,start_angle=180,theta=180,width=width).movex(-shift/2)
        D << out
    WG = mn.waveguide(length=bend+shift*n,width=width).rotate(90).movex(-bend-shift*n+shift/2)
    D << WG
    D << pg.copy(WG).rotate(180)
    D.add_port(name = 1, midpoint = [D.xmin+width/2,D.ymax], width = width, orientation = 90)
    D.add_port(name = 2, midpoint = [-D.xmin-width/2,-D.ymax], width = width, orientation = 270)
    return D.rotate(90)

D = Device('SEMI')

width = 1.5
for i in range(4):
    SS = D << semi_spiral(bend=430,shift=50,width=width,layer=1, n=i).move((2e3*i,-90*i))
    D << mn.extend(port=SS.ports[2],length=10e3-2e3*i)
    D << mn.extend(port=SS.ports[1],length=4e3+2e3*i)

pg.outline(D,distance=10).flatten().write_gds('190412_spiral.gds')
qp(D)
D.area()/2.5