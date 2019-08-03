D = Device('simple')

l = 8e3
bend = 100
w = 1
wg1 = D << mn.waveguide(w,l)
wg2 = D << mn.waveguide(w,l).move((-l,-4*bend))

S = Device('s_shape') 
wg0 = S << pg.connector(width=w)
arc1 = S << pg.turn(wg0.ports[2],angle=180,radius=bend,angle_resolution=1)
arc2 = S << pg.turn(arc1.ports[2],angle=-180,radius=bend,angle_resolution=1)
D << S

y_shift = 6*2*bend
wg1 = D << mn.waveguide(w,l).move((0,y_shift))
wg2 = D << mn.waveguide(w,l).move((-l,y_shift-8*bend))

S1 = pg.copy(S)
D << S1.movey(y_shift)
S2 = pg.copy(S)
D << S2.movey(y_shift-4*bend)


y_shift = 14*2*bend
wg1 = D << mn.waveguide(w,l).move((0,y_shift))
wg2 = D << mn.waveguide(w,l).move((-l,y_shift-12*bend))

S1 = pg.copy(S)
D << S1.movey(y_shift)
S2 = pg.copy(S)
D << S2.movey(y_shift-4*bend)
S2 = pg.copy(S)
D << S2.movey(y_shift-8*bend)

# y_shift = 16*2*bend
# wg1 = D << mn.waveguide(w,l).move((0,y_shift))
# wg2 = D << mn.waveguide(w,l).move((-l,y_shift-16*bend))

# S1 = pg.copy(S)
# D << S1.movey(y_shift)
# S2 = pg.copy(S)
# D << S2.movey(y_shift-4*bend)
# S3 = pg.copy(S)
# D << S2.movey(y_shift-8*bend)
# S4 = pg.copy(S)
# D << S2.movey(y_shift-12*bend)

qp(D)
D.write_gds('simple_s.gds')
