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
D = Device('CJC')
LB_CEL = Device('LB_CEL')

def asymMRR(width_rg=1, width_bus=1, radius=30, gap=0.1,lenL=10,lenR=10):
    D = Device('MRRBUS')
    RG = D << pg.ring(radius=radius,width=width_rg, angle_resolution=.1)
    BUS = D << mn.waveguide(length=2*radius+lenL+lenR+width_rg,
                            width=width_bus).movex(-radius-(width_rg)/2-lenL)
    # align ring & bus, rotate
    BUS.ymax = RG.ymin - gap
    D.add_port(name = 1, midpoint = [D.xmax,D.ymin+width_bus/2], 
               width = width_bus, orientation = 0)
    D.add_port(name = 2, midpoint = [D.xmin,D.ymin+width_bus/2], 
               width = width_bus, orientation = 180)
    return D
w = 1.5 # width of
wBus = 1.5
wRg = w
# wTp = 0.2

devLen = 10000
rRg = 100

HD = 4*rRg
VD = rRg*.8
num = 8 # num of MRR

gapPeriod = .05
offset = devLen/2 - num*HD/2
# margin = 100

for i in range(num):
    gap = gapPeriod*i+0.1
    MRR = D << asymMRR(width_bus=wBus,
                       width_rg=wRg,radius=rRg, 
                       gap=gap,
                       lenL=i*HD+i*rRg,
                       lenR=0).move((offset+HD*i,-VD*i))
    LB_CEL << pg.text(text='GAP%d' % (1e3*gap), layer=2, justify='right').move((offset+HD*i,-VD*i))
    TPCL = D << pg.connector((0,rRg-VD*i),width=wBus)
    TPCR = D << pg.connector((devLen,rRg-VD*i),width=wBus)
#     MIDL = D << pg.connector((MRR.xmin-margin,(MRR.ymin+rRg)),width=wBus)
    RT1 = D << pr.route_manhattan(port1=TPCL.ports[1],port2=MRR.ports[2],
                                  bendType='circular',radius=rRg)
    RT2 = D << pr.route_manhattan(port1=TPCR.ports[2],port2=MRR.ports[1],
                                  bendType='circular',radius=rRg)

mark = [pg.rectangle((100,100), layer=2).move((300*i,-(num)*VD)) for i in range(5)]
mark2 = [pg.rectangle((100,100), layer=2).move((devLen-300*i-100,-(num)*VD)) for i in range(5)]

bar =  mn.waveguide(length=devLen,width=wBus).move((0,-(num+1)*VD))
for i in range(3):
    D << pg.copy(bar).movey(-i*VD)
    
D_out = pg.outline(D, distance=10, layer=1)

for i in (D, D_out):
    i << LB_CEL
    i << tuple(mark)
    i << tuple(mark2)

D.rotate(90)
D_out.flatten().write_gds('190807-nanofab-mrr-nega.gds')
D.flatten().write_gds('190807-nanofab-mrr-posi.gds')