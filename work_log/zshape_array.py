def s_shape(l):
    D = Device()
    wg = D << mn.waveguide(width=w,length=l).movex(-l/2).rotate(90)
    b1 = D << pg.turn(wg.ports[1],angle=-90,radius=bend,angle_resolution=2)
    b2 = D << pg.turn(wg.ports[2],angle=-90,radius=bend,angle_resolution=2)
#     D << mn.waveguide()
    return D

D = Device('simple')

l = 8e3
wg0 = D << mn.waveguide(w,2*l).movex(-l)

bend = 100
w = 1

step = 200
ys = 0
for i in range(4):
    ys += (i+1)*step
    S = Device('S_shape')
    h=i*step
    S << pg.copy(s_shape(h))
    S << mn.waveguide(w,l-bend).move((bend,h/2+bend))
    S << mn.waveguide(w,l-bend).move((-l,-h/2-bend))
    D << S.movey(ys)

D.flatten()
qp(D)
D.write_gds('simple.gds')

# D = Device('simple')

# l = 5e3

# bend = 100
# w = 1

# wg0 = D << mn.waveguide(w,2*l).movex(-l)


# step = 200
# ys = 0
# for i in range(4):
#     ys += (i+1)*step
#     S = Device('S_shape')
#     h=i*step
#     S << pg.copy(s_shape(h))
#     S << mn.waveguide(w,l-bend).move((bend,h/2+bend))
#     S << mn.waveguide(w,l-bend).move((-l,-h/2-bend))
#     D << S.movey(ys)

# D.flatten()

# D_set = Device('final')

# D_set << pg.deepcopy(D)
# D_set << pg.deepcopy(D).movey(3e3)
# D_set << pg.deepcopy(D).movey(6e3)

# qp(D_set)
# D_set.write_gds('simple_set.gds')
