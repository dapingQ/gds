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
num = 6
width_bus = 1.5
width_rg = 1.5
ext = 3e3
# BD=
# RG=[]
for i in range(num):
    BD = D << z_shape(width=width_bus, radius=150, mid=150, left=ext+500+500*i,right=ext+500*(num-i)).movey(-30*i)
    RG = D << pg.ring(radius=200,width=width_rg)
    RG.ymin = BD.ymin + width_bus + 0.2 +gap*i
    RG.move((ext+500+500*i-100,0))

D_out = pg.outline(D,distance=8,layer=2)
for i in range(num):
    D_out << pg.text('GAP %s' % (200+50*i), size = 15, justify = 'center',layer=2).move((ext+500+500*i-100,-30*i+150))
    
D_out.flatten().write_gds('190409_ring_1mm.gds')

# qp(D_out)