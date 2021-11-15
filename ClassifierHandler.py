from RocchioClassifier import RocchioClassifier
from BayesiansClassifier import  BayesiansClassifier
from CSVParser import CSVParser
import json

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
        self.__evaluate(rocchioClassifier.similarities, "RocchioEvaluation_0.75_0.25.json")

        # Rocchio - beta = 0.85 gamma = 0.15
        rocchioClassifier.calculateCentroids(classes, 0.85, 0.15)
        rocchioClassifier.calculateSimilarities(parsedTestSet, 0.85, 0.15)
        self.__evaluate(rocchioClassifier.similarities, "RocchioEvaluation_0.85_0.15.json")

        # Rocchio - beta = 0.95 gamma = 0.05
        rocchioClassifier.calculateCentroids(classes, 0.95, 0.05)
        rocchioClassifier.calculateSimilarities(parsedTestSet, 0.95, 0.05)
        self.__evaluate(rocchioClassifier.similarities, "RocchioEvaluation_0.95_0.05.json")

        # Bayesians
        bayesiansClassifier.calculateCentroids(trainingTotalDos, classes, terms)
        bayesiansClassifier.calculateSimilarities(parsedTestSet)
        self.__evaluate(bayesiansClassifier.similarities, "BayesiansEvaluation.json")

    def __evaluate(self, similarities, filename):
        evaluation = {}
        totalDocs = len(similarities.keys())
        for sim in similarities:
            className = similarities[sim]["originalClass"]
            if className not in evaluation:
                evaluation[className] = {
                                            "a" : 0,
                                            "b" : 0,
                                            "c" : 0,
                                            "d" : 0,
                                            "e" : 0,
                                            "f" : 0,
                                            "g" : totalDocs
                                        }
            assignedClass = similarities[sim]["scale"][0][0]
            if className == assignedClass:
                evaluation[className]["a"] += 1

            evaluation[className]["c"] += 1

            if assignedClass not in evaluation:
                evaluation[assignedClass] = {
                                            "a" : 0,
                                            "b" : 0,
                                            "c" : 0,
                                            "d" : 0,
                                            "e" : 0,
                                            "f" : 0,
                                            "g" : totalDocs
                                        }
            evaluation[assignedClass]["f"] += 1

        for className in evaluation:
            a = evaluation[className]["a"]
            c = evaluation[className]["c"]
            f = evaluation[className]["f"]
            g = evaluation[className]["g"]
            evaluation[className]["b"] = c - a
            evaluation[className]["d"] = f - a
            evaluation[className]["e"] = (g - f) - evaluation[className]["b"]
            evaluation[className]["precision"] = a / f
            evaluation[className]["recall"] = a / c
            evaluation[className]["success"] = (a + evaluation[className]["e"]) / g
            evaluation[className]["error"] = (evaluation[className]["b"] + evaluation[className]["d"]) / g
        
        with open(f'results/{filename}', 'w') as outfile:
            json.dump(evaluation, outfile, indent=4) 

c = ClassifierHandler()
c.doTests("training-set.csv", "test-set.csv")