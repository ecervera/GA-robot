# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:46:33 2013

@author: robinlab
"""

import math, time
from fit import sinfun, A, T, phi, K
from naoqi import ALProxy
from scipy import linspace, pi

class Nao:
    
    def __init__(self):
        self.IP = "localhost"  # Replace here with your NaoQi's IP address.
        self.PORT = 9559
        self.bmanager = ALProxy("ALBehaviorManager", self.IP, self.PORT)
        self.poseProxy = ALProxy("ALRobotPose", self.IP, self.PORT)
        self.motionProxy = ALProxy("ALMotion", self.IP, self.PORT)
        self.memProxy = ALProxy("ALMemory",self.IP,self.PORT)
    
    def stand_up(self):
        if (self.bmanager.isBehaviorRunning('stand_up')):
            self.bmanager.stopBehavior('stand_up')
            time.sleep(1.0)
        self.bmanager.runBehavior('stand_up')

    def getActualPose(self):
        pose, elapsedTime = self.poseProxy.getActualPoseAndTime()
        return pose
        
    def initCrawling(self):
        proxy = self.motionProxy
        proxy.setStiffnesses("Body", 1.0)
        proxy.setAngles(['LShoulderPitch','RShoulderPitch'], [-0.25, -0.25], 0.5)
        time.sleep(3)
        proxy.setAngles(['LAnklePitch','RAnklePitch'], [-0.75, -0.75], 0.2)
        time.sleep(3)
        proxy.setStiffnesses("Body", 1.0)
        names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 
          'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 
          'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 
          'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 
          'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 
          'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 
          'RWristYaw', 'RHand']
        posture = [0.0, -0.7, -0.25, 0.1, -1.58, -0.1, 0.0, 0.0,
                   -0.4, 0.2437, -0.825, 1.8, 0.75, 0.68, -0.4, -0.2437,
                   -0.825, 1.8, 0.75, -0.68, -0.25, -0.1, 1.58, 0.1,
                   0.0, 0.0]
        proxy.setAngles(names, posture, 0.2);
        time.sleep(3)
        proxy.setAngles(['LShoulderPitch','RShoulderPitch'], [0.21, 0.21], 1.0)
        time.sleep(3)
        
    def crawl(self, params, seconds=5):
        proxy = self.motionProxy
        proxy.setStiffnesses("Body", 1.0)
        
        names = ["LShoulderPitch","RShoulderPitch",
                 "LShoulderRoll","RShoulderRoll",
                 "LElbowRoll","RElbowRoll",
                 "LKneePitch","RKneePitch",
                 "LHipPitch","RHipPitch",
                 "LHipRoll","RHipRoll",]
        
        # PARAMETERS
#        period = 1.28
#        
#        shoulderPitchA = 0.1
#        shoulderPitchK = 0.21
#        shoulderPitchPhi = 0.
#        
#        shoulderRollA = 0.035
#        shoulderRollK = 0.039
#        shoulderRollPhi = -2.
#        
#        hipPitchA = 0.12
#        hipPitchK = -0.86
#        hipPitchPhi = pi
#        
#        hipRollA = 0.06
#        hipRollK = 0.33
#        hipRollPhi = pi/2
#        
#        elbowRollA = 0.005
#        elbowRollK = -0.11
#        elbowRollPhi = -2.
#        
#        kneePitchA = 0.008
#        kneePitchK = 1.8
#        kneePitchPhi = 0.

        period = params[0]
        
        shoulderPitchA = params[1]
        shoulderPitchK = params[2]
        shoulderPitchPhi = params[3]
        
        shoulderRollA = params[4]
        shoulderRollK = params[5]
        shoulderRollPhi = params[6]
        
        hipPitchA = params[7]
        hipPitchK = params[8]
        hipPitchPhi = params[9]
        
        hipRollA = params[10]
        hipRollK = params[11]
        hipRollPhi = params[12]
        
        elbowRollA = params[13]
        elbowRollK = params[14]
        elbowRollPhi = params[15]
        
        kneePitchA = params[16]
        kneePitchK = params[17]
        kneePitchPhi = params[18]        

        #cycles = 10
        cycles = seconds / period
        sampercyc = 20
        t = linspace(period,period*(cycles+1),sampercyc*cycles)
        timeList = t.tolist()
        isAbsolute = True
        
        T.set(period)
        
        A.set(shoulderPitchA)
        phi.set(shoulderPitchPhi)
        K.set(shoulderPitchK)
        LSP = sinfun(t)
        
        A.set(shoulderPitchA)
        phi.set(shoulderPitchPhi+pi)
        K.set(shoulderPitchK)
        RSP = sinfun(t)
        
        A.set(shoulderRollA)
        phi.set(shoulderRollPhi)
        K.set(shoulderRollK)
        LSR = sinfun(t)
        
        A.set(shoulderRollA)
        phi.set(shoulderRollPhi)
        K.set(-shoulderRollK)
        RSR = sinfun(t)
        
        A.set(elbowRollA)
        phi.set(elbowRollPhi)
        K.set(elbowRollK)
        LER = sinfun(t)
        
        A.set(elbowRollA)
        phi.set(elbowRollPhi)
        K.set(-elbowRollK)
        RER = sinfun(t)
        
        A.set(kneePitchA)
        phi.set(kneePitchPhi)
        K.set(kneePitchK)
        LKP = sinfun(t)
        
        A.set(kneePitchA)
        phi.set(kneePitchPhi+pi)
        K.set(kneePitchK)
        RKP = sinfun(t)
        
        A.set(hipPitchA)
        phi.set(hipPitchPhi)
        K.set(hipPitchK)
        LHP = sinfun(t)
        
        A.set(hipPitchA)
        phi.set(hipPitchPhi+pi)
        K.set(hipPitchK)
        RHP = sinfun(t)
        
        A.set(hipRollA)
        phi.set(hipRollPhi)
        K.set(hipRollK)
        LHR = sinfun(t)
        
        A.set(hipRollA)
        phi.set(hipRollPhi)
        K.set(-hipRollK)
        RHR = sinfun(t)
        
        xi = self.memProxy.getData("Simulator/TorsoPosition/X")
        yi = self.memProxy.getData("Simulator/TorsoPosition/Y")
        zi = self.memProxy.getData("Simulator/TorsoPosition/Z")
        #print "Robot Position before", (xi,yi,zi)
        
        # Make the robot crawl
        proxy.angleInterpolation(names, 
                                 [LSP.tolist(), RSP.tolist(),
                                  LSR.tolist(), RSR.tolist(),
                                  LER.tolist(), RER.tolist(),
                                  LKP.tolist(), RKP.tolist(),
                                  LHP.tolist(), RHP.tolist(),
                                  LHR.tolist(), RHR.tolist()], 
                                 [timeList, timeList, timeList, 
                                  timeList, timeList, timeList, 
                                  timeList, timeList, timeList, 
                                  timeList, timeList, timeList], 
                                 isAbsolute)
        
        xf = self.memProxy.getData("Simulator/TorsoPosition/X")
        yf = self.memProxy.getData("Simulator/TorsoPosition/Y")
        zf = self.memProxy.getData("Simulator/TorsoPosition/Z")
        #print "Robot Position after", (xf,yf,zf)
        
        dx = xf-xi
        dy = yf-yi
        dz = zf-zi
        distance = math.sqrt(dx*dx+dy*dy+dz*dz)
        #print "Distance: %.3f" % distance
        return distance
