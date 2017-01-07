import vrep
import random
import time
import robot
import algo

def main():
    # Close eventual old connections
    vrep.simxFinish(-1)
    # Connect to V-REP remote server
    opmode = vrep.simx_opmode_oneshot_wait
    clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
    vrep.simxSynchronous(clientID, True)
    if clientID != -1:
        r = robot.Robot(opmode, clientID)
        algoGen = algo.Algo(50, 25, r)
        algoGen.run()
        vrep.simxFinish(clientID)

if __name__ == '__main__':
    main()
