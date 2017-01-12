import vrep
import math

class Robot:
    def __init__(self, opmode, clientID):
        #Function to wait
        self.clientID = clientID
        self.opmode = opmode
        self.opmode_streaming = vrep.simx_opmode_streaming
        self.opmode_buffer = vrep.simx_opmode_buffer
        self.wrist = vrep.simxGetObjectHandle(clientID, "WristMotor", opmode)[1]
        self.elbow = vrep.simxGetObjectHandle(clientID, "ElbowMotor", opmode)[1]
        self.shoulder = vrep.simxGetObjectHandle(clientID, "ShoulderMotor", opmode)[1]
        self.robot = vrep.simxGetObjectHandle(clientID, "2W1A", opmode)[1]

    def orientation(self):
        return vrep.simxGetObjectOrientation(self.clientID, self.robot, -1, self.opmode)[1]

    def position(self):
        return vrep.simxGetObjectPosition(self.clientID, self.robot, -1, self.opmode)[1]

    def setRotation(self, rotation, motor):
        return vrep.simxSetJointTargetPosition(self.clientID, getattr(self, motor), math.radians(rotation), self.opmode)
