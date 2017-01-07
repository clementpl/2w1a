import random
import numpy
import vrep
import time

class Candidat:
    def __init__(self, robot, operations=None):
        self.robot = robot
        if (operations == None):
            self.operations = []
            self.generateOperations()
        else:
            self.operations = operations

    def dist(self, p1, p2):
        return numpy.linalg.norm(numpy.array(p1)-numpy.array(p2))

    def getMotor(self, num):
        motors = ["shoulder", "elbow", "wrist"]
        return motors[num]

    def generateOperations(self):
        for i in range(100):
            self.operations.append([random.randint(0, 2), random.randint(0, 360)])

    def getDistance(self):
        print("start getDistance");
#        self.robot.setRotation(250.0, "shoulder")
        vrep.simxStartSimulation(self.robot.clientID, self.robot.opmode)
        savePos = self.robot.position()
        saveOrientation = self.robot.orientation()
        for i in range(3):
            for op in self.operations:
                self.robot.setRotation(op[1], self.getMotor(op[0]))
        vrep.simxStopSimulation(self.robot.clientID, self.robot.opmode)
        newOrientation = self.robot.orientation()
        newPos = self.robot.position()
        dist = self.dist(savePos, newPos)
        print("stop getDistance");
        return dist
