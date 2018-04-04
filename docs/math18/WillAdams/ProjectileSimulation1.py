#!/usr/bin/env python3
"""
Created on Sun Feb 18 22:51:55 2018

@author: Dr. Bill Adams
"""
import pandas as pd
import numpy as np
#The Earth's radius in meters
earth_radius = 6.371e6
#The Earth's mass in kg
earth_mass = 5.972e24
#Newton's gravitational constant in mks units
G = 6.674e-11


########################################################
##### Functions that define our simulation          ####
########################################################
def next_step(delta_t, current_x, current_y, 
              current_vx, current_vy):
    '''
    This function moves our object forward delta_t in time.  It uses
    the function accel_gravity() to calculate the y-axis acceleration
    '''
    ay = accel_gravity(current_y)
    ax = 0
    vy = current_vy + ay * delta_t
    vx = current_vx + ax * delta_t
    y = current_y + vy * delta_t
    x = current_x + vx * delta_t
    return (x, y, vx, vy)

def accel_gravity(dist_from_surface, planet_mass=earth_mass, 
                  planet_radius=earth_radius):
    '''
    Calculates the acceleration due to gravity a given distance from the
    surface of a planet.
    '''
    return -planet_mass * G / (dist_from_surface+planet_radius)**2

def simulate_angle(x, y, v, angle, delta_t=0.01, max_t=1000):
    angle_deg = angle * np.pi/180
    return simulate(x, y, v*np.cos(angle_deg), v*np.sin(angle_deg), delta_t, max_t)
    
def simulate(x, y, vx, vy, delta_t=0.01, max_t=1000):
    '''
    Performs our full simulation until the object hits the planet or
    we go out to max_t.
    '''
    t = 0
    rval = []
    while (y >= 0) and (t < max_t):
        x, y, vx, vy = next_step(delta_t, x, y, vx, vy)
        #print('x='+str(x)+" y="+str(y))
        t = t+delta_t
        rval.append([x, y, vx, vy, t])
    print("Last x="+str(x))
    return pd.DataFrame(rval, columns=['X', 'Y', 'Vx', 'Vy', 'Time'])

########################################################
####  Now do the simulation   ##########################
########################################################
#info=simulate(x=0, y=10, vx=1, vy=11300, delta_t=0.05, max_t=60000)
info=simulate_angle(x=0, y=10, v=16000, angle=5, delta_t=0.05, max_t=600000)
from matplotlib import pyplot as plt
#Plot the results
plt.scatter(info['X'], info['Y'])
plt.title("Projectile Trajectory")
plt.xlabel('X-axis')
plt.ylabel('Vertical Height')
