# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 20:28:24 2013

@author: robinlab
"""

from scipy import optimize, sin, pi
from numpy.core.multiarray import arange

class Parameter:
    def __init__(self, value=0):
            self.value = value

    def set(self, value):
            self.value = value

    def __call__(self):
            return self.value

# sinfun parameters
A   = Parameter()
T   = Parameter()
phi = Parameter()
K   = Parameter()

def sinfun(x): 
    return A()*sin(2*pi/T()*x+phi()) + K()   

def fit(function, parameters, y, x = None):
    def f(params):
        i = 0
        for p in parameters:
            p.set(params[i])
            i += 1
        return y - function(x)

    if x is None: x = arange(y.shape[0])
    p = [param() for param in parameters]
    p, success = optimize.leastsq(f, p)
    return p, success