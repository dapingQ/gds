def archimedes(bent = 200, width = 0.5, n = 1, shift = 10, angle_resolution = 1, layer = 0):
    D = Device('SPIRAL')
    # spiral section
    sp_t = np.linspace(0, 360*n, np.ceil(360*n/angle_resolution))*np.pi/180
#     angle.sort()
    rho = 2*radius + sp_t*shift
    inner_rho = rho-width*.5
    outer_rho = rho+width*.5
    inner_sp_x = (inner_rho*cos(sp_t)).tolist()
    inner_sp_y = (inner_rho*sin(sp_t)).tolist()
    outer_sp_x = (outer_rho*cos(sp_t)).tolist()
    outer_sp_y = (outer_rho*sin(sp_t)).tolist()
    # arc section
    inner_t = arg(inner_sp_x,inner_sp_y)
    arc_radius = radius*0.5/sin(inner_t)
    arc_t = np.linspace(1.5*np.pi-inner_t, 1.5*np.pi+inner_t,100)[:-1]# np.ceil(2*inner_t/d2r(angle_resolution)))
    inner_arc_x = ( arc_radius*sin(inner_t) + (arc_radius-width*0.5)*cos(arc_t) ).tolist()
    inner_arc_y = ( arc_radius*cos(inner_t) + (arc_radius-width*0.5)*sin(arc_t) ).tolist()
    outer_arc_x = ( arc_radius*sin(inner_t) + (arc_radius+width*0.5)*cos(arc_t) ).tolist()
    outer_arc_y = ( arc_radius*cos(inner_t) + (arc_radius+width*0.5)*sin(arc_t) ).tolist()
    
    outer_t = arg(outer_sp_x[::-1], outer_sp_y[::-1]) 
    ext_radius = (inner_sp_x[-1]+outer_sp_x[-1])*0.5/sin(outer_t)
    ext_t = np.linspace(outer_t-np.pi*0.5, np.pi*.5,100)[0:]# np.ceil(2*inner_t/d2r(angle_resolution)))
    inner_ext_x = ( (ext_radius-width*0.5)*cos(ext_t) ).tolist()
    inner_ext_y = ( ext_radius*cos(outer_t) + (ext_radius-width*0.5)*sin(ext_t) ).tolist()
    outer_ext_x = ( (ext_radius+width*0.5)*cos(ext_t) ).tolist()
    outer_ext_y = ( ext_radius*cos(outer_t) + (ext_radius+width*0.5)*sin(ext_t) ).tolist()
    
    xpts = inner_arc_x + inner_sp_x + inner_ext_x + outer_ext_x[::-1] + outer_sp_x[::-1] + outer_arc_x[::-1]
    ypts = inner_arc_y + inner_sp_y + inner_ext_y + outer_ext_y[::-1] + outer_sp_y[::-1] + outer_arc_y[::-1]
    D.add_polygon(points = (xpts,ypts), layer = layer)
    D.add_polygon(points = (xpts,ypts), layer = layer).rotate(180)
    
    D.add_port(name = 1, midpoint = [0,D.ymax-width/2], width = width, orientation = 180)
    D.add_port(name = 2, midpoint = [0,D.ymin+width/2], width = width, orientation = 0)
    return D#.rotate(90-r2d(outer_t))
