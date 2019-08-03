D = Device('CJC')

devLen = 10e3
def z_shape(width=1.5, radius=50, mid=50, left=100, right=100, layer=0):
    D = Device('z_shape')
    LW = D << mn.waveguide(width=width,length=left,layer=layer)
    BD1 = D << pg.turn(port=LW.ports[2],angle=90,radius=radius,angle_resolution=0.5)
    MD = D << mn.extend(port=BD1.ports[2],length=mid)
    BD2 = D << pg.turn(port=MD.ports[2],angle=-90,radius=radius,angle_resolution=0.5)
    RW = D << mn.extend(port=BD2.ports[2],length=right)
    return D

PD = 2.5e2 # cell position distance, PerioD
num = 8 # num of MRR

w = 4 # width of
width_bus = w
width_rg = w

# ext = 2.5e3
rad = 100
SD = 50 # bus waveguide shift distance

LB_CEL = Device('LB_CEL')
xx = 5.5e3
for i in range(num):
    gap = 0.10 + i*0.05
    RG_CEL = Device('RG_CEL') # ring cell def
    # add ring & bus
    RG = RG_CEL << pg.ring(radius=rad,width=width_rg) 
    BUS =RG_CEL << mn.waveguide(length=rad,width=width_bus).movex(-.5*rad)
    # align ring & bus, rotate
    RG.ymin = BUS.ymax + gap
    RG_CEL.rotate(90).move((PD*i,-SD*i))
#     LB_CEL << pg.text(text='GAP%d' % (1e3*gap),position=(-rad+PD*i,-SD*i),layer=1)
    CN1 = pg.connector((xx,BUS.ymax+rad),width=width_bus)
    RT1 = RG_CEL << pr.route_manhattan(port1=CN1.ports[2],port2=BUS.ports[2],bendType='circular',radius=rad)
    CN2 = pg.connector((-(i+10)*SD,BUS.ymin-rad),width=width_bus)
    RT2 = RG_CEL << pr.route_manhattan(port1=CN2.ports[1],port2=BUS.ports[1],bendType='circular',radius=rad)
    CN3 = pg.connector((xx-devLen,BUS.ymax+rad),width=width_bus)
    RT3 = RG_CEL << pr.route_manhattan(port1=CN3.ports[1],port2=CN2.ports[2],bendType='circular',radius=rad)
    D << RG_CEL

# straight waveguide
bar =  mn.waveguide(length=devLen,width=width_bus).move((xx-devLen,-650))
for i in range(3):
    D << pg.copy(bar).movey(i*SD)
    
D_out = pg.outline(D.flatten(),distance=8,layer=1)
D_out << LB_CEL
# D_out << pg.copy(D_out).movey(2e3)   
# D_out << pg.copy(D_out).movey(1e3)
# D_out.flatten().write_gds('190729_radius100_ring_array_width%d.gds' % (1e3*width_rg))
# D_out.write_gds('190429_st.gds')

qp(D_out)