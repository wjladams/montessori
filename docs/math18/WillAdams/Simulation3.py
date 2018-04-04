#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 19:44:46 2018

@author: wjadams
"""
from math import sqrt, sin, cos, pi, atan2
from matplotlib import pyplot as plt
from matplotlib import figure as fig

#The Earth's radius in meters
earth_radius = 6.371e6
#The Earth's mass in kg
earth_mass = 5.972e24
#Newton's gravitational constant in mks units
G = 6.674e-11


def orbital_velocity(dist_to_body, mass_of_body = earth_mass):
    return sqrt(G * mass_of_body / dist_to_body)

class Simulation:
    def __init__(self, init_x=0, init_y=earth_radius, vx=0, vy=0):
        self.xs = [init_x]
        self.ys = [init_y]
        self.vxs = [vx]
        self.vys = [vy]
        self.axs = [0]
        self.ays = [0]
        self.delta_t = 0.05
        self.time = 0
        self.heading = 90

    def accel_gravity(self, planet_x=0, planet_y=0, planet_mass=earth_mass):
        '''
        Calculates the acceleration due to gravity a given distance from the
        surface of a planet.
        '''
        x = self.xs[-1]
        y = self.ys[-1]
        dist = sqrt((x-planet_x)**2 + (y-planet_y)**2)
        magnitude = planet_mass * G / (dist)**2
        accel_x = -magnitude * (x-planet_x)/dist
        accel_y = -magnitude * (y-planet_y)/dist
        return accel_x, accel_y

    def v(self, v=None, angle_degrees=0):
        if v is None:
            vy = self.vys[-1]
            vx = self.vxs[-1]
            angle = atan2(vy, vx) * 180 / pi
            return sqrt(vx**2 + vy**2), angle
        self.vxs[-1]=v * cos(angle_degrees*pi/180)
        self.vys[-1]=v * sin(angle_degrees*pi/180)

    def step(self, add_ax=0, add_ay=0, time=0, a=None, rotate_thrust=None):
        '''
        This function moves our object forward delta_t in time.  It uses
        the function accel_gravity() to calculate the y-axis acceleration
        '''
        now = self.time
        while (self.time - now) <= time:
            g_ax, g_ay = self.accel_gravity()
            if rotate_thrust is not None:
                self.heading = self.heading + rotate_thrust * self.delta_t
                self.heading = self.heading % 360
                add_ay = a * sin(self.heading * pi / 180)
                add_ax = a * cos(self.heading * pi / 180)
                ax = add_ax + g_ax
                ay = add_ay + g_ay
            else:
                ax = g_ax + add_ax
                ay = g_ay + add_ay 
            vy = self.vys[-1] + ay * self.delta_t
            vx = self.vxs[-1] + ax * self.delta_t
            y = self.ys[-1] + vy * self.delta_t
            x = self.xs[-1] + vx * self.delta_t
            self.xs.append(x)
            self.ys.append(y)
            self.vxs.append(vx)
            self.vys.append(vy)
            self.axs.append(ax)
            self.ays.append(ay)
            self.time += self.delta_t

    def graph(self):
        earth_xs = [earth_radius * cos(2*pi/100 * i) for i in range(500) ]
        earth_ys = [earth_radius * sin(2*pi/100 * i) for i in range(500) ]
        plt.plot(self.xs, self.ys )
        plt.plot(earth_xs, earth_ys)

    def orbital_velocity(self):
        x = self.xs[-1]
        y = self.ys[-1]
        dist_to_earth = sqrt(x**2 + y**2)
        earth_angle = atan2(y, x) * 180 / pi
        orbit_angle = earth_angle - 90
        return orbital_velocity(dist_to_earth), orbit_angle

