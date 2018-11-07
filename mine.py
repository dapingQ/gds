from __future__ import division, print_function, absolute_import
import numpy as np
import itertools
from numpy import sqrt, pi, cos, sin, log, exp, sinh
from scipy.special import iv as besseli
from scipy.optimize import fmin, fminbound
from scipy import integrate
# from scipy.interpolate import interp1d

import gdspy
from phidl.device_layout import Device, Port
from phidl.device_layout import _parse_layer, DeviceReference
import phidl.routing as pr
import copy as python_copy
from collections import OrderedDict
import pickle

from skimage import draw, morphology

# waveguide: 1st para is length, second is width
def waveguide(width = 10, height = 1):
    WG = Device('waveguide')
    WG.add_polygon( [(0, 0), (width, 0), (width, height), (0, height)] )
    WG.add_port(name = 'wgport1', midpoint = [0,height/2], width = height, orientation = 180)
    WG.add_port(name = 'wgport2', midpoint = [width,height/2], width = height, orientation = 0)
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
    D << new_ring(radius=cR,width=CGS[0])
    D << new_ring(radius=iR,width=CGS[2])
    D << new_ring(radius=oR,width=CGS[2])
    return D
    

def BMRR(dis = 20, gap = 0.0, width = 1.5):
    # dis: distance of ports
    # gap is same for two bus 
    rgR = dis - gap - width 
    lc = 10*dis
    
    D = Device('BMRR')
    D << racetrack(radius = dis/2, width = width, lc = lc).movey(-1.5*dis)
    D << racetrack(radius = dis/2, width = width, lc = lc).movey(1.5*dis)
    D << pg.ring(radius=rgR,width=width).movex(4*dis)
    D << pg.ring(radius=rgR,width=width).movex(-4*dis)
    return D

