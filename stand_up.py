# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 19:09:10 2013

@author: robinlab
"""
from naoqi import ALProxy
import time

IP = "localhost"  # Replace here with your NaoQi's IP address.
PORT = 9559
bmanager = ALProxy("ALBehaviorManager", IP, PORT)

if (bmanager.isBehaviorRunning('stand_up')):
    bmanager.stopBehavior('stand_up')
    time.sleep(1.0)
bmanager.runBehavior('stand_up')
