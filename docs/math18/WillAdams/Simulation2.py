#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 15:46:38 2018

@author: wjadams
"""

#!/usr/bin/env python3
"""
Created on Sun Feb 18 22:51:55 2018

@author: Dr. Bill Adams
"""
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import figure as fig
#The Earth's radius in meters
earth_radius = 6.371e6
#The Earth's mass in kg
earth_mass = 5.972e24
#Newton's gravitational constant in mks units
G = 6.674e-11


from math import sqrt, sin, cos, pi

def next_step2(delta_t, current_x, current_y, 
              current_vx, current_vy):
    '''
    This function moves our object forward delta_t in time.  It uses
    the function accel_gravity() to calculate the y-axis acceleration
    '''
    ax, ay = accel_gravity2(current_x, current_y)
    vy = current_vy + ay * delta_t
    vx = current_vx + ax * delta_t
    y = current_y + vy * delta_t
    x = current_x + vx * delta_t
    return (x, y, vx, vy)

def accel_gravity2(x, y, planet_x=0, planet_y=0, planet_mass=earth_mass):
    '''
    Calculates the acceleration due to gravity a given distance from the
    surface of a planet.
    '''
    dist = sqrt((x-planet_x)**2 + (y-planet_y)**2)
    magnitude = planet_mass * G / (dist)**2
    accel_x = -magnitude * (x-planet_x)/dist
    accel_y = -magnitude * (y-planet_y)/dist
    return accel_x, accel_y

def simulate2(x, y, angle, v, delta_t=0.01, max_t=1000, planet_radius=earth_radius):
    '''
    Performs our full simulation until the object hits the planet or
    we go out to max_t.
    '''
    vx = v * cos(angle)
    vy = v * sin(angle)
    t = 0
    rval = []
    while (sqrt(x**2 + y**2) >= planet_radius) and (t < max_t):
        x, y, vx, vy = next_step2(delta_t, x, y, vx, vy)
        #print('x='+str(x)+" y="+str(y))
        t = t+delta_t
        rval.append([x, y, vx, vy, t])
    return pd.DataFrame(rval, columns=['X', 'Y', 'Vx', 'Vy', 'Time'])


########################################################
####  Now do the simulation   ##########################
########################################################
info=simulate2(x=0, y=earth_radius, angle=pi/7.8, v=11100, delta_t=1, max_t=1000000)
earth_xs = [earth_radius * cos(2*pi/100 * i) for i in range(500) ]
earth_ys = [earth_radius * sin(2*pi/100 * i) for i in range(500) ]
x = [info['X'][i] for i in range(len(info['X'])) if i % 100 == 0 ]
y = [info['Y'][i] for i in range(len(info['Y'])) if i % 100 == 0 ]

plt.figure(figsize=(10,10))
plt.scatter(x, y, s=2 )
plt.scatter(earth_xs, earth_ys, s=2)
plt.show()
