# cell11
wBus = 1.5
cellGDS = Device('cell11')

# sweep the ring width between groups of devices

gpNum  = 4
for k in range(gpNum):
    
    wRg = 1.5 + .1*k
    devLen = 9.8e3
    
    # taper length & taper width, width of bus -> width of taper
    lTp = 500
    wTp = .3
    
    # ring radius
    rRg = 200
    
    # horizontal and vertical dist. per device
    HD = 4*rRg
    VD = rRg
    devNum = 7 # num of MRR dev

    gapPeriod = .05
    
    # x-axis shift
    offset = devLen/2 - devNum*HD/2 + rRg*4
    # margin = 100

    D = Device(f'GP{k}')
    LB = Device(f'LB{k}')

    for i in range(devNum):
        gap = gapPeriod*i+0.1
        MRR = D << asymMRR(width_bus=wBus,
                           width_rg=wRg,radius=rRg,
                           gap=gap,
                           lenL=i*HD+i*rRg,
                           lenR=0,
                          layer=WG_LAY).move((offset+HD*i,-VD*i))
        LB << pg.text(text=f'WRG {wRg}\nGAP {1e3*gap:.0f}', layer=LB_LAY, justify='center').move((offset+HD*i,-VD*i))
        
        # tp port
        TPCL = D << pg.connector((lTp,rRg-VD*i), width=wBus)
        TPCR = D << pg.connector((devLen-lTp,rRg-VD*i), width=wBus)
        '''
        PTL = D << pg.connector((0,rRg-VD*i),width=wTp)
        PTR = D << pg.connector((devLen,rRg-VD*i),width=wTp)
        D << pr.route_basic(port1=TPCL.ports[2],port2=PTL.ports[1], layer=4)
        D << pr.route_basic(port1=TPCR.ports[1],port2=PTR.ports[2], layer=4)
        '''
        D << pg.taper(port=TPCL.ports[2],length=lTp,
                      width1=wBus, width2=wTp, layer=TP_LAY)
        D << pg.taper(port=TPCR.ports[1],length=lTp,
                      width1=wBus, width2=wTp, layer=TP_LAY)
        
    #     MIDL = D << pg.connector((MRR.xmin-margin,(MRR.ymin+rRg)),width=wBus)
        RT1 = D << pr.route_manhattan(port1=TPCL.ports[1],port2=MRR.ports[2],
                                      bendType='circular',radius=rRg,layer=WG_LAY)
        RT2 = D << pr.route_manhattan(port1=TPCR.ports[2],port2=MRR.ports[1],
                                      bendType='circular',radius=rRg,layer=WG_LAY)

    markNum = 3
    markDist = 300
    markSize = 100
    markLeft = D << [pg.cross(length=100, width=20, layer=MK_LAY).move((i*markDist, -VD*devNum)) for i in range(markNum)  ]
    markRight = D << [pg.cross(length=100, width=20, layer=MK_LAY).move((devLen-i*markDist, -VD*devNum)) for i in range(markNum)  ]
    LB << pg.text(text=f'R {rRg:.0f}\nWB {wBus:.2f}\nWRG {wRg}\nTPL {lTp}\nTPW {wTp}', 
                      layer=LB_LAY, justify='right', size=20).move(TPCL.ports[1]).move((0,-rRg))
    LB << pg.text(text=f'R {rRg:.0f}\nWB {wBus:.2f}\nWRG {wRg}\nTPL {lTp}\nTPW {wTp}', 
                      layer=LB_LAY, justify='left', size=20).move(TPCR.ports[2]).move((0,-rRg))
    D << LB
    cellGDS << D.flatten().movey(VD*(devNum+2)*k)

bar =  mn.waveguide(length=devLen,width=wBus, layer=WG_LAY).move((0,-(devNum+1)*VD)) 

for i in range(3):
    cellGDS << pg.copy(bar).movey(-i*VD-VD*2)


cellGDS.move(-cellGDS.center)

cellGDS <<  pg.basic_die(size=cellSize, text_size=100,
                         street_length=500, 
                         street_width=20, text_location='S',
                         die_name='cell 11',
                         draw_bbox=False,
                         layer=MK_LAY)
cellGDS.flatten().write_gds('cell33.gds')