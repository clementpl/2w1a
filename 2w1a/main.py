import vrep
import random
import time
import robot
import algo
import pickle

def main():
    # Close eventual old connections
    vrep.simxFinish(-1)
    # Connect to V-REP remote server
    opmode = vrep.simx_opmode_oneshot_wait
    clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
    if clientID != -1:
        vrep.simxSynchronous(clientID, True)
        r = robot.Robot(opmode, clientID)
        algoGen = algo.Algo(75, 75, r, 0.50, 0.01)
        algoGen.run()
        with open('bestCandidate', 'wb') as fp:
            pickle.dump(algoGen.population[0].operations, fp)
        vrep.simxFinish(clientID)

if __name__ == '__main__':
    main()
