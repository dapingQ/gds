from __future__ import division, print_function, absolute_import
import numpy as np

from phidl import Device, Layer, LayerSet, make_device
from phidl import quickplot as qp # Rename "quickplot()" to the easier "qp()"
import phidl.geometry as pg
import phidl.routing as pr
import phidl.utilities as pu

# import customed geolib
import mine as mn

# waveguide: 1st para is length, second is width
# def waveguide(width = 10, height = 1):
#     WG = Device('waveguide')
#     WG.add_polygon( [(0, 0), (width, 0), (width, height), (0, height)] )
#     WG.add_port(name = 'wgport1', midpoint = [0,height/2], width = height, orientation = 180)
#     WG.add_port(name = 'wgport2', midpoint = [width,height/2], width = height, orientation = 0)
#     return WG

wgL = 20e3 # mmw
wgW = 1.5
rgR = 200
cldW = 10

args = {'layer':3}

# def BMRR(dis = 20, gap = 0.0, width = 1.5):
#     # dis: distance of ports
#     # gap is same for two bus 
#     rgR = dis - gap - width 
#     lc = 10*dis
    
#     D = Device('BMRR')
#     # bus waveguide
#     D << mn.racetrack(radius = dis/2, width = width, lc = lc).movey(-1.5*dis)
#     D << mn.racetrack(radius = dis/2, width = width, lc = lc).movey(1.5*dis)
#     # resonators
#     D << pg.ring(radius=rgR,width=width).movex(4*dis)
#     D << mn.racetrack(radius=rgR,width=width, lc=10).movex(-4*dis)
#     return D

OUT = Device()

WG = mn.waveguide(length=wgL, width=wgW, **args)
RG = pg.ring(rgR, wgW, **args)
RT1 = mn.racetrack(rgR, wgW,10, **args)
RT2 = mn.racetrack(rgR, wgW,15, **args)
# RT3 = mn.racetrack(rgR, wgW,20)
RT3 = mn.slot_ring(rgR, CGS=[1.3,0.1,0.2],**args)

gap_list = np.arange(0.1,0.4,0.05)

shift = 4e3

for i in range(len(gap_list)):
    D = Device('Inner')

    wg = D << WG
    rg = D << RG
    rt1 = D << RT1
    rt2 = D << RT2
    rt3 = D << RT3
    
    gap = gap_list[i]
    
    rg.ymin = gap+wgW
    rg.movex(shift)
    
    rt1.ymin = gap+wgW
    rt1.movex(shift*2) 
    
    rt2.ymin = gap+wgW
    rt2.movex(shift*3) 
    
    rt3.ymin = gap+wgW
    rt3.movex(shift*4) 
    
    
    # find outline
    D_out = pg.outline(D, distance = cldW)
    
    LB_rg = pg.text('GAP %s' % int(gap*1000), size = 15, justify = 'center').move([shift,100])
    LB1 = pg.text('LC 10 GAP %s' % int(gap*1000), size = 15, justify = 'center').move([shift*2,100])
    LB2 = pg.text('LC 15 GAP %s' % int(gap*1000), size = 15, justify = 'center').move([shift*3,100])
    LB3 = pg.text('C1.3G0.1S0.2 GAP %s' % int(gap*1000), size = 15, justify = 'center').move([shift*4,100])
    
    D_out << LB_rg
    D_out << LB1
    D_out << LB2
    D_out << LB3
    
    copy = pg.deepcopy(D_out)
    OUT.add_ref(copy).movey(i*rgR*3)


# qp(OUT)
# OUT.flatten()
OUT.write_gds('out/180829.gds')