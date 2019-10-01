# create trenches to test etching rate
D = Device('trench')

w_l = [0.2,0.3,0.4,0.6,1,2,5,10]

mx = 0
for i in range(len(w_l)):
    mx += (w_l[i] + 5)
#     print(mx)
    D << mn.waveguide(width=w_l[i],length=15e3, layer=1).movey(mx)

qp(D)
D.write_gds('190729_trench.gds')