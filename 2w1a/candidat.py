import random
import numpy
import vrep
import time

class Candidat:
    def __init__(self, robot, operations=None):
        self.robot = robot
        self.dist = -1
        if (operations == None):
            self.operations = []
            self.generateOperations()
        else:
            self.operations = operations

    def computeDist(self, p1, p2):
        return numpy.linalg.norm(numpy.array(p1)-numpy.array(p2))

    def getMotor(self, num):
        motors = ["shoulder", "elbow", "wrist"]
        return motors[num]

    def generateOperations(self):
        for i in range(100):
            self.operations.append([random.randint(0, 2), random.randint(0, 360)])

    def getDistance(self):
        if (self.dist == -1):
            vrep.simxStartSimulation(self.robot.clientID, self.robot.opmode)
            vrep.simxSynchronousTrigger(self.robot.clientID)
            savePos = self.robot.position()
            saveOrient = self.robot.orientation()
            for i in range(3):
                for op in self.operations:
                    self.robot.setRotation(op[1], self.getMotor(op[0]))
                    vrep.simxSynchronousTrigger(self.robot.clientID)

            newPos = self.robot.position()
            newOrient = self.robot.orientation()
            vrep.simxStopSimulation(self.robot.clientID, self.robot.opmode)
            time.sleep(0.1)#wait for end of simxStopSimulation
            self.dist = self.computeDist(savePos, newPos) - self.computeDist(saveOrient, newOrient)/100
#            self.dist = self.computeDist(savePos, newPos)
        return self.dist
