# from __future__ import division, print_function, absolute_import
# import numpy as np
# import itertools
# from numpy import sqrt, pi, cos, sin, log, exp, sinh
# from scipy.special import iv as besseli
# from scipy.optimize import fmin, fminbound
# from scipy import integrate
# # from scipy.interpolate import interp1d

# import gdspy
# from phidl.device_layout import Device, Port
# from phidl.device_layout import _parse_layer, DeviceReference
# import phidl.routing as pr
# import copy as python_copy
# from collections import OrderedDict
# import pickle

# from skimage import draw, morphology

from phidl.geometry import *

# waveguide: 1st para is length, second is width
def waveguide(width = 1, length = 10, layer = 0):
    WG = Device('waveguide')
    WG.add_polygon( [(0, -width/2), (0, width/2), (length, width/2), (length, -width/2)], layer = layer)
    WG.add_port(name = 1, midpoint = [0,0], width = width, orientation = 180)
    WG.add_port(name = 2, midpoint = [length,0], width = width, orientation = 0)
    return WG

# new ring as an alternative of pg.ring
def new_ring(radius = 10, width = 0.5, angle_resolution = 1, layer = 0):
    D = Device(name = 'new_ring')
    inner_radius = radius - width/2
    outer_radius = radius + width/2
    angle = np.linspace(0, 360, np.ceil(360/angle_resolution))
    angle.sort()
    t=angle*np.pi/180
    inner_points_x = (inner_radius*cos(t)).tolist()
    inner_points_y = (inner_radius*sin(t)).tolist()
    outer_points_x = (outer_radius*cos(t)).tolist()
    outer_points_y = (outer_radius*sin(t)).tolist()
    xpts = inner_points_x + outer_points_x[::-1]
    ypts = inner_points_y + outer_points_y[::-1]
    D.add_polygon(points = (xpts,ypts), layer = layer)
    return D

def extend(port, length = 20,layer = 0):
	'''
	Extend the port with a straight waveguide.
	'''
	D = waveguide(port.width, length, layer=layer)
	D.rotate(port.orientation).move(origin = D.ports[1], destination = port)
	return D

# racetrack
def racetrack(radius = 10, width = 0.5, lc = 5, angle_resolution = 2.5, layer = 0):
    D = Device(name = 'racetrack')
    inner_radius = radius - width/2
    outer_radius = radius + width/2
    angle = np.append(np.linspace(0, 360, np.ceil(360/angle_resolution)),[90,90,270,270])
    angle.sort()
    t=angle*np.pi/180
    inner_points_x = [i+np.sign(i)*lc/2 for i in inner_radius*cos(t)]
    inner_points_y = (inner_radius*sin(t)).tolist()
    outer_points_x = [i+np.sign(i)*lc/2 for i in outer_radius*cos(t)]
    outer_points_y = (outer_radius*sin(t)).tolist()
    xpts = inner_points_x + outer_points_x[::-1]
    ypts = inner_points_y + outer_points_y[::-1]
    D.add_polygon(points = (xpts,ypts), layer = layer)
    return D

# ring with triple slot
def slot_ring(radius=50,CGS=[1.0,0.1,0.3], angle_resolution = 2.5, layer = 0):
    D = Device(name = 'slot_ring')
    cR=radius
    iR=radius-CGS[0]*0.5-CGS[1]-CGS[2]*0.5
    oR=radius+CGS[0]*0.5+CGS[1]+CGS[2]*0.5
    D << new_ring(radius=cR,width=CGS[0], layer=layer)
    D << new_ring(radius=iR,width=CGS[2], layer=layer)
    D << new_ring(radius=oR,width=CGS[2], layer=layer)
    return D

@device_lru_cache
def arc_grating(num_periods = 20, period = 0.75, fill_factor = 0.5, angle = 45, length_taper = 5, width = 0.5, layer = 0):
    #returns a fiber grating
    G = Device('grating')

    # make the grating teeth
    cradius = length_taper + period*(1-0.5*fill_factor)
    for i in range(num_periods):
        cgrating = G.add_ref(arc(radius=cradius, start_angle=-angle/2, theta=angle, width=period*fill_factor, layer = layer))
        cradius += period

    # make the taper
    out_len = width*0.5/np.tan(angle/360*np.pi)
    A = bbox([(0,-width/2),(out_len,width/2)])
    B = arc(radius=length_taper/2,start_angle=-angle/2,theta=angle,width=length_taper,layer=layer)
    G.add_ref(boolean(A, B, operation = 'a+b'))
    p = G.add_port(name = 1, midpoint = (0,0), width = width, orientation = 180)

    G.flatten()
    return G