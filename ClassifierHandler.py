from RocchioClassifier import RocchioClassifier
from BayesiansClassifier import  BayesiansClassifier
from CSVParser import CSVParser

class ClassifierHandler:

    def doTests(self, trainingPath, testPath):

        csvParser = CSVParser()
        bayesiansClassifier = BayesiansClassifier()
        rocchioClassifier = RocchioClassifier()

        parsedTrainingInfo = csvParser.parseTrainingSet(trainingPath)
        trainingTotalDos = parsedTrainingInfo[0]
        classes = parsedTrainingInfo[1]
        terms = parsedTrainingInfo[2]

        parsedTestSet = csvParser.parseTestSet(testPath)

        # Rocchio - beta = 0.75 gamma = 0.25
        rocchioClassifier.calculateCentroids(classes, 0.75, 0.25)
        rocchioClassifier.calculateSimilarities(parsedTestSet, 0.75, 0.25)

        # Rocchio - beta = 0.85 gamma = 0.15
        rocchioClassifier.calculateCentroids(classes, 0.85, 0.15)
        rocchioClassifier.calculateSimilarities(parsedTestSet, 0.85, 0.15)

        # Rocchio - beta = 0.95 gamma = 0.05
        rocchioClassifier.calculateCentroids(classes, 0.95, 0.05)
        rocchioClassifier.calculateSimilarities(parsedTestSet, 0.95, 0.05)

        # Bayesians
        bayesiansClassifier.calculateCentroids(trainingTotalDos, classes, terms)
        bayesiansClassifier.calculateSimilarities(parsedTestSet)          

c = ClassifierHandler()
c.doTests("training-set.csv", "test-set.csv")