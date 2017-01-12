import sys
import pickle
import os.path
import robot
import candidat
import vrep

if (len(sys.argv) != 2):
    print("[USAGE] test.py input_file")
else:
    filename = sys.argv[1]
    if (os.path.isfile(filename)):
        operations = pickle.load(open(filename, 'rb'))
        # Close eventual old connections
        vrep.simxFinish(-1)
        # Connect to V-REP remote server
        opmode = vrep.simx_opmode_oneshot_wait
        clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
        vrep.simxSynchronous(clientID, True)
        r = robot.Robot(opmode, clientID)
        c = candidat.Candidat(r, operations)
        c.getDistance()
        print ("stop")
        vrep.simxFinish(clientID)
    else:
        print("file " + filename + " doesn't exist")
