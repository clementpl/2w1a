import candidat
import random

class Algo:
    def __init__(self, nbGeneration, nbPopulation, robot, percentBestToKeep=0.8, percentChildToKeep=0.2, percentToMutate=0.01):
        self.robot = robot
        self.nbGeneration = nbGeneration
        self.nbPopulation = nbPopulation
        self.populations = []
        self.percentBestToKeep = percentBestToKeep
        self.percentChildToKeep = percentChildToKeep
        self.percentToMutate = percentToMutate

    def generatePopulation(self):
        for i in range(self.nbPopulation):
            self.populations.append(candidat.Candidat(self.robot))

    def executeSequence(self):
        distanceTab = []#Array of distance [0] = distance, [1] = candidate
        for candidate in self.populations:
            distanceTab.append([candidate.getDistance(), candidate])
        #sort tab by distance
        distanceTabSorted = sorted(distanceTab, key=lambda x: x[0])
        return distanceTabSorted

    def selectBest(self, population):
        #select only the x percent best candidate
        tab = []
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
            operationsChild1.append(c2.operations[i+randomC2ToKeep])
            operationsChild2.append(c1.operations[i+randomC2ToKeep])
        for i in range(len(c1.operations)):
            if (random.randint(0,100)/100 <= self.percentToMutate):
                operationsChild1[i] = [random.randint(0, 2), random.randint(0, 360)]
            if (random.randint(0,100)/100 <= self.percentToMutate):
                operationsChild2[i] = [random.randint(0, 2), random.randint(0, 360)]
        return candidat.Candidat(self.robot, operationsChild1), candidat.Candidat(self.robot, operationsChild2)

    def getRandomCandidate(self, population):
        return population[random.randint(0, len(population) -1)]

    def createNewGeneration(self, population):
        #create child and append child to bestPopulation
        for i in range(int(self.nbPopulation*(self.percentChildToKeep/2))):
            child1, child2 = self.crossOver(self.getRandomCandidate(population), self.getRandomCandidate(population))
            population.append(child1)
            population.append(child2)
        return population

    def run(self):
        self.generatePopulation()
        for i in range(self.nbGeneration):
            self.bestPopulation = self.selectBest(self.executeSequence())
            self.population = self.createNewGeneration(self.bestPopulation)
            print (str(i) + " generation")
