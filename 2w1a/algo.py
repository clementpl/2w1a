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
        for i in range(int(len(population)*(self.percentBestToKeep))):
            tab.append(population[i])
        return tab

    def crossOverTakeBeginThenLast(self, c1, c2):
        #create child1 with x percent first operations of c1 and append x percent last operations of c2 then add mutations
        #create child2 with x percent first operations of c2 and append x percent last operations of c1 then add mutations
        randomC1ToKeep = random.randint(20, 80)
        randomC2ToKeep = 100 - randomC1ToKeep
        operationsChild1 = []
        operationsChild2 = []
        for i in range(randomC1ToKeep):
            operationsChild1.append(c1.operations[i])
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

    def crossOverTakeEachBegin(self, c1, c2):
        #create child1 with x percent first operations of c1 and append x percent first operations of c2 then add mutations
        #create child2 with x percent first operations of c2 and append x percent first operations of c1 then add mutations
        randomC1ToKeep = random.randint(20, 80)
        randomC2ToKeep = 100 - randomC1ToKeep
        operationsChild1 = []
        operationsChild2 = []
        for i in range(randomC1ToKeep):
            operationsChild1.append(c1.operations[i])
            operationsChild2.append(c2.operations[i])
        for i in range(randomC2ToKeep):
            operationsChild1.append(c2.operations[i])
            operationsChild2.append(c1.operations[i])
        for i in range(len(c1.operations)):
            if (random.randint(0,100)/100 <= self.percentToMutate):
                operationsChild1[i] = [random.randint(0, 2), random.randint(0, 360)]#create new operation ([0] = motor range(0, 2) --- [1] rotation in degree)
            if (random.randint(0,100)/100 <= self.percentToMutate):
                operationsChild2[i] = [random.randint(0, 2), random.randint(0, 360)]
        return candidat.Candidat(self.robot, operationsChild1), candidat.Candidat(self.robot, operationsChild2)

    def getRandomCandidate(self, population):
        return population[random.randint(0, len(population) -1)]

#crossover generate 2 child
    def createNewGeneration2child(self, population):
        #create child and append child to population
        nbNewChild = self.nbPopulation - len(population)
        for i in range(0, nbNewChild, 2):
#            child1, child2 = self.crossOverTakeBeginThenLast(self.getRandomCandidate(population), self.getRandomCandidate(population))
            child1, child2 = self.crossOverTakeEachBegin(self.getRandomCandidate(population), self.getRandomCandidate(population))
            population.append(child1)
            if (i+1 < nbNewChild):#append child 2 only if enough space in the population
                population.append(child2)
        return population

    #take first part of operations from c1 second part from c2
    def crossOverSimple(self, c1, c2):
        operationsChild = []
        rand = random.randint(1, 99)
        for i in range(100):#for each operation
            if (i <= rand):
                operationsChild.append(c1.operations[i])
            else:
                operationsChild.append(c2.operations[i])
            #mutate
            if (random.randint(0, 100)/100 <= self.percentToMutate):
                operationsChild[i] = [random.randint(0, 2), random.randint(0, 360)]
        return candidat.Candidat(self.robot, operationsChild)

    #take first part of operation from c1 second part from c2 then last part of operations from c1
    def crossOverDouble(self, c1, c2):
        operationsChild = []
        rand = [random.randint(1, 99), random.randint(1, 99)]
        if (random.randint(0, 1) == 0):
            tmp = c1
            c1 = c2
            c2 = c1
        for i in range(100):#for each operation
            if (i <= min(rand)):
                operationsChild.append(c1.operations[i])
            elif (i <= max(rand)):
                operationsChild.append(c2.operations[i])
            else:
                operationsChild.append(c1.operations[i])
            #mutate
            if (random.randint(0, 100)/100 <= self.percentToMutate):
                operationsChild[i] = [random.randint(0, 2), random.randint(0, 360)]
        return candidat.Candidat(self.robot, operationsChild)

    #take random operation between c1 (50%) et c2 (50%)
    def crossOverMulti(self, c1, c2):
        #create a tab with the 50% of operations of c1 to take
        randomTab = []
        while (len(randomTab) < 50):
            r = random.randint(0, 100)
            if (r not in randomTab):
                randomTab.append(r)
        #affect 50% of c1 operations and 50% of c2 operations
        operationsChild = []
        for i in range(100):#for each operation
            if (i in randomTab):
                operationsChild.append(c1.operations[i])
            else:
                operationsChild.append(c2.operations[i])
            #mutate
            if (random.randint(0, 100)/100 <= self.percentToMutate):
                operationsChild[i] = [random.randint(0, 2), random.randint(0, 360)]
        return candidat.Candidat(self.robot, operationsChild)

    #crossover generate 1 child
    def createNewGeneration(self, population):
        #create child and append child to population
        nbNewChild = self.nbPopulation - len(population)
        for i in range(0, nbNewChild):
            child = None
            #90%chance to be crossOverDouble, 10% chance to be crossOverMulti
            if (random.randint(0,9) < 9):
                child = self.crossOverDouble(self.getRandomCandidate(population), self.getRandomCandidate(population))
            else:
                child = self.crossOverMulti(self.getRandomCandidate(population), self.getRandomCandidate(population))
            population.append(child)
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
        self.min = []

    def prepareGraph(self, i, pop):
        self.x.append(i)
#        self.mean.append(sum(p.dist for p in pop if p.dist > -1)/len(pop))
        tabDist = [p.dist for p in pop if p.dist > -1]
        self.mean.append(sum(tabDist)/len(tabDist))
        self.best.append(max(tabDist))
        self.min.append(min(tabDist))

    def graphAll(self):
        plt.plot(numpy.array(self.x), numpy.array(self.mean), label="mean")
        plt.plot(numpy.array(self.x), numpy.array(self.best), label="max")
        plt.plot(numpy.array(self.x), numpy.array(self.min), label="min")
        plt.legend()
        plt.xlabel("Generation")
        plt.ylabel("Distance")
        plt.show()
