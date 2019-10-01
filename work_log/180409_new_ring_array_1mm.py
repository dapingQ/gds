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
gap = 0.05
num = 5
width_bus = 1.5
width_rg = 1.5
ext = 2.5e3
rad = 200
SD = 30
# BD=
# RG=[]
for i in range(num):
    im = 50+num*SD
    RG = D << pg.ring(radius=rad,width=width_rg).movey(rad+im/2-50)
    BD = D << z_shape(width=width_bus, radius=rad, mid=im, left=ext+PD*(i+1),right=ext+PD*(num-i)).movey(-SD*i)
    RG.xmax = (BD.xmin+BD.xmax)/2 + PD*(i-2) - width_bus*.5 - (0.2 +gap*i)
#     RG.move((ext,0))

bar =  mn.waveguide(length=11.4e3,width=1.5).movey(650)
for i in range(3):
    D << pg.copy(bar).movey(i*SD)
    
D_out = pg.outline(D.flatten(),distance=8,layer=2)
for i in range(num):
    D_out << pg.text('GAP %s' % (200+50*i), size = 15, justify = 'center',layer=2).move((ext+PD*(i+1),205))

# D_out << pg.copy(D_out).movey(2e3)   
# D_out << pg.copy(D_out).movey(1e3)
D_out.flatten().write_gds('180409_new_ring_array_1mm.gds')

# qp(D_out)