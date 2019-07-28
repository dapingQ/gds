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

def z_shape(width=1.5, radius=50, mid=50, left=100, right=100, layer=0):
    D = Device('z_shape')
    LW = D << mn.waveguide(width=width,length=left,layer=layer)
    BD1 = D << pg.turn(port=LW.ports[2],angle=90,radius=radius,angle_resolution=0.5)
    MD = D << mn.extend(port=BD1.ports[2],length=mid)
    BD2 = D << pg.turn(port=MD.ports[2],angle=-90,radius=radius,angle_resolution=0.5)
    RW = D << mn.extend(port=BD2.ports[2],length=right)
    return D

PD = 1e3
num = 5

w = 1.7
width_bus = w
width_rg = w

ext = 2.5e3
rad = 200
SD = 30

LB_CEL = Device('LB_CEL')
for i in range(num):
    gap = 0.20 + i*0.05
    RG_CEL = Device('RG_CEL')
    RG = RG_CEL << pg.ring(radius=rad,width=width_rg)
    BUS =RG_CEL << mn.waveguide(length=rad,width=width_bus).movex(-.5*rad)
    RG.ymin = BUS.ymax + gap
    RG_CEL.rotate(90).move((PD*i,-SD*i))
    LB_CEL << pg.text(text='GAP%d' % (1e3*gap),position=(-rad+PD*i,-SD*i),layer=1)
    CN1 = pg.connector((7e3,BUS.ymax+rad),width=width_bus)
    RT1 = RG_CEL << pr.route_manhattan(port1=CN1.ports[2],port2=BUS.ports[2],bendType='circular',radius=rad)
    CN2 = pg.connector((-(i+10)*SD,BUS.ymin-rad),width=width_bus)
    RT2 = RG_CEL << pr.route_manhattan(port1=CN2.ports[1],port2=BUS.ports[1],bendType='circular',radius=rad)
    CN3 = pg.connector((-3e3,BUS.ymax+rad),width=width_bus)
    RT3 = RG_CEL << pr.route_manhattan(port1=CN3.ports[1],port2=CN2.ports[2],bendType='circular',radius=rad)
    D << RG_CEL

bar =  mn.waveguide(length=10e3,width=width_bus).move((-3e3,-550))
for i in range(3):
    D << pg.copy(bar).movey(i*SD)
    
D_out = pg.outline(D.flatten(),distance=8,layer=1)
D_out << LB_CEL
# D_out << pg.copy(D_out).movey(2e3)   
# D_out << pg.copy(D_out).movey(1e3)
D_out.flatten().write_gds('./0417/180416_ring_array_%d.gds' % (1e3*width_rg))

# qp(D_out)