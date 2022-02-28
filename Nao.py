# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 11:00:00 2022

@author: robinlab
"""

from controller import Robot

from fit import sinfun, A, T, phi, K
from numpy import linspace
import math

class Nao (Robot):
    PHALANX_MAX = 8
    
    def __init__(self):
        Robot.__init__(self)
        self.findAndEnableDevices()
        
    def setJoints(self, joints, values):
        for i in range(len(joints)):
            getattr(self, joints[i]).setPosition(values[i])
            
    def steps(self, n):
        for _ in range(n):
            self.step(self.timeStep)
         
    def findAndEnableDevices(self):
        # get the time step of the current world.
        self.timeStep = int(self.getBasicTimeStep())

        # camera
        self.cameraTop = self.getDevice("CameraTop")
        self.cameraBottom = self.getDevice("CameraBottom")
        self.cameraTop.enable(4 * self.timeStep)
        self.cameraBottom.enable(4 * self.timeStep)

        # accelerometer
        self.accelerometer = self.getDevice('accelerometer')
        self.accelerometer.enable(4 * self.timeStep)

        # gyro
        self.gyro = self.getDevice('gyro')
        self.gyro.enable(4 * self.timeStep)

        # gps
        self.gps = self.getDevice('gps')
        self.gps.enable(4 * self.timeStep)

        # inertial unit
        self.inertialUnit = self.getDevice('inertial unit')
        self.inertialUnit.enable(self.timeStep)

        # ultrasound sensors
        self.us = []
        usNames = ['Sonar/Left', 'Sonar/Right']
        for i in range(0, len(usNames)):
            self.us.append(self.getDevice(usNames[i]))
            self.us[i].enable(self.timeStep)

        # foot sensors
        self.fsr = []
        fsrNames = ['LFsr', 'RFsr']
        for i in range(0, len(fsrNames)):
            self.fsr.append(self.getDevice(fsrNames[i]))
            self.fsr[i].enable(self.timeStep)

        # foot bumpers
        self.lfootlbumper = self.getDevice('LFoot/Bumper/Left')
        self.lfootrbumper = self.getDevice('LFoot/Bumper/Right')
        self.rfootlbumper = self.getDevice('RFoot/Bumper/Left')
        self.rfootrbumper = self.getDevice('RFoot/Bumper/Right')
        self.lfootlbumper.enable(self.timeStep)
        self.lfootrbumper.enable(self.timeStep)
        self.rfootlbumper.enable(self.timeStep)
        self.rfootrbumper.enable(self.timeStep)

        # there are 7 controlable LED groups in Webots
        self.leds = []
        self.leds.append(self.getDevice('ChestBoard/Led'))
        self.leds.append(self.getDevice('RFoot/Led'))
        self.leds.append(self.getDevice('LFoot/Led'))
        self.leds.append(self.getDevice('Face/Led/Right'))
        self.leds.append(self.getDevice('Face/Led/Left'))
        self.leds.append(self.getDevice('Ears/Led/Right'))
        self.leds.append(self.getDevice('Ears/Led/Left'))

        # get phalanx motor tags
        # the real Nao has only 2 motors for RHand/LHand
        # but in Webots we must implement RHand/LHand with 2x8 motors
        self.lphalanx = []
        self.rphalanx = []
        self.maxPhalanxMotorPosition = []
        self.minPhalanxMotorPosition = []
        for i in range(0, self.PHALANX_MAX):
            self.lphalanx.append(self.getDevice("LPhalanx%d" % (i + 1)))
            self.rphalanx.append(self.getDevice("RPhalanx%d" % (i + 1)))

            # assume right and left hands have the same motor position bounds
            self.maxPhalanxMotorPosition.append(self.rphalanx[i].getMaxPosition())
            self.minPhalanxMotorPosition.append(self.rphalanx[i].getMinPosition())

        jointNames = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 
          'LElbowYaw', 'LElbowRoll', 'LWristYaw', 
          'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 
          'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 
          'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 
          'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 
          'RWristYaw']
        for joint in jointNames:
            setattr(self, joint, self.getDevice(joint))

    def initCrawling(self):
        self.setJoints(["RShoulderPitch", "LShoulderPitch"], [-0.25, -0.25])
        self.steps(50)

        self.setJoints(["RAnklePitch", "LAnklePitch"], [-0.75, -0.75])
        self.steps(50)
        
        joints = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 
          'LElbowYaw', 'LElbowRoll', 'LWristYaw', 
          'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 
          'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 
          'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 
          'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 
          'RWristYaw']
        posture = [0.0, -0.67, -0.25, 0.1, -1.58, -0.1, 0.0,
                   -0.4, 0.2437, -0.825, 1.8, 0.75, 0.68, -0.4, -0.2437,
                   -0.825, 1.8, 0.75, -0.68, -0.25, -0.1, 1.58, 0.1,
                   0.0]
        self.setJoints(joints, posture)
        self.steps(50)

        self.setJoints(["RShoulderPitch", "LShoulderPitch"], [0.21, 0.21])
        self.steps(50)
        
    def crawl(self, params, seconds=5):
        joints = ["LShoulderPitch","RShoulderPitch",
                  "LShoulderRoll","RShoulderRoll",
                  "LElbowRoll","RElbowRoll",
                  "LKneePitch","RKneePitch",
                  "LHipPitch","RHipPitch",
                  "LHipRoll","RHipRoll",]
        
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

        cycles = seconds / period
        sampercyc = 20
        t = linspace(period,period*(cycles+1),int(sampercyc*cycles))
        timeList = t.tolist()
        
        T.set(period)
        
        A.set(shoulderPitchA)
        phi.set(shoulderPitchPhi)
        K.set(shoulderPitchK)
        LSP = sinfun(t).tolist()
        
        A.set(shoulderPitchA)
        phi.set(shoulderPitchPhi+math.pi)
        K.set(shoulderPitchK)
        RSP = sinfun(t).tolist()
        
        A.set(shoulderRollA)
        phi.set(shoulderRollPhi)
        K.set(shoulderRollK)
        LSR = sinfun(t).tolist()
        
        A.set(shoulderRollA)
        phi.set(shoulderRollPhi)
        K.set(-shoulderRollK)
        RSR = sinfun(t).tolist()
        
        A.set(elbowRollA)
        phi.set(elbowRollPhi)
        K.set(elbowRollK)
        LER = sinfun(t).tolist()
        
        A.set(elbowRollA)
        phi.set(elbowRollPhi)
        K.set(-elbowRollK)
        RER = sinfun(t).tolist()
        
        A.set(kneePitchA)
        phi.set(kneePitchPhi)
        K.set(kneePitchK)
        LKP = sinfun(t).tolist()
        
        A.set(kneePitchA)
        phi.set(kneePitchPhi+math.pi)
        K.set(kneePitchK)
        RKP = sinfun(t).tolist()
        
        A.set(hipPitchA)
        phi.set(hipPitchPhi)
        K.set(hipPitchK)
        LHP = sinfun(t).tolist()
        
        A.set(hipPitchA)
        phi.set(hipPitchPhi+math.pi)
        K.set(hipPitchK)
        RHP = sinfun(t).tolist()
        
        A.set(hipRollA)
        phi.set(hipRollPhi)
        K.set(hipRollK)
        LHR = sinfun(t).tolist()
        
        A.set(hipRollA)
        phi.set(hipRollPhi)
        K.set(-hipRollK)
        RHR = sinfun(t).tolist()
        
        xi,yi,zi = self.gps.getValues()
        
        # Make the robot crawl
        for i in range(len(timeList)):
            posture = [LSP[i], RSP[i], LSR[i], RSR[i], LER[i], RER[i],
                       LKP[i], RKP[i], LHP[i], RHP[i], LHR[i], RHR[i]]
            self.setJoints(joints, posture)
            self.steps(3)

        xf,yf,zf = self.gps.getValues()
        
        dx = xf-xi
        dy = yf-yi
        dz = zf-zi
        distance = math.sqrt(dx*dx+dy*dy+dz*dz)
        return distance
