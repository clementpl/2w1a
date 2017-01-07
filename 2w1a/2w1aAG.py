"""
Simple genetic algorithm guessing a string.
"""

# ----- Dependencies

from random import random
from string import ascii_letters

# One-linner for randomly choose a element in an array
# This one-linner is fastest than random.choice(x).
choice = lambda x: x[int(random() * len(x))]

# ----- Runtime configuration (edit at your convenience)

#best score (more straight forward movement)
BEST_SCORE = 0

# Enter here the chance for an individual to mutate (range 0-1)
CHANCE_TO_MUTATE = 0.1

# Enter here the percent of top-grated individuals to be retained for the next generation (range 0-1)
PERCENT_TO_RETAIN = 0.2

# Enter here the chance for a non top-grated individual to be retained for the next generation (range 0-1)
CHANCE_RETAIN_NONGRATED = 0.05

# Number of individual in the population
POPULATION = 100

# Maximum number of generation before stopping the script
GENERATION_COUNT_MAX = 100000

# ----- Do not touch anything after this line

# Number of top-grated individuals to be retained for the next generation
NUMBER_OF_PARENT_TO_RETAIN = int(POPULATION * PERCENT_TO_RETAIN)

# Precompute the length of the expected string (individual are always fixed size objects)
LENGTH_OF_EXPECTED_STR = len(EXPECTED_STR)

# Precompute LENGTH_OF_EXPECTED_STR // 2
MIDDLE_LENGTH_OF_EXPECTED_STR = LENGTH_OF_EXPECTED_STR // 2

# Charmap of all allowed characters (A-Z a-z, space and !)
ALLOWED_CHARMAP = ascii_letters + ' !\'.'

# Maximum fitness value
MAXIMUM_FITNESS = LENGTH_OF_EXPECTED_STR

# ----- Genetic Algorithm code
# Note: An individual is simply an array of LENGTH_OF_EXPECTED_STR characters.
# And a population is nothing more than an array of individuals.

def get_random_char():
    """ Return a random char from the allowed charmap. """
    return choice(ALLOWED_CHARMAP)


def get_random_individual():
    """ Create a new random individual. """
    return [get_random_char() for _ in range(LENGTH_OF_EXPECTED_STR)]


def get_random_population():
    """ Create a new random population, made of `POPULATION` individual. """
    return [get_random_individual() for _ in range(POPULATION)]


def get_individual_fitness(individual):
    """ Compute the fitness of the given individual. """
    fitness = 0
    for c, expected_c in zip(individual, EXPECTED_STR):
        if c == expected_c:
            fitness += 1
    return fitness


def average_population_grade(population):
    """ Return the average fitness of all individual in the population. """
    total = 0
    for individual in population:
        total += get_individual_fitness(individual)
    return total / POPULATION


def grade_population(population):
    """ Grade the population. Return a list of tuple (individual, fitness) sorted from most graded to less graded. """
    graded_individual = []
    for individual in population:
        graded_individual.append((individual, get_individual_fitness(individual)))
    return sorted(graded_individual, key=lambda x: x[1], reverse=True)


def evolve_population(population):
    """ Make the given population evolving to his next generation. """

    # Get individual sorted by grade (top first), the average grade and the solution (if any)
    raw_graded_population = grade_population(population)
    average_grade = 0
    solution = []
    graded_population = []
    for individual, fitness in raw_graded_population:
        average_grade += fitness
        graded_population.append(individual)
        if fitness == MAXIMUM_FITNESS:
            solution.append(individual)
    average_grade /= POPULATION

    # End the script when solution is found
    if solution:
        return population, average_grade, solution

    # Filter the top graded individuals
    parents = graded_population[:NUMBER_OF_PARENT_TO_RETAIN]

    # Randomly add other individuals to promote genetic diversity
    for individual in graded_population[NUMBER_OF_PARENT_TO_RETAIN:]:
        if random() < CHANCE_RETAIN_NONGRATED:
            parents.append(individual)

    # Mutate some individuals
    for individual in parents:
        if random() < CHANCE_TO_MUTATE:
            place_to_modify = int(random() * LENGTH_OF_EXPECTED_STR)
            individual[place_to_modify] = get_random_char()

    # Crossover parents to create children
    parents_len = len(parents)
    desired_len = POPULATION - parents_len
    children = []
    while len(children) < desired_len:
        father = choice(parents)
        mother = choice(parents)
        if True: #father != mother:
            child = father[:MIDDLE_LENGTH_OF_EXPECTED_STR] + mother[MIDDLE_LENGTH_OF_EXPECTED_STR:]
            children.append(child)

    # The next generation is ready
    parents.extend(children)
    return parents, average_grade, solution


# ----- Runtime code

def main():
    """ Main function. """

    # Create a population and compute starting grade
    population = get_random_population()
    average_grade = average_population_grade(population)
    print('Starting grade: %.2f' % average_grade, '/ %d' % MAXIMUM_FITNESS)

    # Make the population evolve
    i = 0
    solution = None
    log_avg = []
    while not solution and i < GENERATION_COUNT_MAX:
        population, average_grade, solution = evolve_population(population)
        if i & 255 == 255:
            print('Current grade: %.2f' % average_grade, '/ %d' % MAXIMUM_FITNESS, '(%d generation)' % i)
        if i & 31 == 31:
            log_avg.append(average_grade)
        i += 1

    import pygal
    line_chart = pygal.Line(show_dots=False, show_legend=False)
    line_chart.title = 'Fitness evolution'
    line_chart.x_title = 'Generations'
    line_chart.y_title = 'Fitness'
    line_chart.add('Fitness', log_avg)
    line_chart.render_to_file('bar_chart.svg')

    # Print the final stats
    average_grade = average_population_grade(population)
    print('Final grade: %.2f' % average_grade, '/ %d' % MAXIMUM_FITNESS)

    # Print the solution
    if solution:
        print('Solution found (%d times) after %d generations.' % (len(solution), i))
    else:
        print('No solution found after %d generations.' % i)
        print('- Last population was:')
        for number, individual in enumerate(population):
            print(number, '->',  ''.join(individual))


