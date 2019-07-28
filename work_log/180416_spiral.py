import numpy as np

from phidl import Device, Layer, LayerSet, make_device
from phidl import quickplot as qp # Rename "quickplot()" to the easier "qp()"
import phidl.geometry as pg

import phidl.routing as pr
import phidl.utilities as pu

# import customed geolib
import mine as mn
import matplotlib.pyplot as plt

D = Device('SEMI')
D_b = Device('lb')
width = 1.5
xs = 50
ys = 90

for i in range(4):
    CEL = Device('CEL')
    foo = 1e3+i*xs
    SS = CEL << mn.semi_spiral(bend=430,shift=xs,width=width,layer=1, n=i).move((foo*i,-ys*i))
    EXR = CEL << mn.extend(port=SS.ports[2],length=6e3-(foo+xs)*i)

    EXL = CEL << mn.extend(port=SS.ports[1],length=(foo)*i)
    CN = pg.connector((-3.7e3,SS.ports[2].midpoint[1]),width,orientation=0)
    CEL << pr.route_manhattan(CN.ports[1],EXL.ports[2],bendType='circular',radius=300)    
    L = CEL.area()/width
    D_b << pg.text(text='WL%.2f'% L, position=((foo*i,100-ys*i)))
    D << CEL
#       D.area()/width

D_out = pg.outline(D,distance=10)
D_out << D_b

D_out.flatten().write_gds('190417_spiral_align.gds')
# qp(D)
