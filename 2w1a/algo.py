import candidat
import random
import numpy
import matplotlib.pyplot as plt

class Algo:
    def __init__(self, nbGeneration, nbPopulation, robot, percentBestToKeep=0.8, percentToMutate=0.01):
        self.robot = robot
        self.nbGeneration = nbGeneration
        self.nbPopulation = nbPopulation
        self.population = []
        self.percentBestToKeep = percentBestToKeep
        self.percentToMutate = percentToMutate
        self.initGraph()

    def generatePopulation(self):
        for i in range(self.nbPopulation):
            self.population.append(candidat.Candidat(self.robot))

    def executeSequence(self):
        distanceTab = []#Array of distance [0] = distance, [1] = candidate
        for candidate in self.population:
            distanceTab.append([candidate.getDistance(), candidate])
        #sort tab by distance
        distanceTabSorted = sorted(distanceTab, key=lambda x: x[0], reverse=True)
        return [x[1] for x in distanceTabSorted] #return one dimensional array of candidate

    def selectBest(self, population):
        #select only the x percent best candidate
        tab = []
        print("SELECT BEST : len(population): " + str(len(population)) + "  if range: " + str(int(len(population)*(self.percentBestToKeep))))
        for i in range(int(len(population)*(self.percentBestToKeep))):
            tab.append(population[i])
        return tab

    def crossOver(self, c1, c2):
        #create child1 with x percent of operations of c1 append x percent of operations of c2 and add mutation
        #create child2 with x percent of operations of c1 append x percent of operations of c2 and add mutation
        randomC1ToKeep = random.randint(20, 80)
        randomC2ToKeep = 100 - randomC1ToKeep
        operationsChild1 = []
        operationsChild2 = []
        for i in range(randomC1ToKeep):
            operationsChild1.append(c1.operations[i])#TODO check for error => [operationsChild1.append(c1.operations[i]) AttributeError: 'list' object has no attribute 'operations']
            operationsChild2.append(c2.operations[i])
        for i in range(randomC2ToKeep):
            operationsChild1.append(c2.operations[i+randomC1ToKeep])
            operationsChild2.append(c1.operations[i+randomC1ToKeep])
        for i in range(len(c1.operations)):
            if (random.randint(0,100)/100 <= self.percentToMutate):
                operationsChild1[i] = [random.randint(0, 2), random.randint(0, 360)]#create new operation ([0] = motor range(0, 2) --- [1] rotation in degree)
            if (random.randint(0,100)/100 <= self.percentToMutate):
                operationsChild2[i] = [random.randint(0, 2), random.randint(0, 360)]
        return candidat.Candidat(self.robot, operationsChild1), candidat.Candidat(self.robot, operationsChild2)

    def getRandomCandidate(self, population):
        return population[random.randint(0, len(population) -1)]

    def createNewGeneration(self, population):
        #create child and append child to population
        nbNewChild = self.nbPopulation - len(population)
        print ("population nb: " + str(self.nbPopulation) + " -- len(population): " + str(len(population)) + " -- nbNewChild: " + str(nbNewChild))
        for i in range(0, nbNewChild, 2):
            child1, child2 = self.crossOver(self.getRandomCandidate(population), self.getRandomCandidate(population))
            population.append(child1)
            if (i+1 < nbNewChild):#append child 2 only if enough space in the population
                population.append(child2)
        return population

    def run(self):
        self.generatePopulation()
        for i in range(self.nbGeneration):
            print ("generation " + str(i))
            bestPopulation = self.selectBest(self.executeSequence())
            self.prepareGraph(i, bestPopulation)
            self.population = self.createNewGeneration(bestPopulation)
            self.printTabpop()
        self.graphAll()

    def printTabpop(self):
        tab = []
        for p in self.population:
            tab.append(p.dist)
        print(tab)

##
#  Graph function
##
    def initGraph(self):
        self.x = []
        self.mean = []
        self.best = []

    def prepareGraph(self, i, pop):
        self.x.append(i)
#        self.mean.append(sum(p.dist for p in pop if p.dist > -1)/len(pop))
        tabDist = [p.dist for p in pop if p.dist > -1]
        self.mean.append(sum(tabDist)/len(tabDist))
        self.best.append(max(tabDist))

    def graphAll(self):
        plt.plot(numpy.array(self.x), numpy.array(self.mean), label="mean")
        plt.plot(numpy.array(self.x), numpy.array(self.best), label="max")
        plt.legend()
        plt.xlabel("Generation")
        plt.ylabel("Distance")
        plt.show()
