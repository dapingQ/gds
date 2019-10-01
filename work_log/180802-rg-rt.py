from __future__ import division, print_function, absolute_import
import numpy as np

from phidl import Device, Layer, LayerSet, make_device
from phidl import quickplot as qp # Rename "quickplot()" to the easier "qp()"
import phidl.geometry as pg
import phidl.routing as pr
import phidl.utilities as pu

# import customed geolib
from mine import waveguide, racetrack, new_ring

wgL = 20e3 # mm
wgW = 1.5
rgR = 200
cldW = 20

OUT = Device()

WG = waveguide(length=wgL, width=wgW)
RG = pg.ring(rgR, wgW)
RT1 = racetrack(rgR, wgW,10)
RT2 = racetrack(rgR, wgW,15)
RT3 = racetrack(rgR, wgW,20)

gap_list = np.arange(0.05,0.4,0.05)

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
    LB3 = pg.text('LC 20 GAP %s' % int(gap*1000), size = 15, justify = 'center').move([shift*4,100])
    
    D_out << LB_rg
    D_out << LB1
    D_out << LB2
    D_out << LB3
    
    copy = pg.deepcopy(D_out)
    OUT.add_ref(copy).movey(i*rgR*3)

# qp(OUT)

OUT.write_gds('./out/180802.gds')