if __name__ == '__main__':
    main()

# File created by Thibaut Royer, Epitech school
# thibaut1.royer@epitech.eu
# It intends to be an example program for the "Two wheels, one arm" educative project.

import vrep
import math
import random
import time

print ('Start')

# Close eventual old connections
vrep.simxFinish(-1)
# Connect to V-REP remote server
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

if clientID != -1:
    print ('Connected to remote API server')

    # Communication operating mode with the remote API : wait for its answer before continuing (blocking mode)
    # http://www.coppeliarobotics.com/helpFiles/en/remoteApiConstants.htm
    opmode = vrep.simx_opmode_oneshot_wait

    # Try to retrieve motors and robot handlers
    # http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm#simxGetObjectHandle
    ret1, wristHandle = vrep.simxGetObjectHandle(clientID, "WristMotor", opmode)
    ret2, elbowHandle = vrep.simxGetObjectHandle(clientID, "ElbowMotor", opmode)
    ret3, shoulderHandle = vrep.simxGetObjectHandle(clientID, "ShoulderMotor", opmode)
    ret4, robotHandle = vrep.simxGetObjectHandle(clientID, "2W1A", opmode)

    # If handlers are OK, execute three random simulations
    if ret1 == 0 and ret2 == 0 and ret3 == 0:
        random.seed()
        for i in range(0, 3):
            # Start the simulation
            # http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm#simxStartSimulation
            vrep.simxStartSimulation(clientID, opmode)
            print ("----- Simulation started -----")

            # Start getting the robot position
            # Unlike other commands, we will use a streaming operating mode
            # http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm#simxGetObjectPosition
            pret, robotPos = vrep.simxGetObjectPosition(clientID, robotHandle, -1, vrep.simx_opmode_streaming)
            print ("2w1a position: (x = " + str(robotPos[0]) +\
                  ", y = " + str(robotPos[1]) + ")")

            # Start getting the robot orientation
            # Unlike other commands, we will use a streaming operating mode
            # http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm#simxGetObjectOrientation
            oret, robotOrient = vrep.simxGetObjectOrientation(clientID, robotHandle, -1, vrep.simx_opmode_streaming)
            print ("2w1a orientation: (x = " + str(robotOrient[0]) + \
                  ", y = " + str(robotOrient[1]) +\
                  ", z = " + str(robotOrient[2]) + ")")

            # Make the robot move randomly five times
            for j in range(0, 5):
                # Generating random positions for the motors
                awrist = random.randint(0, 360)
                aelbow = random.randint(0, 360)
                ashoulder = random.randint(0, 360)

                # The control functions use Radians to determine the target position.
                # Here, we use maths.radians to convert degrees into radians.
                # http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm#simxSetJointTargetPosition
                print ("Motors target positions: " + str(ashoulder) + " " + str(aelbow) + " " + str(awrist))
                vrep.simxSetJointTargetPosition(clientID, wristHandle, math.radians(awrist), opmode)
                vrep.simxSetJointTargetPosition(clientID, elbowHandle, math.radians(aelbow), opmode)
                vrep.simxSetJointTargetPosition(clientID, shoulderHandle, math.radians(ashoulder), opmode)

                # Wait in order to let the motors finish their movements
                # Tip: there must be a more efficient way to do it...
                time.sleep(5)

                # Get the motors effective positions after the movement sequence
                # http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm#simxGetJointPosition
                pwrist = vrep.simxGetJointPosition(clientID, wristHandle, opmode)
                pelbow = vrep.simxGetJointPosition(clientID, elbowHandle, opmode)
                pshoulder = vrep.simxGetJointPosition(clientID, shoulderHandle, opmode)
                print ("Motors reached positions: " + str(ashoulder) + " " + str(aelbow) + " " + str(awrist))

                # Get the robot position after the movement sequence
                pret, robotPos = vrep.simxGetObjectPosition(clientID, robotHandle, -1, vrep.simx_opmode_buffer)
                print ("2w1a position: (x = " + str(robotPos[0]) +\
                      ", y = " + str(robotPos[1]) + ")")

                # Get the robot orientation after the movement sequence
                oret, robotOrient = vrep.simxGetObjectOrientation(clientID, robotHandle, -1, vrep.simx_opmode_buffer)
                print ("2w1a orientation: (x = " + str(robotOrient[0]) +\
                      ", y = " + str(robotOrient[1]) +\
                      ", z = " + str(robotOrient[2]) + ")")

            # End the simulation, wait to be sure V-REP had the time to stop it entirely
            # http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm#simxStopSimulation
            vrep.simxStopSimulation(clientID, opmode)
            time.sleep(1)
            print ("----- Simulation ended -----")

    # Close the connection to V-REP remote server
    # http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm#simxFinish
    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('End')
